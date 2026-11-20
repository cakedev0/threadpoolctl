# Dependents dashboard

Who depends on the packages we maintain, which versions they accept, and what a higher minimum version in a consumer (e.g. scikit-learn) would break. Generated on 2026-11-20 by `build.py`.

| Package | Latest release | PyPI dependents | With upper bound or pin | Exclude the latest release | Exclude the next minor | conda-forge dependents | With upper bound or pin | Exclude the latest release | Exclude the next minor |
|---|---|---|---|---|---|---|---|---|---|
| [joblib](joblib.md) | 1.6.0 (2026-08-31) | 6640 | 1807 | 1239 | 26 | 374 | 23 | 10 | 3 |
| [threadpoolctl](threadpoolctl.md) | 3.8.0 (2026-11-05) | 1170 | 589 | 515 | 4 | 74 | 5 | 2 | 0 |
| [loky](loky.md) | 3.7.0 (2026-09-29) | 84 | 21 | 6 | 2 | 8 | 0 | 0 | 0 |
| [skore](skore.md) | 0.29.1 (2026-11-01) | 5 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |

## How to read the pages

Each page has, for one package (the target):

- **Which versions get installed**: the PyPI downloads of the last 30 days by series, with the share that comes from CI jobs. This tells how many environments still get an old series.
- **What the consumer requires**: the history of the minimum version in the consumer (scikit-learn for joblib and threadpoolctl), and how old it was.
- **Dependents**: the constraint of the latest release of each project that depends on the target, on PyPI and on conda-forge. The main table gives what a higher minimum version would exclude, and separates the projects that also exclude the next consumer release (pinned environments, nothing changes for them) from the ones that accept it (real conflicts).

## Method

- PyPI: PyPI has no reverse dependency index. The candidates are the union of the projects listed by [Wheelodex](https://www.wheelodex.org), of the ones with any release requiring the target in ClickHouse, and of the [15000 most downloaded projects](https://hugovk.github.io/top-pypi-packages/). The first two are incomplete (both miss scikit-learn as a dependent of threadpoolctl), the third one makes sure that no popular project is missed. The requirements of the latest final release of each candidate are then read from the PyPI JSON API. The download counts come from the public ClickHouse instance behind [ClickPy](https://clickpy.clickhouse.com), a copy of the PyPI download logs. The requirements of the latest final release of each candidate are then read from the PyPI JSON API.
- conda-forge: the latest build of each package in `current_repodata.json` (noarch and linux-64).
- Markers are evaluated for CPython 3.13 on Linux x86_64. A project that only requires the target in extras is counted with its most restrictive extra and marked "(extra)".
- "Exclude" means that no released version at or above the given one satisfies the constraint.

## Limits

- Only the latest release of each project is read. A resolver can fall back to an older release, so an excluded project may still install, with an old version of itself.
- The lockfiles and `requirements.txt` of applications are not on PyPI, so they are not counted. Exact pins published on PyPI are a small sample of them.
- Downloads include mirrors and CI jobs. The CI share is only known for the installers that report it (pip and uv), over the last 7 days for dependents.
- conda-forge packages have no download counts here, and repodata patches added after a build are included but `run_constrained` is not.

## Update

```bash
pip install packaging
python build.py joblib:scikit-learn threadpoolctl:scikit-learn loky skore
```

A run takes about 10 minutes (it reads the metadata of ~20000 projects from PyPI) and makes about 30 queries to ClickHouse, whose public user is limited to 60 queries per hour.

