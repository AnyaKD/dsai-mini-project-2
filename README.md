# Can a small area's profile predict how crowded its households are?

**Mini Project 2** — Data Science & AI course
*Anya Duxfield · github - AnyaKD · November 2026*

---

## The client and their question

**Commissioned by:** Kāinga Ora — Homes and Communities (Housing Supply &
Evidence). New Zealand's public housing agency.

**The policy customer:** the **Ministry for Cities, Environment, Regions and
Transport (MCERT)** — established in 2026, absorbing the former Ministry of
Housing and Urban Development along with the Ministry for the Environment, the
Ministry of Transport and local government functions from DIA. Housing policy
now sits inside that larger ministry.

**The question as it reached me**, third hand, in one line:

> "Can the census tell us where the crowded households are, in areas small enough
> to act on?"

A real brief arrives about that thin. Turning it into something answerable is the
first piece of the job — the four blanks are the unit of analysis, the outcome,
the benchmark to beat, and the decision it informs. Full brief, the people
involved, and why the second half of the question matters to them:
**[`CLIENT_BRIEF.md`](CLIENT_BRIEF.md)**.

**The question I actually answered**, written down before touching the data:

> Can the socio-economic and housing profile of a small area tell us how crowded
> its households are — and do the natural groupings of small areas outperform the
> standard administrative ones at that job?

Two halves. First, cluster New Zealand's statistical area 2 (SA2) geographies on
their census profile. Second, predict a household-level crowding outcome from the
area profile, and test whether adding the cluster label beats using regional
council or territorial authority instead.

The second half exists because of the client's own framing: their planning and
reporting are organised around administrative boundaries, and they have no
evidence those boundaries group areas that are actually alike.

## Why it matters

Crowding is associated with respiratory illness, rheumatic fever and poor
educational outcomes, and it is one of the measures housing policy is judged on.
If area-level census variables carry real signal, then crowding can be monitored
where a direct measurement is not available. If the natural groupings of areas
carry more signal than administrative boundaries do, that is a finding about how
we draw the areas — not just about the model.

**What the client does with it.** Two decisions:

1. *Where to prioritise need assessment.* A ranked list of SA2s, not a
   yes/no. They care about the ordering, which is why the metric is recall and
   PR-AUC rather than accuracy.
2. *Whether to keep planning against administrative boundaries.* Evidence either
   way is useful — a weak ARI justifies revisiting the boundaries, a strong one
   justifies leaving them alone. A null result is a deliverable here.

**The asymmetry that sets the metric.** For this client a false negative is a
crowded household that never appears on an assessment list. A false positive is
an assessor visiting a household that turns out fine. The costly error runs
    opposite to how it usually does, and the metric choice follows from that rather
    than from convention.

## Data

All from **Stats NZ**, 2023 Census. No registration, no paid access.

**Why 2023 and not something more recent.** There was no 2025 census. In June
2025 the Government announced the end of the five-yearly field enumeration: the
next census moves from 2028 to **2030** and the model changes to **admin
data-first**, with administrative data as the backbone and an annual Census
Attributes Survey — from 2027, sampling a few percent of the population — filling
the gaps. October 2025 was a field *test* of that survey in three centres, not
used to produce official statistics. So 2023 is the most recent census, and the
last of its kind.

That matters here specifically: household crowding is derived from household
composition against a bedroom requirement, which is questionnaire-shaped
information that admin data does not capture the same way. See
[`CLIENT_BRIEF.md`](CLIENT_BRIEF.md) for the full reasoning and sources.

*Current position, not settled fact:* the 2030 date and the admin-first model
come from the Data and Statistics (Census) Amendment Bill. Reporting through 2026
noted contingency work as that legislation progressed, so the timeline could
still move.

| Dataset | Source | Geography | Licence |
|---|---|---|---|
| Households totals by topic | [Aotearoa Data Explorer](https://explore.data.stats.govt.nz/) | SA2, 2013 / 2018 / 2023 | CC BY 4.0 |
| Individuals totals by topic | [Aotearoa Data Explorer](https://explore.data.stats.govt.nz/) | SA2, 2013 / 2018 / 2023 | CC BY 4.0 |
| SA2 higher geographies (concordance) | [Datafinder](https://datafinder.stats.govt.nz/) | SA2 → SA3, TA, RC | CC BY 4.0 |
| SA2 2023 boundaries (generalised) | [Datafinder](https://datafinder.stats.govt.nz/layer/111227-statistical-area-2-2023-generalised/) | SA2 polygons | CC BY 4.0 |

> Stats NZ data reused under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
> Adapted from 2023 Census data, Statistics New Zealand.
> Holland, [access date].

**How to reproduce the download.** [Exact click path through Aotearoa Data
Explorer, and which file you saved where.] Replace this line with the real steps
— a reader must be able to get the same inputs.

## Method

### 1. Assembly

SA2-level household and individual tables are joined on the SA2 code, then the
concordance is left-joined to attach the administrative hierarchy. Geometry is
loaded from the generalised SA2 boundary file and projected to **NZTM2000
(EPSG:2193)** so that area and density are computed in real metres, not degrees.

### 2. Clustering

- K-Means on the scaled continuous features, with the number of clusters chosen
  from the elbow curve and the silhouette score.
- K-Prototypes on the mixed numeric/categorical frame, so categorical variables
  are kept rather than dummy-encoded away.
- Clusters interpreted in plain language, and cross-tabulated against regional
  council and urban/rural.
- **Adjusted Rand Index** and **Adjusted Mutual Information** quantify how far the
  data-driven clusters agree with the administrative boundaries.

### 3. Classification

One scikit-learn `Pipeline` throughout (`ColumnTransformer` → scaler / one-hot →
estimator), so every step is inside cross-validation:

| Model | Role |
|---|---|
| `LogisticRegression` | interpretable baseline |
| `KNeighborsClassifier` | non-parametric comparison |
| `RandomForestClassifier` | ensemble, with feature importance |
| `SVC` | optional, if time allows |

**Metric, chosen from the cost of errors.** A false negative — a crowded household
the model misses — is the costly error here, because the response it would trigger
is support, not a penalty. So the headline metric is **recall on the crowded
class**, reported alongside **PR-AUC** rather than ROC-AUC, since the positive
class is the minority. Accuracy is reported for completeness and is not the
decision metric.

Two comparisons are reported: **models** (baseline → ensemble) and **features**
(area profile alone vs area profile plus cluster label vs administrative area).

## Results

*[Fill in from `05_conclusions.ipynb` output. Do not type these from memory.]*

| Model | Features | Recall (crowded) | PR-AUC | ROC-AUC |
|---|---|---|---|---|
| Logistic regression | area profile | | | |
| Random forest | area profile | | | |
| Random forest | + cluster label | | | |
| Random forest | + administrative area | | | |

Base rate (predicting the majority class throughout): **__**

Headline: *[one sentence — the number, and what it means in plain terms]*

ARI between K-Means clusters and regional council: **__**
ARI between K-Means clusters and territorial authority: **__**

## Findings

*[Three to five bullets. Each one a sentence a non-specialist can act on, with the
number that supports it.]*

## Limitations

An honest list is a strength here, not a confession.

- **Ecological fallacy.** An SA2's profile does not determine any individual
  household's crowding. The model describes areas, and cannot be read as a
  statement about a person or a family. This is the most important caveat in the
  project.
- **The target is a construct, not a measurement.** The crowding index is derived
  from household composition against a bedroom requirement. It is a definition, and
  a different definition would give different numbers.
- **Suppression.** Counts are fixed random rounded to base 3, and sensitive cells
  below six are suppressed. Suppression is not missing-at-random — it concentrates
  in small areas, which biases the clustering toward large urban SA2s.
- **Circularity.** Area-level income and tenure partly define what "crowded" means
  in the same census. The association is not independent evidence.
- **One point in time, and a measurement instrument being replaced.** The 2023
  Census is a single snapshot — and the last full enumeration census New Zealand
  will take. The next census moves to 2030 under an admin-data-first model, so
  this baseline cannot be refreshed on the same basis. Crowding is derived from
  household composition, which admin data does not capture as a census form does.
  Any monitoring built on this needs a stated plan for that transition. Details
  and sources in [`CLIENT_BRIEF.md`](CLIENT_BRIEF.md).
- **The relationship is not causal.** The associations are observed in one
  snapshot; nothing here is evidence that income causes crowding, and nothing here
  predicts it.
- **Comparison across years.** The crowding methodology changed for 2023 — it now
  uses gender rather than sex — so 2013/2018 comparisons need that caveat.

## What I would do next

*[Two or three concrete next steps, e.g. repeat the clustering at SA1 to test
robustness, add external administrative data such as regional house prices, or
validate against a held-out census year.]*

## Repository layout

```
.
├── README.md
├── requirements.txt
├── src/
│   └── mp2.py               # shared loaders, geometry and feature helpers
├── data/                    # downloaded inputs (see data/README.md)
└── notebooks/
    ├── 01_data_assembly.ipynb
    ├── 02_eda.ipynb
    ├── 03_clustering.ipynb
    ├── 04_classification.ipynb
    └── 05_conclusions.ipynb
```

## Running it

**conda-first, deliberately.** `geopandas` needs GDAL, GEOS and PROJ, and pip
wheels for those are built against whatever versions were current when each
package was uploaded. Install them from conda-forge instead and the three solve
together as a set. `requirements.txt` lists the same versions for reference, but
conda is the supported route.

```bash
# 1. Create the project environment from conda-forge
conda create -n mp2 -c conda-forge python=3.11 \
    geopandas fiona shapely pyproj \
    pandas numpy scikit-learn kmodes matplotlib jupyterlab -y

conda activate mp2
```

```bash
# 2. Register the kernel, so Jupyter offers it by name
python -m ipykernel install --user --name mp2 --display-name "Python (mp2)"
```

```bash
# 3. Place the four inputs in data/, then launch from the project root
#    (not from notebooks/ — the notebooks import from ../src)
jupyter lab --notebook-dir=.
```

Then **select the kernel explicitly** in each notebook: *Kernel → Change Kernel →
Python (mp2)*. A Jupyter started from your base environment offers a base kernel
by default, and `import geopandas` fails there even though it works in `mp2`.
Switch all five; the stubs do not pin one.

Run the notebooks in order, `01` through `05`. Each runs top to bottom on a fresh
clone with no errors.

### Two things that will cost you an hour if you skip them

**Do not reuse an existing course environment.** If you have a `dsai` environment
from the course materials, leave it alone. Installing `geopandas` and `kmodes`
into it can pull the GDAL stack out from under a lab, and you would be debugging
that the week an assessment is due. The `mp2` environment above costs nothing and
keeps the course environment clean.

**Launch Jupyter from the project root.** The notebook stubs open with
`sys.path.append("../src")` so they can `import mp2`. Started from `notebooks/`,
that path does not resolve. Either launch from the project root as above, or
change the line to match wherever you actually start Jupyter.

### If you would rather use pip

Works on Colab and on most Linux and macOS machines:

```bash
pip install -r requirements.txt
```

Commit the `pip freeze` output if you go this way, so the environment is pinned
exactly. On Windows, use conda — the pip path is genuinely painful there.

## Licence and attribution

Code in this repository: [your choice — MIT is fine].

Census data: **CC BY 4.0**, Statistics New Zealand. Attribution as above. SA2
boundary geometry is redistributed here under the same licence; check Stats NZ's
current terms before republishing derived boundary files.
