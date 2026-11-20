import datetime as dt

import pytest

pytest.importorskip("packaging")

from build import (
    Dependent,
    classify,
    conda_specifier,
    requirement_regex,
    split_requirements,
)
from packaging.specifiers import SpecifierSet
from packaging.version import Version


@pytest.mark.parametrize(
    "spec, accepted, rejected",
    [
        (">=1.2.0", ["1.2.0", "1.6.0"], ["1.1.1"]),
        (">=1.2,<1.5", ["1.4.2"], ["1.5.0"]),
        (">=1.2,<1.5.0a0", ["1.4.2"], ["1.5.0"]),
        ("1.4.*", ["1.4.0", "1.4.2"], ["1.5.0", "1.3.2"]),
        ("1.4*", ["1.4.2"], ["1.5.0"]),
        ("=1.4", ["1.4.2"], ["1.5.0"]),
        ("==1.4.2", ["1.4.2"], ["1.4.0"]),
        ("1.4.2", ["1.4.2"], ["1.4.0"]),
        ("*", ["1.4.2"], []),
        (">=3.*", ["3.1.0"], ["2.9"]),
    ],
)
def test_conda_specifier(spec, accepted, rejected):
    specifier = conda_specifier(spec)
    for version in accepted:
        assert specifier.contains(version)
    for version in rejected:
        assert not specifier.contains(version)


def test_conda_specifier_alternatives():
    assert conda_specifier(">=1.2,<1.3|>=1.4") is None


def test_split_requirements():
    reqs = [
        "joblib>=1.2",
        'joblib<1.5; python_version < "3.8"',
        'joblib==1.4.2; extra == "pinned"',
        "joblib-stubs",
        "scikit_learn>=1.0",
    ]
    core, extra = split_requirements(reqs, "joblib")
    assert [str(spec) for spec in core] == [">=1.2"]
    assert [str(spec) for spec in extra] == ["==1.4.2"]
    core, extra = split_requirements(reqs, "scikit-learn")
    assert [str(spec) for spec in core] == [">=1.0"]


def test_requirement_regex():
    # The regex is for RE2, but this subset behaves the same with `re` once
    # the POSIX class is replaced.
    import re

    regex = requirement_regex("scikit-learn").replace("[:space:]", r"\s")
    regex = regex.replace("([[(", r"([\[(")
    assert re.search(regex, "scikit_learn>=1.0")
    assert re.search(regex, "Scikit-Learn")
    assert re.search(regex, "scikit-learn[extra] (>=1.0)")
    assert not re.search(regex, "scikit-learn-intelex>=2024")


def test_classify():
    releases = {Version(v): dt.date(2024, 1, 1) for v in ("1.3.0", "1.4.0", "1.5.0")}

    def dependent(spec, consumer=None, extra_only=False):
        specs = [SpecifierSet(s) for s in spec]
        consumer = consumer and [SpecifierSet(consumer)]
        return Dependent("x", "1", dt.date(2024, 1, 1), specs, extra_only, consumer)

    pinned = dependent(["==1.4.0"], "<1.10")
    capped = dependent([">=1.3,<1.5"], ">=1.0")
    next_capped = dependent(["<1.6"])
    free = dependent([">=1.4"])
    extras = dependent(["<2", "==1.3.0"], extra_only=True)
    deps = [pinned, capped, next_capped, free, extras]
    classify(deps, releases, Version("1.10.0"))

    assert (pinned.kind, pinned.exact, pinned.consumer) == ("capped", True, "excludes")
    assert pinned.max_allowed == pinned.min_allowed == Version("1.4.0")
    assert (capped.kind, capped.exact, capped.consumer) == ("capped", False, "allows")
    assert capped.max_allowed == Version("1.4.0")
    assert next_capped.max_allowed == Version("1.5.0")
    assert not next_capped.allows_next_minor
    assert (free.kind, free.consumer) == ("lower", "none")
    assert free.min_allowed == Version("1.4.0") and free.allows_next_major
    # Only required by extras: the most restrictive one counts.
    assert extras.max_allowed == Version("1.3.0")
