# threadpoolctl

Version constraints that other packages put on [threadpoolctl](https://pypi.org/project/threadpoolctl/). Latest release: 3.8.0 (2026-11-05). Generated on 2026-11-20.

See the [README](README.md) for the method and its limits.

## Which versions of threadpoolctl get installed

Downloads from PyPI over the last 30 days, by series. "From CI" is the share of the downloads made with the `CI` environment variable set, as reported by pip and uv.

| Series | First release | Age (months) | Downloads | Share | Cumulative | From CI |
|---|---|---|---|---|---|---|
| 3.8 | 2026-11-05 | 0 | 44M | 21% | 21% | 27% |
| 3.7 | 2026-09-15 | 2 | 97M | 46% | 67% | 20% |
| 3.6 | 2025-03-13 | 20 | 56M | 27% | 93% | 63% |
| 3.5 | 2024-04-29 | 31 | 4.8M | 2% | 95% | 21% |
| 3.4 | 2024-03-20 | 32 | 172k | 0% | 96% | 17% |
| 3.3 | 2024-02-14 | 33 | 194k | 0% | 96% | 4% |
| Older than 3.3 |  |  | 9.2M | 4% | 100% | 4% |

## What scikit-learn requires

The minimum version of threadpoolctl required by each scikit-learn series, its age when that series was released, and the number of more recent threadpoolctl series that existed then.

| scikit-learn | Released | Requires | Age of the minimum (months) | Newer series available |
|---|---|---|---|---|
| 1.4 | 2024-01-18 | `threadpoolctl>=2.0.0` | 49 | 5 |
| 1.5 | 2024-05-21 | `threadpoolctl>=3.1.0` | 28 | 4 |
| 1.6 | 2024-12-09 | `threadpoolctl>=3.1.0` | 34 | 4 |
| 1.7 | 2025-06-05 | `threadpoolctl>=3.1.0` | 40 | 5 |
| 1.8 | 2025-12-10 | `threadpoolctl>=3.2.0` | 29 | 4 |
| 1.9 | 2026-06-02 | `threadpoolctl>=3.5.0` | 25 | 1 |

## PyPI dependents

1170 projects require threadpoolctl in their latest release ([CSV](data/threadpoolctl-pypi.csv)). Active: latest release less than 12 months ago. Downloads are over the last 30 days.

| Constraint on threadpoolctl | Projects | Active | >= 10k dl |
|---|---|---|---|
| No constraint | 185 | 111 | 23 |
| Lower bound only | 396 | 330 | 34 |
| Upper bound or pin, allows 3.8.0 | 74 | 55 | 6 |
| Excludes 3.8.0 | 515 | 85 | 3 |
| **Total** | 1170 | 581 | 66 |

### What a higher minimum version of threadpoolctl would exclude

Each row counts the projects whose latest release can't be installed with threadpoolctl at or above the given version. The bold column is the one that matters for scikit-learn: projects that accept scikit-learn 1.10.0 (the next minor release) but not this version of threadpoolctl. They would have no solution if scikit-learn 1.10.0 required it (for the ones marked "(extra)", only with that extra). The projects of the last column only conflict when installed next to scikit-learn.

| Minimum threadpoolctl | Projects | Active | >= 10k dl | Exact pins | Also exclude scikit-learn 1.10.0 | **Allow scikit-learn 1.10.0** | No scikit-learn dependency |
|---|---|---|---|---|---|---|---|
| >= 3.3.0 | 279 | 10 | 0 | 276 | 261 | **6** | 12 |
| >= 3.4.0 | 296 | 11 | 0 | 291 | 275 | **7** | 14 |
| >= 3.5.0 | 307 | 13 | 0 | 301 | 286 | **7** | 14 |
| >= 3.6.0 | 407 | 23 | 0 | 401 | 382 | **7** | 18 |
| >= 3.7.0 | 508 | 78 | 2 | 500 | 478 | **9** | 21 |
| >= 3.8.0 | 515 | 85 | 3 | 506 | 483 | **9** | 23 |

Projects that accept scikit-learn 1.10.0 but not threadpoolctl >= 3.8.0:

| Project | Latest release | Downloads (30 d) | From CI | Constraint | On scikit-learn |
|---|---|---|---|---|---|
| [swane](https://pypi.org/project/swane/) | 0.3 (2026-11) | 946 | 0% | `==3.6.0` | `>=1.5.0` |
| [iqm-exa-core](https://pypi.org/project/iqm-exa-core/) | 20.0.0 (2026-11) | 475 | 0% | `==3.6.0` (extra) | `<2,>=1.5.0` |
| [domaps](https://pypi.org/project/domaps/) | 1.1.0 (2025-02) | 130 | 0% | `==3.3.0` (extra) | `any` |
| [clusterlets](https://pypi.org/project/clusterlets/) | 0.0.3 (2025-02) | 124 | 0% | `==3.0.0` | `>=1.0.0` |
| [dorkylever-lama-phenotype-detection](https://pypi.org/project/dorkylever-lama-phenotype-detection/) | 1.0.1 (2022-11) | 114 | 0% | `==3.1.0` | `>=1.0.2` |
| [ohmt](https://pypi.org/project/ohmt/) | 0.0.4 (2024-10) | 86 | 0% | `==3.1.0` | `>=1.0.0` |
| [nehorayrapid1](https://pypi.org/project/nehorayrapid1/) | 0.0.1 (2023-02) | 74 | 0% | `==3.1.0` | `any` |
| [skroute](https://pypi.org/project/skroute/) | 1.0.0a1 (2020-12) | 54 | 0% | `==2.1.0` | `>=0.22.0` |
| [nehorayrapid](https://pypi.org/project/nehorayrapid/) | 0.0.1 (2023-02) | 42 | 0% | `==3.1.0` | `any` |

### Highest threadpoolctl series allowed

For the projects that exclude 3.8.0: the most recent series they accept.

| Series | Projects | Active | >= 10k dl | Exact pins | Range caps |
|---|---|---|---|---|---|
| 3.7 | 7 | 7 | 1 | 6 | 1 |
| 3.6 | 101 | 55 | 2 | 99 | 2 |
| 3.5 | 100 | 10 | 0 | 100 | 0 |
| 3.4 | 11 | 2 | 0 | 10 | 1 |
| 3.3 | 17 | 1 | 0 | 15 | 2 |
| Older than 3.3 | 279 | 10 | 0 | 276 | 3 |

### Caps on the next releases

Projects that accept 3.8.0 but would exclude 3.9.0: 4, of which 4 with an exact pin. Projects that would accept 3.9.0 but exclude 4.0.0: 70.

| Project | Latest release | Downloads (30 d) | From CI | Constraint | On scikit-learn |
|---|---|---|---|---|---|
| [dkist-processing-cryonirsp](https://pypi.org/project/dkist-processing-cryonirsp/) | 4.2.4 (2026-11) | 13k | 13% | `==3.8.0` (extra) | `==1.9.0` |
| [dkist-processing-visp](https://pypi.org/project/dkist-processing-visp/) | 5.13.4 (2026-11) | 12k | 12% | `==3.8.0` (extra) | `==1.6.1` |
| [dkist-processing-trend](https://pypi.org/project/dkist-processing-trend/) | 0.3.4 (2026-11) | 5.6k | 11% | `==3.8.0` (extra) | `==1.9.0` |
| [elicito](https://pypi.org/project/elicito/) | 0.9.0 (2026-11) | 1.3k | 11% | `==3.8.0` (extra) |  |

### Lower bounds

The oldest threadpoolctl series accepted by the projects that have a lower bound (or a pin). The last column is the cumulative share of those projects that require this series or a more recent one.

| Oldest series accepted | Projects | Cumulative |
|---|---|---|
| 3.8 | 8 | 1% |
| 3.7 | 12 | 2% |
| 3.6 | 153 | 18% |
| 3.5 | 167 | 35% |
| 3.4 | 13 | 36% |
| 3.3 | 20 | 38% |
| Older than 3.3 | 610 | 100% |

### Most downloaded dependents

| Project | Latest release | Downloads (30 d) | From CI | Constraint | On scikit-learn |
|---|---|---|---|---|---|
| [scipy](https://pypi.org/project/scipy/) | 1.18.1 (2026-08) | 403M | 29% | `any` (extra) |  |
| [scikit-learn](https://pypi.org/project/scikit-learn/) | 1.9.1 (2026-09) | 217M | 30% | `>=3.5.0` |  |
| [joblib](https://pypi.org/project/joblib/) | 1.6.0 (2026-08) | 203M | 38% | `any` (extra) |  |
| [imbalanced-learn](https://pypi.org/project/imbalanced-learn/) | 0.14.2 (2026-06) | 6.0M | 6% | `<4,>=2.0.0` | `<2,>=1.4.2` |
| [astropy](https://pypi.org/project/astropy/) | 8.0.3 (2026-11) | 4.3M | 24% | `>=3.0.0` (extra) |  |
| [blosc2](https://pypi.org/project/blosc2/) | 4.15.0 (2026-11) | 3.2M | 33% | `any` |  |
| [statsforecast](https://pypi.org/project/statsforecast/) | 2.1.1 (2026-07) | 1.9M | 48% | `>=3` |  |
| [pymc](https://pypi.org/project/pymc/) | 6.4.0 (2026-11) | 1.4M | 50% | `<4.0.0,>=3.1.0` |  |
| [botorch](https://pypi.org/project/botorch/) | 0.18.1 (2026-06) | 639k | 66% | `any` |  |
| [sphinx-gallery](https://pypi.org/project/sphinx-gallery/) | 0.22.1 (2026-09) | 542k | 45% | `any` (extra) |  |
| [mne](https://pypi.org/project/mne/) | 1.13.2 (2026-09) | 534k | 20% | `any` (extra) | `>=1.5` |
| [funasr](https://pypi.org/project/funasr/) | 1.4.27 (2026-11) | 476k | 36% | `>=3.0.0` |  |
| [aider-chat](https://pypi.org/project/aider-chat/) | 0.86.2 (2026-02) | 373k | 28% | `==3.6.0` (extra) | `==1.8.0` |
| [better-optimize](https://pypi.org/project/better-optimize/) | 0.5.1 (2026-10) | 329k | 66% | `any` |  |
| [mdanalysis](https://pypi.org/project/mdanalysis/) | 2.11.0 (2026-10) | 283k | 41% | `any` | `any` |
| [implicit](https://pypi.org/project/implicit/) | 0.7.3 (2026-05) | 264k | 25% | `any` |  |
| [batchgenerators](https://pypi.org/project/batchgenerators/) | 0.25.6 (2026-10) | 175k | 27% | `any` | `any` |
| [ouster-sdk](https://pypi.org/project/ouster-sdk/) | 1.0.1 (2026-08) | 134k | 26% | `>=3.5.0` |  |
| [squidpy](https://pypi.org/project/squidpy/) | 1.8.4 (2026-10) | 127k | 7% | `>=3` | `>=0.24` |
| [filprofiler](https://pypi.org/project/filprofiler/) | 2024.11.2 (2024-11) | 121k | 93% | `any` |  |
| [momwire](https://pypi.org/project/momwire/) | 0.95.0 (2026-11) | 86k | 1% | `>=3` |  |
| [aeon](https://pypi.org/project/aeon/) | 1.6.0 (2026-09) | 76k | 49% | `>=3.2.0` | `<1.10.0,>=1.6.0` |
| [aot-biomaps](https://pypi.org/project/aot-biomaps/) | 2.9.1068 (2026-11) | 60k | 0% | `>=3.0.0` |  |
| [spikeinterface](https://pypi.org/project/spikeinterface/) | 0.106.0 (2026-11) | 51k | 36% | `>=3.0.0` | `any` |
| [pints](https://pypi.org/project/pints/) | 0.6.1 (2026-03) | 50k | 58% | `any` |  |

1145 more, see the CSV file.

## conda-forge dependents

74 conda-forge packages depend on threadpoolctl in their latest build ([CSV](data/threadpoolctl-conda.csv)). Active: latest build less than 12 months ago.

| Constraint on threadpoolctl | Projects | Active |
|---|---|---|
| No constraint | 38 | 33 |
| Lower bound only | 31 | 25 |
| Upper bound or pin, allows 3.8.0 | 3 | 2 |
| Excludes 3.8.0 | 2 | 2 |
| **Total** | 74 | 62 |

### What a higher minimum version of threadpoolctl would exclude

Each row counts the projects whose latest release can't be installed with threadpoolctl at or above the given version. The bold column is the one that matters for scikit-learn: projects that accept scikit-learn 1.10.0 (the next minor release) but not this version of threadpoolctl. They would have no solution if scikit-learn 1.10.0 required it (for the ones marked "(extra)", only with that extra). The projects of the last column only conflict when installed next to scikit-learn.

| Minimum threadpoolctl | Projects | Active | Exact pins | Also exclude scikit-learn 1.10.0 | **Allow scikit-learn 1.10.0** | No scikit-learn dependency |
|---|---|---|---|---|---|---|
| >= 3.3.0 | 0 | 0 | 0 | 0 | **0** | 0 |
| >= 3.4.0 | 1 | 1 | 0 | 0 | **0** | 1 |
| >= 3.5.0 | 1 | 1 | 0 | 0 | **0** | 1 |
| >= 3.6.0 | 1 | 1 | 0 | 0 | **0** | 1 |
| >= 3.7.0 | 2 | 2 | 0 | 1 | **0** | 1 |
| >= 3.8.0 | 2 | 2 | 0 | 1 | **0** | 1 |

### Highest threadpoolctl series allowed

For the projects that exclude 3.8.0: the most recent series they accept.

| Series | Projects | Active | Exact pins | Range caps |
|---|---|---|---|---|
| 3.7 | 0 | 0 | 0 | 0 |
| 3.6 | 1 | 1 | 0 | 1 |
| 3.5 | 0 | 0 | 0 | 0 |
| 3.4 | 0 | 0 | 0 | 0 |
| 3.3 | 1 | 1 | 0 | 1 |
| Older than 3.3 | 0 | 0 | 0 | 0 |

### Caps on the next releases

Projects that accept 3.8.0 but would exclude 3.9.0: 0, of which 0 with an exact pin. Projects that would accept 3.9.0 but exclude 4.0.0: 3.

### Lower bounds

The oldest threadpoolctl series accepted by the projects that have a lower bound (or a pin). The last column is the cumulative share of those projects that require this series or a more recent one.

| Oldest series accepted | Projects | Cumulative |
|---|---|---|
| 3.8 | 0 | 0% |
| 3.7 | 1 | 3% |
| 3.6 | 2 | 9% |
| 3.5 | 2 | 14% |
| 3.4 | 0 | 14% |
| 3.3 | 1 | 17% |
| Older than 3.3 | 29 | 100% |
