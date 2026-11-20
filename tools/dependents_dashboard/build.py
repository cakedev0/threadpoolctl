"""Build a markdown dashboard of the version constraints that other packages put
on a package: who depends on it, who caps or pins it, and what would break if a
consumer (e.g. scikit-learn) raised its minimum supported version.

    python build.py joblib:scikit-learn threadpoolctl:scikit-learn loky skore

Each argument is ``target[:consumer]``. Only needs ``packaging``.

Data sources (no credentials needed):

- PyPI metadata and download logs, from the public ClickHouse instance behind
  https://clickpy.clickhouse.com (a mirror of the PyPI BigQuery dataset). Its
  demo user is limited to 60 queries per hour and a run with 4 targets makes
  about 30 of them, so don't run this more than once per hour.
- conda-forge ``current_repodata.json`` (noarch and linux-64).
"""

import argparse
import csv
import datetime as dt
import functools
import json
import re
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path

from packaging.markers import UndefinedComparison, UndefinedEnvironmentName
from packaging.requirements import InvalidRequirement, Requirement
from packaging.specifiers import InvalidSpecifier, SpecifierSet
from packaging.utils import canonicalize_name
from packaging.version import InvalidVersion, Version

CLICKHOUSE_URL = "https://sql-clickhouse.clickhouse.com/?user=demo"
TOP_PACKAGES_URL = (
    "https://hugovk.github.io/top-pypi-packages/top-pypi-packages.min.json"
)
CONDA_URL = "https://conda.anaconda.org/conda-forge/{subdir}/current_repodata.json"
CONDA_SUBDIRS = ("noarch", "linux-64")
USER_AGENT = "dependents-dashboard"

DOWNLOAD_DAYS = 30
CI_DAYS = 7
ACTIVE_MONTHS = 12
POPULAR_DOWNLOADS = 10_000
N_MINORS = 6

# Environment used to evaluate the markers of the requirements.
MARKER_ENV = {
    "python_version": "3.13",
    "python_full_version": "3.13.5",
    "sys_platform": "linux",
    "platform_system": "Linux",
    "platform_machine": "x86_64",
    "implementation_name": "cpython",
    "platform_python_implementation": "CPython",
    "os_name": "posix",
}

NORM_NAME = "lower(replaceRegexpAll(name, '[-_.]+', '-'))"


# --------------------------------------------------------------------------
# Data access


def clickhouse(sql):
    request = urllib.request.Request(
        CLICKHOUSE_URL,
        data=(sql + " FORMAT JSONCompact").encode(),
        headers={"User-Agent": USER_AGENT},
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return json.load(response)["data"]
    except urllib.error.HTTPError as error:
        # ClickHouse explains the failure in the body.
        raise RuntimeError(error.read().decode(errors="replace")[:500]) from error


def requirement_regex(name):
    """RE2 regex (without backslashes) matching a requirement on `name`."""
    name = canonicalize_name(name).replace("-", "[-_.]+")
    return f"(?i)^[[:space:]]*{name}[[:space:]]*([[(<>=!~;,[:space:]]|$)"


def sql_list(values):
    return ", ".join("'" + v.replace("'", "") + "'" for v in values)


def pypi_json(name, version=None):
    """Metadata of a release (the latest final one by default), or None."""
    path = f"{name}/{version}" if version else name
    request = urllib.request.Request(
        f"https://pypi.org/pypi/{path}/json", headers={"User-Agent": USER_AGENT}
    )
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            if error.code == 404:
                return None
        except OSError:
            pass
        time.sleep(2 * (attempt + 1))
    raise OSError(f"can't fetch the PyPI metadata of {path}")


def fetch_releases(name):
    """{Version: first upload date} of the final releases of a project."""
    releases = {}
    for version, files in pypi_json(name)["releases"].items():
        try:
            version = Version(version)
        except InvalidVersion:
            continue
        if files and not (version.is_prerelease or version.is_devrelease):
            date = min(file["upload_time"] for file in files)[:10]
            releases[version] = dt.date.fromisoformat(date)
    return dict(sorted(releases.items()))


def wheelodex_dependents(target):
    """Projects whose latest wheel requires `target`, from wheelodex.org."""
    names, page = set(), 1
    while True:
        request = urllib.request.Request(
            f"https://www.wheelodex.org/projects/{target}/rdepends/?page={page}",
            headers={"User-Agent": USER_AGENT},
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                html = response.read().decode()
        except urllib.error.HTTPError as error:
            # The page after the last one is a 404.
            if error.code == 404 and page > 1:
                return names
            raise
        found = set(re.findall(r'href="/projects/([^"/]+)/"', html)) - {target}
        if not found - names:
            return names
        names |= found
        page += 1


def top_packages(target):
    """The most downloaded PyPI projects, whatever they depend on."""
    request = urllib.request.Request(
        TOP_PACKAGES_URL, headers={"User-Agent": USER_AGENT}
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return {row["project"] for row in json.load(response)["rows"]}


def clickhouse_dependents(target):
    """Projects with a release that requires `target`, from ClickHouse."""
    query = (
        f"SELECT DISTINCT {NORM_NAME} AS n FROM pypi.projects WHERE "
        f"arrayExists(x -> match(x, '{requirement_regex(target)}'), requires_dist)"
    )
    try:
        rows = clickhouse(query)
    except RuntimeError as error:
        # More rows than the demo user can get at once.
        if "TOO_MANY_ROWS" not in str(error):
            raise
        n_buckets = 8
        rows = []
        for bucket in range(n_buckets):
            rows += clickhouse(f"{query} AND cityHash64(n) % {n_buckets} = {bucket}")
    return {row[0] for row in rows} - {target}


def fetch_pypi_dependents(target, cache):
    """Latest final release of each project that may require `target`.

    Returns {name: (version, upload date, requires_dist)}.

    PyPI has no reverse dependency index. The candidates are the union of two
    incomplete ones (Wheelodex and the ClickHouse copy of the PyPI metadata
    both miss projects, scikit-learn for instance) and of the 15000 most
    downloaded projects, so that no popular project is missed. The
    requirements of each candidate are then read from PyPI.
    """
    candidates = set()
    for source in (wheelodex_dependents, clickhouse_dependents, top_packages):
        try:
            found = {canonicalize_name(name) for name in source(target)}
        except (OSError, RuntimeError, ValueError) as error:
            print(f"  {source.__name__} failed: {error!r}")
            continue
        print(f"  {source.__name__}: {len(found)} candidates")
        candidates |= found

    def fetch(name):
        if name not in cache:
            try:
                data = pypi_json(name)
            except OSError:
                return name, None
            if data is None:
                cache[name] = None
            else:
                dates = [file["upload_time"][:10] for file in data["urls"]]
                cache[name] = (
                    data["info"]["version"],
                    max(dates, default=None),
                    data["info"].get("requires_dist") or [],
                )
        return name, cache[name]

    with ThreadPoolExecutor(16) as executor:
        results = list(executor.map(fetch, sorted(candidates - {target})))
    return {
        name: (version, dt.date.fromisoformat(date), reqs)
        for name, (version, date, reqs) in (r for r in results if r[1])
        if date
    }


def fetch_downloads(names):
    """{name: downloads over the last DOWNLOAD_DAYS days}."""
    names = sorted(names)
    downloads = {}
    for start in range(0, len(names), 5000):
        chunk = names[start : start + 5000]
        for name, count in clickhouse(
            "SELECT project, sum(count) FROM pypi.pypi_downloads_per_day "
            f"WHERE date >= today() - {DOWNLOAD_DAYS} AND date < today() "
            f"AND project IN ({sql_list(chunk)}) GROUP BY project"
        ):
            downloads[name] = int(count)
    return downloads


def fetch_ci_share(downloads):
    """{name: share of the downloads of the last CI_DAYS days made from a CI}.

    `downloads` maps the projects to their downloads over DOWNLOAD_DAYS. This
    reads the raw download logs, which the demo user can only scan 1e9 rows
    of per query: the projects are batched to stay well under that.
    """
    max_rows = 3e8
    batches, batch, rows = [], [], 0
    for name, count in sorted(downloads.items(), key=lambda item: -item[1]):
        estimate = count * CI_DAYS / DOWNLOAD_DAYS
        if estimate > max_rows:
            continue
        if batch and (rows + estimate > max_rows or len(batch) >= 500):
            batches.append(batch)
            batch, rows = [], 0
        batch.append(name)
        rows += estimate
    if batch:
        batches.append(batch)
    shares = {}
    for batch in batches:
        try:
            rows = clickhouse(
                "SELECT project, countIf(ci = 'true'), count() FROM pypi.pypi "
                f"WHERE date >= today() - {CI_DAYS} AND date < today() "
                f"AND project IN ({sql_list(batch)}) GROUP BY project"
            )
        except (OSError, RuntimeError) as error:
            print(f"  CI share: a batch of {len(batch)} projects failed: {error!r}")
            continue
        shares.update(
            {name: int(ci) / int(total) for name, ci, total in rows if int(total)}
        )
    return shares


def fetch_version_downloads(name):
    """{Version: (downloads, downloads from CI)} over the last DOWNLOAD_DAYS."""
    name = canonicalize_name(name)
    totals = defaultdict(lambda: [0, None])
    for version, count in clickhouse(
        "SELECT version, sum(count) FROM pypi.pypi_downloads_per_day_by_version "
        f"WHERE project = '{name}' AND date >= today() - {DOWNLOAD_DAYS} "
        "AND date < today() GROUP BY version"
    ):
        try:
            totals[Version(version)][0] += int(count)
        except InvalidVersion:
            pass
    for days in (DOWNLOAD_DAYS, CI_DAYS):
        try:
            rows = clickhouse(
                "SELECT version, countIf(ci = 'true'), count() FROM pypi.pypi "
                f"WHERE project = '{name}' AND date >= today() - {days} "
                "AND date < today() GROUP BY version"
            )
        except (OSError, RuntimeError) as error:
            print(f"  CI share by version over {days} days failed: {error!r}")
            continue
        for version, ci, total in rows:
            try:
                version = Version(version)
            except InvalidVersion:
                continue
            if int(total):
                totals[version][1] = int(ci) / int(total)
        break
    return {version: tuple(values) for version, values in totals.items()}


def fetch_conda_packages():
    """Latest build of each conda-forge package: {name: record}."""
    latest = {}
    for subdir in CONDA_SUBDIRS:
        request = urllib.request.Request(
            CONDA_URL.format(subdir=subdir), headers={"User-Agent": USER_AGENT}
        )
        with urllib.request.urlopen(request, timeout=600) as response:
            repodata = json.load(response)
        for key in ("packages", "packages.conda"):
            for record in repodata.get(key, {}).values():
                try:
                    order = (
                        Version(record["version"]),
                        record.get("build_number", 0),
                        record.get("timestamp", 0),
                    )
                except InvalidVersion:
                    continue
                name = record["name"]
                if name not in latest or order > latest[name][0]:
                    latest[name] = (order, record)
    return {name: record for name, (_, record) in latest.items()}


def conda_specifier(spec):
    """Convert the version part of a conda match spec to a SpecifierSet.

    Returns None for the specs it can't convert (``|`` alternatives).
    """
    if "|" in spec:
        return None
    clauses = []
    for clause in spec.split(","):
        clause = clause.strip()
        if not clause or clause == "*":
            continue
        match = re.match(r"^(>=|<=|==|!=|~=|>|<|=)?\s*(.+)$", clause)
        operator, version = match.groups()
        if operator in (None, "=", "=="):
            if operator == "=" and not version.endswith("*"):
                version += ".*"
            clause = "==" + re.sub(r"(?<!\.)\*$", ".*", version)
        else:
            clause = operator + version.rstrip(".*")
        clauses.append(clause)
    try:
        return SpecifierSet(",".join(clauses))
    except InvalidSpecifier:
        return None


# --------------------------------------------------------------------------
# Analysis


@dataclass
class Dependent:
    name: str
    version: str
    date: dt.date
    # Specifiers on the target that apply together (core requirements), or one
    # per extra when the target is only required by extras.
    specs: list
    extra_only: bool
    # None: no requirement on the consumer.
    consumer_specs: list | None
    downloads: int | None = None
    ci_share: float | None = None
    max_allowed: Version | None = None
    min_allowed: Version | None = None
    kind: str = ""
    exact: bool = False
    allows_next_minor: bool = True
    allows_next_major: bool = True
    consumer: str = field(default="")

    @property
    def spec_text(self):
        texts = sorted({str(spec) or "any" for spec in self.specs})
        return "; ".join(texts)

    @property
    def consumer_text(self):
        if self.consumer_specs is None:
            return ""
        return "; ".join(sorted({str(s) or "any" for s in self.consumer_specs}))


def split_requirements(reqs, name):
    """Specifiers of the requirements on `name`: (core, only in extras)."""
    core, extra = [], []
    for req in reqs:
        try:
            req = Requirement(req)
        except InvalidRequirement:
            continue
        if canonicalize_name(req.name) != name:
            continue
        if req.marker is None:
            core.append(req.specifier)
            continue
        try:
            if req.marker.evaluate({**MARKER_ENV, "extra": ""}):
                core.append(req.specifier)
            elif "extra" in str(req.marker):
                extra.append(req.specifier)
        except (UndefinedComparison, UndefinedEnvironmentName):
            # A marker that can't be evaluated: ignore the requirement.
            pass
    return core, extra


def pypi_dependents(target, consumer, raw):
    dependents = []
    for name, (version, date, reqs) in raw.items():
        core, extra = split_requirements(reqs, target)
        if not core and not extra:
            continue
        consumer_specs = None
        if consumer:
            consumer_core, consumer_extra = split_requirements(reqs, consumer)
            consumer_specs = consumer_core or consumer_extra or None
        dependents.append(
            Dependent(name, version, date, core or extra, not core, consumer_specs)
        )
    return dependents


def conda_dependents(target, consumer, packages):
    def specs_on(record, name):
        specs = []
        for depend in record.get("depends", []):
            parts = depend.split()
            if parts and parts[0] == name:
                spec = conda_specifier(parts[1]) if len(parts) > 1 else SpecifierSet()
                if spec is not None:
                    specs.append(spec)
        return specs

    dependents = []
    for name, record in packages.items():
        specs = specs_on(record, target)
        if not specs:
            continue
        consumer_specs = (specs_on(record, consumer) or None) if consumer else None
        timestamp = record.get("timestamp", 0) / 1000
        date = dt.date.fromtimestamp(timestamp) if timestamp else dt.date.min
        dependents.append(
            Dependent(name, record["version"], date, specs, False, consumer_specs)
        )
    return dependents


def next_versions(versions):
    latest = max(versions)
    return Version(f"{latest.major}.{latest.minor + 1}.0"), Version(
        f"{latest.major + 1}.0.0"
    )


def allowed(dependent, versions):
    """Versions accepted by the dependent (by its most restrictive extra when
    the target is only required by extras)."""

    def accepted(specs):
        return {
            v for v in versions if all(s.contains(v, prereleases=True) for s in specs)
        }

    if not dependent.extra_only:
        return accepted(dependent.specs)
    return set.intersection(*(accepted([spec]) for spec in dependent.specs))


def classify(dependents, releases, consumer_next):
    versions = list(releases)
    next_minor, next_major = next_versions(versions)
    for dep in dependents:
        ok = allowed(dep, versions + [next_minor, next_major])
        real = ok - {next_minor, next_major}
        dep.max_allowed = max(real, default=None)
        dep.min_allowed = min(real, default=None)
        dep.allows_next_minor = next_minor in ok
        dep.allows_next_major = next_major in ok
        operators = {s.operator for spec in dep.specs for s in spec}
        dep.exact = (
            bool(operators)
            and operators <= {"==", "==="}
            and not any("*" in s.version for spec in dep.specs for s in spec)
        )
        if not operators:
            dep.kind = "none"
        elif operators <= {">=", ">", "!="}:
            dep.kind = "lower"
        else:
            dep.kind = "capped"
        if dep.consumer_specs is None:
            dep.consumer = "none"
        elif all(
            s.contains(consumer_next, prereleases=True) for s in dep.consumer_specs
        ):
            dep.consumer = "allows"
        else:
            dep.consumer = "excludes"


def minor(version):
    return (version.major, version.minor)


def minor_series(releases):
    """{(major, minor): first version of the series}, oldest first."""
    series = {}
    for version in releases:
        series.setdefault(minor(version), version)
    return series


def consumer_history(consumer, target):
    """[(first version of a consumer series, release date, lower bound on
    target)] for the last N_MINORS series, oldest first."""
    releases = fetch_releases(consumer)
    history = []
    for first in list(minor_series(releases).values())[-N_MINORS:]:
        data = pypi_json(consumer, first)
        reqs = (data["info"].get("requires_dist") or []) if data else []
        core, _ = split_requirements(reqs, target)
        lower = [
            Version(s.version) for spec in core for s in spec if s.operator == ">="
        ]
        history.append((first, releases[first], max(lower, default=None)))
    return history


# --------------------------------------------------------------------------
# Rendering


def human(number):
    if number is None:
        return ""
    for threshold, suffix in ((1e9, "B"), (1e6, "M"), (1e3, "k")):
        if number >= threshold:
            value = number / threshold
            return f"{value:.1f}{suffix}" if value < 10 else f"{value:.0f}{suffix}"
    return str(int(number))


def percent(share):
    if share is None:
        return ""
    return f"{100 * share:.0f}%"


def months_between(start, end):
    return (end - start).days / 30.44


def table(header, rows):
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    lines += [
        "| " + " | ".join(str(cell).replace("|", "\\|") for cell in row) + " |"
        for row in rows
    ]
    return "\n".join(lines)


def link(dep, source):
    if source == "pypi":
        return f"[{dep.name}](https://pypi.org/project/{dep.name}/)"
    return f"[{dep.name}](https://anaconda.org/conda-forge/{dep.name})"


class Stats:
    """Counts of a group of dependents: all / active / popular."""

    def __init__(self, today, source):
        self.today = today
        self.source = source

    def is_active(self, dep):
        return months_between(dep.date, self.today) <= ACTIVE_MONTHS

    def is_popular(self, dep):
        return (dep.downloads or 0) >= POPULAR_DOWNLOADS

    @property
    def header(self):
        header = ["Projects", "Active"]
        if self.source == "pypi":
            header.append(f">= {human(POPULAR_DOWNLOADS)} dl")
        return header

    def cells(self, group):
        cells = [len(group), sum(self.is_active(dep) for dep in group)]
        if self.source == "pypi":
            cells.append(sum(self.is_popular(dep) for dep in group))
        return cells


def dependents_table(deps, source, consumer, limit=None):
    deps = sorted(deps, key=lambda d: (-(d.downloads or 0), d.name))
    shown = deps[:limit] if limit else deps
    header = ["Project", "Latest release"]
    if source == "pypi":
        header += [f"Downloads ({DOWNLOAD_DAYS} d)", "From CI"]
    header.append("Constraint")
    if consumer:
        header.append(f"On {consumer}")
    rows = []
    for dep in shown:
        row = [link(dep, source), f"{dep.version} ({dep.date:%Y-%m})"]
        if source == "pypi":
            row += [human(dep.downloads or 0), percent(dep.ci_share)]
        spec = f"`{dep.spec_text}`" + (" (extra)" if dep.extra_only else "")
        row.append(spec)
        if consumer:
            row.append(f"`{dep.consumer_text}`" if dep.consumer_text else "")
        rows.append(row)
    text = table(header, rows)
    if limit and len(deps) > limit:
        text += f"\n\n{len(deps) - limit} more, see the CSV file."
    return text


def render_constraints(deps, releases, target, consumer, consumer_next, source, today):
    """Sections that are the same for PyPI and conda-forge."""
    stats = Stats(today, source)
    series = minor_series(releases)
    recent = list(series)[-N_MINORS:]
    latest = max(releases)
    next_minor, next_major = next_versions(list(releases))
    out = []

    groups = {
        "No constraint": [d for d in deps if d.kind == "none"],
        "Lower bound only": [d for d in deps if d.kind == "lower"],
        f"Upper bound or pin, allows {latest}": [
            d for d in deps if d.kind == "capped" and d.max_allowed == latest
        ],
        f"Excludes {latest}": [
            d for d in deps if d.kind == "capped" and d.max_allowed != latest
        ],
    }
    rows = [[label, *stats.cells(group)] for label, group in groups.items()]
    rows.append(["**Total**", *stats.cells(deps)])
    out.append(table([f"Constraint on {target}", *stats.header], rows))
    if not any(d.kind == "capped" for d in deps):
        out.append(f"No project puts an upper bound on {target}.")
        return out

    # What a higher minimum would exclude.
    excluded_header = [f"Minimum {target}", *stats.header, "Exact pins"]
    if consumer:
        excluded_header += [
            f"Also exclude {consumer} {consumer_next}",
            f"**Allow {consumer} {consumer_next}**",
            f"No {consumer} dependency",
        ]
    rows, details = [], []
    for key in recent:
        first = series[key]
        group = [d for d in deps if d.max_allowed is None or d.max_allowed < first]
        row = [f">= {first}", *stats.cells(group), sum(d.exact for d in group)]
        if consumer:
            by_consumer = Counter(d.consumer for d in group)
            row += [
                by_consumer["excludes"],
                f"**{by_consumer['allows']}**",
                by_consumer["none"],
            ]
            conflicts = [d for d in group if d.consumer == "allows"]
            if conflicts:
                details.append((first, conflicts))
        rows.append(row)
    out.append(f"### What a higher minimum version of {target} would exclude")
    text = (
        f"Each row counts the projects whose latest release can't be installed "
        f"with {target} at or above the given version."
    )
    if consumer:
        text += (
            f" The bold column is the one that matters for {consumer}: projects "
            f"that accept {consumer} {consumer_next} (the next minor release) but "
            f"not this version of {target}. They would have no solution if "
            f"{consumer} {consumer_next} required it (for the ones marked "
            f'"(extra)", only with that extra). The projects of the last '
            f"column only conflict when installed next to {consumer}."
        )
    out += [text, table(excluded_header, rows)]
    if details:
        first, conflicts = details[-1]
        out.append(
            f"Projects that accept {consumer} {consumer_next} but not "
            f"{target} >= {first}:"
        )
        out.append(dependents_table(conflicts, source, consumer, limit=40))
    notable = [
        d
        for d in deps
        if d.max_allowed != latest and d.consumer == "none" and stats.is_popular(d)
    ]
    if consumer and notable:
        out.append(
            f"Projects with >= {human(POPULAR_DOWNLOADS)} downloads that exclude "
            f"{target} {latest} and don't depend on {consumer}:"
        )
        out.append(dependents_table(notable, source, consumer, limit=20))

    # Highest minor allowed.
    out.append(f"### Highest {target} series allowed")
    out.append(
        f"For the projects that exclude {latest}: the most recent series they accept."
    )
    by_series = defaultdict(list)
    for dep in groups[f"Excludes {latest}"]:
        if dep.max_allowed is None:
            by_series["none"].append(dep)
        elif minor(dep.max_allowed) in recent:
            by_series[minor(dep.max_allowed)].append(dep)
        else:
            by_series["older"].append(dep)
    rows = []
    for key in [*reversed(recent[:-1]), "older", "none"]:
        group = by_series.get(key, [])
        if not group and key == "none":
            continue
        label = {
            "older": f"Older than {recent[0][0]}.{recent[0][1]}",
            "none": "No released version",
        }.get(key) or f"{key[0]}.{key[1]}"
        exact = sum(d.exact for d in group)
        rows.append([label, *stats.cells(group), exact, len(group) - exact])
    out.append(table(["Series", *stats.header, "Exact pins", "Range caps"], rows))

    # Next releases.
    blockers = [d for d in deps if d.max_allowed == latest and not d.allows_next_minor]
    major_caps = [d for d in deps if d.allows_next_minor and not d.allows_next_major]
    out.append("### Caps on the next releases")
    out.append(
        f"Projects that accept {latest} but would exclude {next_minor}: "
        f"{len(blockers)}, of which {sum(d.exact for d in blockers)} with an "
        f"exact pin. Projects that would accept {next_minor} but exclude "
        f"{next_major}: {len(major_caps)}."
    )
    if blockers:
        out.append(dependents_table(blockers, source, consumer, limit=20))

    # Lower bounds.
    out.append("### Lower bounds")
    out.append(
        f"The oldest {target} series accepted by the projects that have a "
        "lower bound (or a pin). The last column is the cumulative share of "
        f"those projects that require this series or a more recent one."
    )
    with_lower = [
        d for d in deps if d.min_allowed is not None and d.min_allowed != min(releases)
    ]
    by_min = Counter(
        minor(d.min_allowed) if minor(d.min_allowed) in recent else "older"
        for d in with_lower
    )
    rows, cumulative = [], 0
    for key in [*reversed(recent), "older"]:
        cumulative += by_min[key]
        label = (
            f"Older than {recent[0][0]}.{recent[0][1]}"
            if key == "older"
            else f"{key[0]}.{key[1]}"
        )
        share = percent(cumulative / len(with_lower)) if with_lower else ""
        rows.append([label, by_min[key], share])
    out.append(table(["Oldest series accepted", "Projects", "Cumulative"], rows))
    return out


def render_target(target, consumer, data, today):
    releases = data["releases"]
    latest = max(releases)
    series = minor_series(releases)
    out = [f"# {target}"]
    intro = (
        f"Version constraints that other packages put on "
        f"[{target}](https://pypi.org/project/{target}/). Latest release: "
        f"{latest} ({releases[latest]}). Generated on {today}."
    )
    out.append(intro)
    out.append("See the [README](README.md) for the method and its limits.")

    # Releases and downloads.
    out.append(f"## Which versions of {target} get installed")
    version_downloads = data["version_downloads"]
    total = sum(count for count, _ in version_downloads.values()) or 1
    recent = list(series)[-N_MINORS:]
    rows, cumulative = [], 0.0
    by_series = defaultdict(lambda: [0, 0.0, 0])
    for version, (count, ci) in version_downloads.items():
        key = minor(version) if minor(version) in recent else "older"
        by_series[key][0] += count
        if ci is not None:
            by_series[key][1] += ci * count
            by_series[key][2] += count
    for key in [*reversed(recent), "older"]:
        count, ci_weighted, ci_count = by_series[key]
        cumulative += count / total
        if key == "older":
            label, date, age = f"Older than {recent[0][0]}.{recent[0][1]}", "", ""
        else:
            first = series[key]
            label, date = f"{key[0]}.{key[1]}", releases[first]
            age = f"{months_between(date, today):.0f}"
        rows.append(
            [
                label,
                date,
                age,
                human(count),
                percent(count / total),
                percent(cumulative),
                percent(ci_weighted / ci_count) if ci_count else "",
            ]
        )
    out.append(
        f"Downloads from PyPI over the last {DOWNLOAD_DAYS} days, by series. "
        '"From CI" is the share of the downloads made with the `CI` environment '
        "variable set, as reported by pip and uv."
    )
    out.append(
        table(
            [
                "Series",
                "First release",
                "Age (months)",
                "Downloads",
                "Share",
                "Cumulative",
                "From CI",
            ],
            rows,
        )
    )

    if consumer and data["history"]:
        out.append(f"## What {consumer} requires")
        rows = []
        for version, date, lower in data["history"][-N_MINORS:]:
            if lower is None:
                rows.append([f"{version.major}.{version.minor}", date, "", "", ""])
                continue
            lower_date = releases.get(lower)
            age = f"{months_between(lower_date, date):.0f}" if lower_date else ""
            newer = [v for v in series.values() if v > lower and releases[v] <= date]
            rows.append(
                [
                    f"{version.major}.{version.minor}",
                    date,
                    f"`{target}>={lower}`",
                    age,
                    len(newer),
                ]
            )
        out.append(
            f"The minimum version of {target} required by each {consumer} "
            "series, its age when that series was released, and the number of "
            f"more recent {target} series that existed then."
        )
        out.append(
            table(
                [
                    f"{consumer}",
                    "Released",
                    "Requires",
                    "Age of the minimum (months)",
                    "Newer series available",
                ],
                rows,
            )
        )

    consumer_next = data["consumer_next"]
    for source, title in (("pypi", "PyPI"), ("conda", "conda-forge")):
        deps = data[source]
        out.append(f"## {title} dependents")
        if not deps:
            out.append(f"No {title} package depends on {target}.")
            continue
        if source == "pypi":
            out.append(
                f"{len(deps)} projects require {target} in their latest release "
                f"([CSV](data/{target}-pypi.csv)). Active: latest release less "
                f"than {ACTIVE_MONTHS} months ago. Downloads are over the last "
                f"{DOWNLOAD_DAYS} days."
            )
        else:
            out.append(
                f"{len(deps)} conda-forge packages depend on {target} in their "
                f"latest build ([CSV](data/{target}-conda.csv)). Active: latest "
                f"build less than {ACTIVE_MONTHS} months ago."
            )
        out += render_constraints(
            deps, releases, target, consumer, consumer_next, source, today
        )
        if source == "pypi":
            out.append("### Most downloaded dependents")
            out.append(dependents_table(deps, source, consumer, limit=25))
    return "\n\n".join(out) + "\n"


def render_index(targets, all_data, today):
    out = ["# Dependents dashboard"]
    out.append(
        "Who depends on the packages we maintain, which versions they accept, "
        "and what a higher minimum version in a consumer (e.g. scikit-learn) "
        f"would break. Generated on {today} by `build.py`."
    )
    rows = []
    for target, consumer in targets:
        data = all_data[target]
        latest = max(data["releases"])
        row = [f"[{target}]({target}.md)", f"{latest} ({data['releases'][latest]})"]
        for source in ("pypi", "conda"):
            deps = data[source]
            capped = [d for d in deps if d.kind == "capped"]
            excluding = [d for d in capped if d.max_allowed != latest]
            blockers = [
                d for d in deps if d.max_allowed == latest and not d.allows_next_minor
            ]
            row += [len(deps), len(capped), len(excluding), len(blockers)]
        rows.append(row)
    header = ["Package", "Latest release"]
    for source in ("PyPI", "conda-forge"):
        header += [
            f"{source} dependents",
            "With upper bound or pin",
            "Exclude the latest release",
            "Exclude the next minor",
        ]
    out.append(table(header, rows))
    out.append(README_METHOD)
    return "\n\n".join(out) + "\n"


README_METHOD = f"""\
## How to read the pages

Each page has, for one package (the target):

- **Which versions get installed**: the PyPI downloads of the last \
{DOWNLOAD_DAYS} days by series, with the share that comes from CI jobs. This \
tells how many environments still get an old series.
- **What the consumer requires**: the history of the minimum version in the \
consumer (scikit-learn for joblib and threadpoolctl), and how old it was.
- **Dependents**: the constraint of the latest release of each project that \
depends on the target, on PyPI and on conda-forge. The main table gives what a \
higher minimum version would exclude, and separates the projects that also \
exclude the next consumer release (pinned environments, nothing changes for \
them) from the ones that accept it (real conflicts).

## Method

- PyPI: PyPI has no reverse dependency index. The candidates are the union of the projects listed by [Wheelodex](https://www.wheelodex.org), of the ones with any release requiring the target in ClickHouse, and of the [15000 most downloaded projects](https://hugovk.github.io/top-pypi-packages/). The first two are incomplete (both miss scikit-learn as a dependent of threadpoolctl), the third one makes sure that no popular project is missed. The requirements of the latest final release of each candidate are then read from the PyPI JSON API. The download counts come from the public ClickHouse instance behind [ClickPy](https://clickpy.clickhouse.com), a copy of the PyPI download logs. The requirements of the latest final release of each candidate are then read from the PyPI JSON API.
- conda-forge: the latest build of each package in `current_repodata.json` \
(noarch and linux-64).
- Markers are evaluated for CPython 3.13 on Linux x86_64. A project that only \
requires the target in extras is counted with its most restrictive extra and \
marked "(extra)".
- "Exclude" means that no released version at or above the given one satisfies \
the constraint.

## Limits

- Only the latest release of each project is read. A resolver can fall back to an older release, so an excluded project may still install, with an old version of itself.
- The lockfiles and `requirements.txt` of applications are not on PyPI, so \
they are not counted. Exact pins published on PyPI are a small sample of them.
- Downloads include mirrors and CI jobs. The CI share is only known for the \
installers that report it (pip and uv), over the last {CI_DAYS} days for \
dependents.
- conda-forge packages have no download counts here, and repodata patches \
added after a build are included but `run_constrained` is not.

## Update

```bash
pip install packaging
python build.py joblib:scikit-learn threadpoolctl:scikit-learn loky skore
```

A run takes about 10 minutes (it reads the metadata of ~20000 projects from \
PyPI) and makes about 30 queries to ClickHouse, whose public user is limited \
to 60 queries per hour.
"""


def write_csv(path, deps, consumer):
    with open(path, "w", newline="") as file:
        writer = csv.writer(file, lineterminator="\n")
        header = [
            "name",
            "version",
            "date",
            "downloads",
            "ci_share",
            "constraint",
            "extra_only",
            "kind",
            "min_allowed",
            "max_allowed",
            "allows_next_minor",
            "allows_next_major",
        ]
        if consumer:
            header.append(f"constraint_on_{consumer}")
        writer.writerow(header)
        for dep in sorted(deps, key=lambda d: (-(d.downloads or 0), d.name)):
            row = [
                dep.name,
                dep.version,
                dep.date,
                dep.downloads if dep.downloads is not None else "",
                f"{dep.ci_share:.2f}" if dep.ci_share is not None else "",
                dep.spec_text,
                int(dep.extra_only),
                dep.kind,
                dep.min_allowed or "",
                dep.max_allowed or "",
                int(dep.allows_next_minor),
                int(dep.allows_next_major),
            ]
            if consumer:
                row.append(dep.consumer_text)
            writer.writerow(row)


print = functools.partial(print, flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("targets", nargs="+", help="target[:consumer]")
    parser.add_argument("--out", type=Path, default=Path(__file__).parent / "dashboard")
    parser.add_argument("--no-conda", action="store_true")
    parser.add_argument(
        "--cache", type=Path, help="JSON file to reuse the PyPI metadata between runs"
    )
    args = parser.parse_args()

    today = dt.date.today()
    targets = []
    for arg in args.targets:
        target, _, consumer = arg.partition(":")
        targets.append((canonicalize_name(target), canonicalize_name(consumer) or None))

    (args.out / "data").mkdir(parents=True, exist_ok=True)
    conda_packages = {} if args.no_conda else fetch_conda_packages()
    # PyPI metadata of the candidates, shared by the targets (and by runs when
    # --cache is given).
    cache = {}
    if args.cache and args.cache.exists():
        cache = json.loads(args.cache.read_text())

    all_data = {}
    for target, consumer in targets:
        print(f"{target}: fetching")
        releases = fetch_releases(target)
        consumer_next = None
        history = []
        if consumer:
            consumer_next, _ = next_versions(list(fetch_releases(consumer)))
            history = consumer_history(consumer, target)
        pypi = pypi_dependents(target, consumer, fetch_pypi_dependents(target, cache))
        if args.cache:
            args.cache.write_text(json.dumps(cache))
        conda = conda_dependents(target, consumer, conda_packages)
        for deps in (pypi, conda):
            classify(deps, releases, consumer_next or Version("0"))
        downloads = fetch_downloads(dep.name for dep in pypi)
        for dep in pypi:
            dep.downloads = downloads.get(dep.name, 0)
        # CI share of the projects that show up in the tables.
        top = sorted(pypi, key=lambda d: -d.downloads)[:25]
        listed = {d.name for d in top} | {
            d.name for d in pypi if d.kind == "capped" and not d.allows_next_minor
        }
        ci_shares = fetch_ci_share({name: downloads.get(name, 0) for name in listed})
        for dep in pypi:
            dep.ci_share = ci_shares.get(dep.name)
        all_data[target] = {
            "releases": releases,
            "version_downloads": fetch_version_downloads(target),
            "history": history,
            "consumer_next": consumer_next,
            "pypi": pypi,
            "conda": conda,
        }
        write_csv(args.out / "data" / f"{target}-pypi.csv", pypi, consumer)
        write_csv(args.out / "data" / f"{target}-conda.csv", conda, consumer)
        page = render_target(target, consumer, all_data[target], today)
        (args.out / f"{target}.md").write_text(page)
        print(f"{target}: {len(pypi)} PyPI dependents, {len(conda)} on conda-forge")
    (args.out / "README.md").write_text(render_index(targets, all_data, today))


if __name__ == "__main__":
    main()
