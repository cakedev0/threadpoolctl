# joblib

Version constraints that other packages put on [joblib](https://pypi.org/project/joblib/). Latest release: 1.6.0 (2026-08-31). Generated on 2026-11-20.

See the [README](README.md) for the method and its limits.

## Which versions of joblib get installed

Downloads from PyPI over the last 30 days, by series. "From CI" is the share of the downloads made with the `CI` environment variable set, as reported by pip and uv.

| Series | First release | Age (months) | Downloads | Share | Cumulative | From CI |
|---|---|---|---|---|---|---|
| 1.6 | 2026-08-31 | 3 | 113M | 56% | 56% | 35% |
| 1.5 | 2025-05-03 | 19 | 75M | 37% | 93% | 54% |
| 1.4 | 2024-04-08 | 31 | 7.9M | 4% | 96% | 27% |
| 1.3 | 2023-06-28 | 41 | 3.9M | 2% | 98% | 19% |
| 1.2 | 2022-09-16 | 50 | 1.6M | 1% | 99% | 14% |
| 1.1 | 2021-10-07 | 61 | 490k | 0% | 99% | 8% |
| Older than 1.1 |  |  | 1.2M | 1% | 100% | 9% |

## What scikit-learn requires

The minimum version of joblib required by each scikit-learn series, its age when that series was released, and the number of more recent joblib series that existed then.

| scikit-learn | Released | Requires | Age of the minimum (months) | Newer series available |
|---|---|---|---|---|
| 1.4 | 2024-01-18 | `joblib>=1.2.0` | 16 | 1 |
| 1.5 | 2024-05-21 | `joblib>=1.2.0` | 20 | 2 |
| 1.6 | 2024-12-09 | `joblib>=1.2.0` | 27 | 2 |
| 1.7 | 2025-06-05 | `joblib>=1.2.0` | 33 | 3 |
| 1.8 | 2025-12-10 | `joblib>=1.3.0` | 29 | 2 |
| 1.9 | 2026-06-02 | `joblib>=1.4.0` | 26 | 1 |

## PyPI dependents

6640 projects require joblib in their latest release ([CSV](data/joblib-pypi.csv)). Active: latest release less than 12 months ago. Downloads are over the last 30 days.

| Constraint on joblib | Projects | Active | >= 10k dl |
|---|---|---|---|
| No constraint | 2282 | 913 | 106 |
| Lower bound only | 2551 | 1718 | 125 |
| Upper bound or pin, allows 1.6.0 | 568 | 274 | 35 |
| Excludes 1.6.0 | 1239 | 232 | 21 |
| **Total** | 6640 | 3137 | 287 |

### What a higher minimum version of joblib would exclude

Each row counts the projects whose latest release can't be installed with joblib at or above the given version. The bold column is the one that matters for scikit-learn: projects that accept scikit-learn 1.10.0 (the next minor release) but not this version of joblib. They would have no solution if scikit-learn 1.10.0 required it (for the ones marked "(extra)", only with that extra). The projects of the last column only conflict when installed next to scikit-learn.

| Minimum joblib | Projects | Active | >= 10k dl | Exact pins | Also exclude scikit-learn 1.10.0 | **Allow scikit-learn 1.10.0** | No scikit-learn dependency |
|---|---|---|---|---|---|---|---|
| >= 1.1.0 | 325 | 2 | 2 | 195 | 245 | **10** | 70 |
| >= 1.2.0 | 447 | 11 | 4 | 304 | 325 | **17** | 105 |
| >= 1.3.0 | 661 | 27 | 7 | 499 | 483 | **27** | 151 |
| >= 1.4.0 | 808 | 49 | 10 | 625 | 575 | **38** | 195 |
| >= 1.5.0 | 1067 | 112 | 14 | 865 | 767 | **47** | 253 |
| >= 1.6.0 | 1239 | 232 | 21 | 1006 | 902 | **49** | 288 |

Projects that accept scikit-learn 1.10.0 but not joblib >= 1.6.0:

| Project | Latest release | Downloads (30 d) | From CI | Constraint | On scikit-learn |
|---|---|---|---|---|---|
| [flaml](https://pypi.org/project/flaml/) | 2.8.0 (2026-11) | 373k | 49% | `<=1.3.2` (extra) | `>=1.0.0; >=1.2.0; any` |
| [pycaret](https://pypi.org/project/pycaret/) | 3.3.2 (2024-04) | 199k | 4% | `<1.4,>=1.2.0` | `>1.4.0` |
| [relevanceai-dev](https://pypi.org/project/relevanceai-dev/) | 3.2.22.2023.1.3.0.10.55.984477 (2023-01) | 21k | 0% | `<1.2.0` | `>=0.20.0` |
| [strable](https://pypi.org/project/strable/) | 0.6.1 (2026-11) | 8.9k | 18% | `<1.6,>=1.3` (extra) | `>=1.6` |
| [merlin-sdk](https://pypi.org/project/merlin-sdk/) | 0.50.0 (2026-04) | 7.0k | 17% | `<1.2.0,>=0.13.0` (extra) | `>=1.1.2` |
| [lingergrn](https://pypi.org/project/lingergrn/) | 1.117 (2026-10) | 3.4k | 0% | `==1.3.2` | `any` |
| [lstchain](https://pypi.org/project/lstchain/) | 0.12.4 (2026-11) | 3.2k | 8% | `~=1.4.0` | `>=1.2` |
| [deeploy](https://pypi.org/project/deeploy/) | 1.67.0 (2026-11) | 2.1k | 13% | `==1.4.2` | `>=0.22.1` |
| [aquariumlearning](https://pypi.org/project/aquariumlearning/) | 1.0.7 (2023-08) | 1.8k | 0% | `==0.17.0` (extra) | `any` |
| [merlin-pyfunc-server](https://pypi.org/project/merlin-pyfunc-server/) | 0.50.0 (2026-04) | 1.5k | 0% | `<1.2.0,>=0.13.0` (extra) | `>=1.1.2` |
| [merlin-batch-predictor](https://pypi.org/project/merlin-batch-predictor/) | 0.50.0 (2026-04) | 1.4k | 0% | `<1.2.0,>=0.13.0` (extra) | `>=1.1.2` |
| [chemsmart](https://pypi.org/project/chemsmart/) | 3.4.10 (2026-11) | 1.4k | 0% | `==1.4.2` | `>=1.6.1` |
| [mat-discover](https://pypi.org/project/mat-discover/) | 2.2.9 (2023-06) | 922 | 0% | `==1.1.0` | `any` |
| [sk-transformers](https://pypi.org/project/sk-transformers/) | 0.11.0 (2023-04) | 786 | 0% | `==1.2.0` | `<2.0.0,>=1.2.0` |
| [akerbp-models](https://pypi.org/project/akerbp-models/) | 1.20220304142108 (2022-03) | 739 | 0% | `==1.0.1` | `>=0.24.2` |
| [nlpia2](https://pypi.org/project/nlpia2/) | 0.2.0 (2025-07) | 486 | 0% | `<1.4,>=1.3.2` | `any` |
| [iqm-exa-core](https://pypi.org/project/iqm-exa-core/) | 20.0.0 (2026-11) | 475 | 0% | `==1.5.3` (extra) | `<2,>=1.5.0` |
| [pycaret-ts-alpha](https://pypi.org/project/pycaret-ts-alpha/) | 3.0.0.dev1649017462 (2022-04) | 461 | 0% | `~=1.0.1` | `>=1.0.2` |
| [thefittest](https://pypi.org/project/thefittest/) | 0.2.7 (2025-09) | 361 | 0% | `==1.2.0` | `>=1.4` |
| [mlmonitor](https://pypi.org/project/mlmonitor/) | 1.0.30 (2025-12) | 291 | 0% | `==1.1.1` (extra) | `<2.0,>=1.3.1` |
| [route-360](https://pypi.org/project/route-360/) | 0.8.14 (2024-11) | 291 | 0% | `==1.4.2` (extra) | `any` |
| [clarifai-evals](https://pypi.org/project/clarifai-evals/) | 0.1.0a10 (2025-07) | 279 | 0% | `==1.4.2` | `any` |
| [artus](https://pypi.org/project/artus/) | 0.3.1 (2023-06) | 273 | 0% | `==1.2.0` | `>=1.2.2` |
| [confectionary](https://pypi.org/project/confectionary/) | 0.3 (2022-10) | 239 | 0% | `==1.2.0` | `any` |
| [mlpet](https://pypi.org/project/mlpet/) | 0.0.7.1 (2021-11) | 220 | 0% | `==1.0.1` | `>=0.24.2` |
| [interprets](https://pypi.org/project/interprets/) | 0.5.0 (2025-01) | 217 | 0% | `==1.4.2` | `any` |
| [evidenceml](https://pypi.org/project/evidenceml/) | 0.32.1 (2026-11) | 211 | 0% | `<1.4.0,>=1.3.2` | `>=1.4.0` |
| [isopeptor](https://pypi.org/project/isopeptor/) | 0.0.80 (2025-06) | 168 | 0% | `==1.4.*` | `>=1.5` |
| [emusort](https://pypi.org/project/emusort/) | 1.1.0 (2026-10) | 166 | 0% | `==1.4.2` (extra) | `>=1.3` |
| [opencortex](https://pypi.org/project/opencortex/) | 0.1.7.post1 (2025-06) | 153 | 0% | `~=1.3.2` | `>=1.5.0` |
| [transport-tools](https://pypi.org/project/transport-tools/) | 0.9.5 (2023-01) | 150 | 0% | `<1.2.0` | `>=0.24.0` |
| [mlio](https://pypi.org/project/mlio/) | 0.9.1 (2018-07) | 146 | 4% | `~=0.11` | `>=0.17` |
| [lookout-style](https://pypi.org/project/lookout-style/) | 0.2.0 (2019-04) | 136 | 0% | `<1.0,>=0.13.2` | `<2.0,>=0.20` |
| [am-lama](https://pypi.org/project/am-lama/) | 0.3.8.3 (2026-04) | 130 | 0% | `<1.3.0` | `>=1.0` |
| [domaps](https://pypi.org/project/domaps/) | 1.1.0 (2025-02) | 130 | 0% | `==1.3.2` (extra) | `any` |
| [packagedquestgenforlambda](https://pypi.org/project/packagedquestgenforlambda/) | 1.0.3 (2022-02) | 126 | 0% | `==0.14.1` | `any` |
| [confnet](https://pypi.org/project/confnet/) | 0.0.3 (2022-11) | 124 | 0% | `==1.2.0` | `any` |
| [wedata-automl](https://pypi.org/project/wedata-automl/) | 0.1.9.post2 (2025-07) | 123 | 0% | `<=1.3.2` | `any` |
| [langchange](https://pypi.org/project/langchange/) | 0.2.0 (2026-07) | 121 | 0% | `<1.3` | `>=1.7` |
| [pycaret-ni](https://pypi.org/project/pycaret-ni/) | 3.4.0 (2025-02) | 95 | 0% | `<1.4,>=1.2.0` | `>1.4.0` |

9 more, see the CSV file.

Projects with >= 10k downloads that exclude joblib 1.6.0 and don't depend on scikit-learn:

| Project | Latest release | Downloads (30 d) | From CI | Constraint | On scikit-learn |
|---|---|---|---|---|---|
| [datasets](https://pypi.org/project/datasets/) | 5.2.0 (2026-11) | 67M | 28% | `<1.3.0` (extra) |  |
| [openhands-ai](https://pypi.org/project/openhands-ai/) | 1.11.0 (2026-07) | 276k | 2% | `==1.5.3` |  |
| [serena-agent](https://pypi.org/project/serena-agent/) | 2.1.0 (2026-10) | 152k | 16% | `==1.5.1` |  |
| [sfctl](https://pypi.org/project/sfctl/) | 11.2.1 (2024-06) | 129k | 0% | `==1.4.2` |  |
| [ethyca-fides](https://pypi.org/project/ethyca-fides/) | 2.86.2 (2026-06) | 24k | 1% | `==1.3.2` |  |
| [ansys-dyna-core](https://pypi.org/project/ansys-dyna-core/) | 0.12.1 (2026-05) | 13k | 66% | `==1.5.3` (extra) |  |
| [ansys-meshing-prime](https://pypi.org/project/ansys-meshing-prime/) | 0.10.5 (2026-10) | 13k | 73% | `==1.5.3` (extra) |  |
| [fudstop](https://pypi.org/project/fudstop/) | 5.9.9 (2024-12) | 13k | 0% | `==1.4.2` |  |

### Highest joblib series allowed

For the projects that exclude 1.6.0: the most recent series they accept.

| Series | Projects | Active | >= 10k dl | Exact pins | Range caps |
|---|---|---|---|---|---|
| 1.5 | 172 | 120 | 7 | 141 | 31 |
| 1.4 | 259 | 63 | 4 | 240 | 19 |
| 1.3 | 147 | 22 | 3 | 126 | 21 |
| 1.2 | 214 | 16 | 3 | 195 | 19 |
| 1.1 | 122 | 9 | 2 | 109 | 13 |
| Older than 1.1 | 324 | 1 | 2 | 194 | 130 |
| No released version | 1 | 1 | 0 | 1 | 0 |

### Caps on the next releases

Projects that accept 1.6.0 but would exclude 1.7.0: 26, of which 20 with an exact pin. Projects that would accept 1.7.0 but exclude 2.0.0: 542.

| Project | Latest release | Downloads (30 d) | From CI | Constraint | On scikit-learn |
|---|---|---|---|---|---|
| [sktime](https://pypi.org/project/sktime/) | 1.3.0 (2026-11) | 689k | 19% | `<1.7,>=1.2.0` | `<1.10.0,>=0.24` |
| [autogluon-common](https://pypi.org/project/autogluon-common/) | 1.6.3 (2026-09) | 410k | 29% | `<1.7,>=1.2` | `<1.10.0,>=1.4.0` |
| [alt-profanity-check](https://pypi.org/project/alt-profanity-check/) | 1.9.1 (2026-09) | 367k | 59% | `==1.6.0` | `==1.9.1` |
| [autogluon-timeseries](https://pypi.org/project/autogluon-timeseries/) | 1.6.3 (2026-09) | 202k | 34% | `<1.7,>=1.2` |  |
| [docassemble-base](https://pypi.org/project/docassemble-base/) | 1.10.15 (2026-10) | 18k | 5% | `==1.6.0` |  |
| [docassemble-webapp](https://pypi.org/project/docassemble-webapp/) | 1.10.15 (2026-10) | 17k | 2% | `==1.6.0` | `==1.9.1` |
| [aindy-runtime](https://pypi.org/project/aindy-runtime/) | 2.40.0 (2026-11) | 17k | 6% | `==1.6.0` |  |
| [dkist-processing-cryonirsp](https://pypi.org/project/dkist-processing-cryonirsp/) | 4.2.4 (2026-11) | 13k | 13% | `==1.6.0` (extra) | `==1.9.0` |
| [dkist-processing-visp](https://pypi.org/project/dkist-processing-visp/) | 5.13.4 (2026-11) | 12k | 12% | `==1.6.0` (extra) | `==1.6.1` |
| [bermuda-ledger](https://pypi.org/project/bermuda-ledger/) | 2.4.2 (2026-10) | 5.8k | 47% | `==1.6.0` (extra) | `==1.9.1` |
| [dkist-processing-trend](https://pypi.org/project/dkist-processing-trend/) | 0.3.4 (2026-11) | 5.6k | 11% | `==1.6.0` (extra) | `==1.9.0` |
| [annif](https://pypi.org/project/annif/) | 1.5.0 (2026-11) | 3.1k | 3% | `~=1.6.0` | `~=1.9.1` |
| [alphadia](https://pypi.org/project/alphadia/) | 2.5.0 (2026-11) | 2.5k | 0% | `==1.6.0` (extra) | `==1.9.1` |
| [concordiahub](https://pypi.org/project/concordiahub/) | 0.3.2 (2026-10) | 2.3k | 0% | `==1.6.0` | `==1.9.1` |
| [tap-readthedocs](https://pypi.org/project/tap-readthedocs/) | 0.8.0 (2026-11) | 1.8k | 2% | `==1.6.0` (extra) |  |
| [dataforge-ml](https://pypi.org/project/dataforge-ml/) | 4.0.0 (2026-10) | 1.6k | 0% | `<1.7,>=1.5` | `<1.10,>=1.9` |
| [cejsp](https://pypi.org/project/cejsp/) | 0.5.0 (2026-10) | 935 | 0% | `==1.6.0` | `==1.9.1` |
| [viewer4a1](https://pypi.org/project/viewer4a1/) | 0.6.0 (2026-11) | 874 | 0% | `==1.6.0` (extra) |  |
| [suffolklitlab-docassemble-base](https://pypi.org/project/suffolklitlab-docassemble-base/) | 1.10.15.post2 (2026-11) | 672 | 0% | `==1.6.0` |  |
| [suffolklitlab-docassemble-webapp](https://pypi.org/project/suffolklitlab-docassemble-webapp/) | 1.10.15.post2 (2026-11) | 665 | 0% | `==1.6.0` | `==1.9.1` |

6 more, see the CSV file.

### Lower bounds

The oldest joblib series accepted by the projects that have a lower bound (or a pin). The last column is the cumulative share of those projects that require this series or a more recent one.

| Oldest series accepted | Projects | Cumulative |
|---|---|---|
| 1.6 | 55 | 1% |
| 1.5 | 491 | 13% |
| 1.4 | 694 | 29% |
| 1.3 | 1019 | 52% |
| 1.2 | 672 | 68% |
| 1.1 | 409 | 77% |
| Older than 1.1 | 998 | 100% |

### Most downloaded dependents

| Project | Latest release | Downloads (30 d) | From CI | Constraint | On scikit-learn |
|---|---|---|---|---|---|
| [scikit-learn](https://pypi.org/project/scikit-learn/) | 1.9.1 (2026-09) | 217M | 30% | `>=1.4.0` |  |
| [datasets](https://pypi.org/project/datasets/) | 5.2.0 (2026-11) | 67M | 28% | `<1.3.0` (extra) |  |
| [nltk](https://pypi.org/project/nltk/) | 3.10.4 (2026-10) | 49M | 45% | `any` | `any` |
| [statsmodels](https://pypi.org/project/statsmodels/) | 0.15.0 (2026-08) | 42M | 26% | `any` (extra) |  |
| [librosa](https://pypi.org/project/librosa/) | 1.0.1 (2026-11) | 11M | 29% | `>=1.2.0` | `>=1.6.0` |
| [pynndescent](https://pypi.org/project/pynndescent/) | 0.7.0 (2026-10) | 7.9M | 67% | `>=0.11` | `>=0.18` |
| [osqp](https://pypi.org/project/osqp/) | 1.1.3 (2026-06) | 6.8M | 46% | `any` |  |
| [imbalanced-learn](https://pypi.org/project/imbalanced-learn/) | 0.14.2 (2026-06) | 6.0M | 6% | `<2,>=1.2.0` | `<2,>=1.4.2` |
| [apache-beam](https://pypi.org/project/apache-beam/) | 2.78.0 (2026-11) | 3.9M | 29% | `>=1.0.1` (extra) | `<1.8.0,>=0.20.0` |
| [pyod](https://pypi.org/project/pyod/) | 3.6.8 (2026-11) | 3.4M | 67% | `>=1.5` | `>=0.22.0` |
| [hdbscan](https://pypi.org/project/hdbscan/) | 0.8.44 (2026-06) | 2.6M | 56% | `>=1.0` | `>=1.6` |
| [phonemizer](https://pypi.org/project/phonemizer/) | 3.6.0 (2026-11) | 2.4M | 23% | `any` |  |
| [pmdarima](https://pypi.org/project/pmdarima/) | 2.1.1 (2025-11) | 1.7M | 12% | `>=0.11` | `>=0.22` |
| [model2vec](https://pypi.org/project/model2vec/) | 0.10.0 (2026-10) | 1.7M | 69% | `any` | `any` |
| [sacremoses](https://pypi.org/project/sacremoses/) | 0.2.0 (2026-08) | 1.6M | 17% | `>=1.2.0` |  |
| [speechbrain](https://pypi.org/project/speechbrain/) | 1.1.2 (2026-10) | 1.6M | 32% | `>=0.14.1` |  |
| [resiliparse](https://pypi.org/project/resiliparse/) | 2.0.1 (2026-11) | 1.5M | 11% | `any` (extra) |  |
| [singer-sdk](https://pypi.org/project/singer-sdk/) | 0.54.9 (2026-10) | 1.4M | 5% | `>=1.3.0` |  |
| [kedro-datasets](https://pypi.org/project/kedro-datasets/) | 10.0.0 (2026-11) | 1.3M | 17% | `>=0.14` (extra) | `<2,>=1.0.2; >=1.0.2` |
| [scanpy](https://pypi.org/project/scanpy/) | 1.13.0 (2026-11) | 1.3M | 28% | `any` | `>=1.6` |
| [paddlex](https://pypi.org/project/paddlex/) | 3.7.2 (2026-06) | 1.2M | 26% | `any` (extra) | `any` |
| [phonemizer-fork](https://pypi.org/project/phonemizer-fork/) | 3.3.2 (2025-01) | 1.2M | 34% | `any` |  |
| [music21](https://pypi.org/project/music21/) | 10.5.2 (2026-10) | 1.1M | 9% | `any` |  |
| [recordlinkage](https://pypi.org/project/recordlinkage/) | 0.16 (2023-07) | 1.1M | 4% | `any` | `>=1` |
| [pymoo](https://pypi.org/project/pymoo/) | 0.6.2 (2026-06) | 1.0M | 69% | `any` (extra) | `any` |

6615 more, see the CSV file.

## conda-forge dependents

374 conda-forge packages depend on joblib in their latest build ([CSV](data/joblib-conda.csv)). Active: latest build less than 12 months ago.

| Constraint on joblib | Projects | Active |
|---|---|---|
| No constraint | 201 | 110 |
| Lower bound only | 150 | 109 |
| Upper bound or pin, allows 1.6.0 | 13 | 11 |
| Excludes 1.6.0 | 10 | 6 |
| **Total** | 374 | 236 |

### What a higher minimum version of joblib would exclude

Each row counts the projects whose latest release can't be installed with joblib at or above the given version. The bold column is the one that matters for scikit-learn: projects that accept scikit-learn 1.10.0 (the next minor release) but not this version of joblib. They would have no solution if scikit-learn 1.10.0 required it (for the ones marked "(extra)", only with that extra). The projects of the last column only conflict when installed next to scikit-learn.

| Minimum joblib | Projects | Active | Exact pins | Also exclude scikit-learn 1.10.0 | **Allow scikit-learn 1.10.0** | No scikit-learn dependency |
|---|---|---|---|---|---|---|
| >= 1.1.0 | 2 | 0 | 1 | 0 | **0** | 2 |
| >= 1.2.0 | 3 | 0 | 2 | 0 | **1** | 2 |
| >= 1.3.0 | 3 | 0 | 2 | 0 | **1** | 2 |
| >= 1.4.0 | 5 | 1 | 2 | 0 | **2** | 3 |
| >= 1.5.0 | 8 | 4 | 3 | 1 | **3** | 4 |
| >= 1.6.0 | 10 | 6 | 3 | 3 | **3** | 4 |

Projects that accept scikit-learn 1.10.0 but not joblib >= 1.6.0:

| Project | Latest release | Constraint | On scikit-learn |
|---|---|---|---|
| [lstchain](https://anaconda.org/conda-forge/lstchain) | 0.12.3 (2026-07) | `<1.5.dev0,>=1.4.0` | `<2.dev0,>=1.2` |
| [morphometrics](https://anaconda.org/conda-forge/morphometrics) | 0.0.8 (2023-11) | `==1.1.0` | `>=0.24.2` |
| [pycaret](https://anaconda.org/conda-forge/pycaret) | 3.3.2 (2025-01) | `<1.4,>=1.2.0` | `>1.4.0` |

### Highest joblib series allowed

For the projects that exclude 1.6.0: the most recent series they accept.

| Series | Projects | Active | Exact pins | Range caps |
|---|---|---|---|---|
| 1.5 | 2 | 2 | 0 | 2 |
| 1.4 | 3 | 3 | 1 | 2 |
| 1.3 | 2 | 1 | 0 | 2 |
| 1.2 | 0 | 0 | 0 | 0 |
| 1.1 | 1 | 0 | 1 | 0 |
| Older than 1.1 | 2 | 0 | 1 | 1 |

### Caps on the next releases

Projects that accept 1.6.0 but would exclude 1.7.0: 3, of which 1 with an exact pin. Projects that would accept 1.7.0 but exclude 2.0.0: 10.

| Project | Latest release | Constraint | On scikit-learn |
|---|---|---|---|
| [alt-profanity-check](https://anaconda.org/conda-forge/alt-profanity-check) | 1.9.1 (2026-09) | `==1.6.0` | `==1.9.1` |
| [autogluon.common](https://anaconda.org/conda-forge/autogluon.common) | 1.6.2 (2026-09) | `<1.7,>=1.2` | `<1.10.0,>=1.4.0` |
| [autogluon.timeseries](https://anaconda.org/conda-forge/autogluon.timeseries) | 1.6.2 (2026-09) | `<1.7,>=1.2` |  |

### Lower bounds

The oldest joblib series accepted by the projects that have a lower bound (or a pin). The last column is the cumulative share of those projects that require this series or a more recent one.

| Oldest series accepted | Projects | Cumulative |
|---|---|---|
| 1.6 | 2 | 1% |
| 1.5 | 17 | 11% |
| 1.4 | 31 | 29% |
| 1.3 | 28 | 45% |
| 1.2 | 28 | 61% |
| 1.1 | 15 | 70% |
| Older than 1.1 | 52 | 100% |
