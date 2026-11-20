# loky

Version constraints that other packages put on [loky](https://pypi.org/project/loky/). Latest release: 3.7.0 (2026-09-29). Generated on 2026-11-20.

See the [README](README.md) for the method and its limits.

## Which versions of loky get installed

Downloads from PyPI over the last 30 days, by series. "From CI" is the share of the downloads made with the `CI` environment variable set, as reported by pip and uv.

| Series | First release | Age (months) | Downloads | Share | Cumulative | From CI |
|---|---|---|---|---|---|---|
| 3.7 | 2026-09-29 | 2 | 1.3M | 50% | 50% | 31% |
| 3.6 | 2026-08-31 | 3 | 197k | 7% | 57% | 88% |
| 3.5 | 2025-03-14 | 20 | 1.1M | 41% | 98% | 28% |
| 3.4 | 2023-04-14 | 43 | 48k | 2% | 100% | 3% |
| 3.3 | 2022-09-15 | 50 | 220 | 0% | 100% | 8% |
| 3.2 | 2022-09-14 | 50 | 47 | 0% | 100% | 0% |
| Older than 3.2 |  |  | 5.9k | 0% | 100% | 6% |

## PyPI dependents

84 projects require loky in their latest release ([CSV](data/loky-pypi.csv)). Active: latest release less than 12 months ago. Downloads are over the last 30 days.

| Constraint on loky | Projects | Active | >= 10k dl |
|---|---|---|---|
| No constraint | 36 | 18 | 2 |
| Lower bound only | 27 | 22 | 2 |
| Upper bound or pin, allows 3.7.0 | 15 | 8 | 1 |
| Excludes 3.7.0 | 6 | 3 | 0 |
| **Total** | 84 | 51 | 5 |

### What a higher minimum version of loky would exclude

Each row counts the projects whose latest release can't be installed with loky at or above the given version.

| Minimum loky | Projects | Active | >= 10k dl | Exact pins |
|---|---|---|---|---|
| >= 3.2.0 | 3 | 1 | 0 | 0 |
| >= 3.3.0 | 3 | 1 | 0 | 0 |
| >= 3.4.0 | 3 | 1 | 0 | 0 |
| >= 3.5.0 | 6 | 3 | 0 | 1 |
| >= 3.6.0 | 6 | 3 | 0 | 1 |
| >= 3.7.0 | 6 | 3 | 0 | 1 |

### Highest loky series allowed

For the projects that exclude 3.7.0: the most recent series they accept.

| Series | Projects | Active | >= 10k dl | Exact pins | Range caps |
|---|---|---|---|---|---|
| 3.6 | 0 | 0 | 0 | 0 | 0 |
| 3.5 | 0 | 0 | 0 | 0 | 0 |
| 3.4 | 3 | 2 | 0 | 1 | 2 |
| 3.3 | 0 | 0 | 0 | 0 | 0 |
| 3.2 | 0 | 0 | 0 | 0 | 0 |
| Older than 3.2 | 3 | 1 | 0 | 0 | 3 |

### Caps on the next releases

Projects that accept 3.7.0 but would exclude 3.8.0: 2, of which 1 with an exact pin. Projects that would accept 3.8.0 but exclude 4.0.0: 13.

| Project | Latest release | Downloads (30 d) | From CI | Constraint |
|---|---|---|---|---|
| [pivot](https://pypi.org/project/pivot/) | 0.11.0 (2026-11) | 297k | 86% | `<3.8,>=3.5.6` |
| [py-asyncutils](https://pypi.org/project/py-asyncutils/) | 1.3.7 (2026-11) | 2.0k | 0% | `==3.7.0` (extra) |

### Lower bounds

The oldest loky series accepted by the projects that have a lower bound (or a pin). The last column is the cumulative share of those projects that require this series or a more recent one.

| Oldest series accepted | Projects | Cumulative |
|---|---|---|
| 3.7 | 3 | 6% |
| 3.6 | 0 | 6% |
| 3.5 | 13 | 33% |
| 3.4 | 15 | 65% |
| 3.3 | 0 | 65% |
| 3.2 | 0 | 65% |
| Older than 3.2 | 17 | 100% |

### Most downloaded dependents

| Project | Latest release | Downloads (30 d) | From CI | Constraint |
|---|---|---|---|---|
| [qutip](https://pypi.org/project/qutip/) | 5.3.1 (2026-08) | 340k | 50% | `any` (extra) |
| [pivot](https://pypi.org/project/pivot/) | 0.11.0 (2026-11) | 297k | 86% | `<3.8,>=3.5.6` |
| [coffea](https://pypi.org/project/coffea/) | 2026.11.0 (2026-11) | 78k | 2% | `>=3.5.6` |
| [adaptive](https://pypi.org/project/adaptive/) | 1.5.2 (2026-06) | 23k | 58% | `>=2.9` |
| [adaptive-scheduler](https://pypi.org/project/adaptive-scheduler/) | 2.17.2 (2026-06) | 10k | 3% | `any` |
| [scinexus](https://pypi.org/project/scinexus/) | 2026.10.26 (2026-10) | 8.2k | 58% | `any` (extra) |
| [flowfile](https://pypi.org/project/flowfile/) | 0.24.3 (2026-11) | 8.0k | 0% | `<3.5.0,>=3.4.1` |
| [ms-flow](https://pypi.org/project/ms-flow/) | 0.12.0 (2026-11) | 7.2k | 0% | `>=3.0` |
| [prediction-market-agent-tooling](https://pypi.org/project/prediction-market-agent-tooling/) | 0.69.40 (2026-04) | 6.3k | 0% | `<4.0.0,>=3.4.1` |
| [extra-data](https://pypi.org/project/extra-data/) | 1.25.0 (2026-10) | 5.7k | 10% | `any` |
| [mxlpy](https://pypi.org/project/mxlpy/) | 0.73.0 (2026-11) | 5.5k | 1% | `>=3.4` |
| [cheutils](https://pypi.org/project/cheutils/) | 2.8.23 (2025-09) | 4.7k | 0% | `any` |
| [glow](https://pypi.org/project/glow/) | 0.16.17 (2026-11) | 3.2k | 0% | `~=3.1` |
| [yenwealth](https://pypi.org/project/yenwealth/) | 0.7.0 (2026-11) | 3.1k | 0% | `>=3.5.2` |
| [qb-cubie](https://pypi.org/project/qb-cubie/) | 0.0.9 (2026-11) | 2.9k | 0% | `<4,>=3.7` |
| [chemfit](https://pypi.org/project/chemfit/) | 4.0.0 (2026-10) | 2.9k | 92% | `any` (extra) |
| [serum-render](https://pypi.org/project/serum-render/) | 0.7.1 (2026-11) | 2.7k | 0% | `any` |
| [pytask-parallel](https://pypi.org/project/pytask-parallel/) | 0.5.5 (2026-08) | 2.5k | 2% | `any` |
| [cocos](https://pypi.org/project/cocos/) | 0.3.1 (2026-10) | 2.5k | 1% | `>=3.4` |
| [canvodpy](https://pypi.org/project/canvodpy/) | 1.1.0 (2026-11) | 2.4k | 31% | `>=3.5.6` |
| [febid](https://pypi.org/project/febid/) | 0.11.0 (2026-03) | 2.1k | 0% | `~=3.4.1` |
| [bionic](https://pypi.org/project/bionic/) | 0.11.1 (2022-11) | 2.0k | 1% | `any` (extra) |
| [multifutures](https://pypi.org/project/multifutures/) | 0.3.2 (2024-04) | 2.0k | 5% | `any` (extra) |
| [py-asyncutils](https://pypi.org/project/py-asyncutils/) | 1.3.7 (2026-11) | 2.0k | 0% | `==3.7.0` (extra) |
| [lilac](https://pypi.org/project/lilac/) | 0.3.9 (2024-02) | 1.9k | 3% | `<4.0.0,>=3.4.1` |

59 more, see the CSV file.

## conda-forge dependents

8 conda-forge packages depend on loky in their latest build ([CSV](data/loky-conda.csv)). Active: latest build less than 12 months ago.

| Constraint on loky | Projects | Active |
|---|---|---|
| No constraint | 6 | 4 |
| Lower bound only | 2 | 2 |
| Upper bound or pin, allows 3.7.0 | 0 | 0 |
| Excludes 3.7.0 | 0 | 0 |
| **Total** | 8 | 6 |

No project puts an upper bound on loky.
