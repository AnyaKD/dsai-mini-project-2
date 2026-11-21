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
#####
#
# README sections — Results, Findings, Limitations

*Drafted from the numbers the notebooks produce. Anything in [square brackets]
is a value I could not read from your run output — fill it from
`outputs/model_meta.json` and the test-scores cell of 04.*

---

## Results

### The target

Crowding is Stats NZ's household crowding index at SA2 level, collapsed to a
binary outcome. **Crowded** means one or more bedrooms needed under the Canadian
National Occupancy Standard — the `crowded` aggregate, which equals its two
"bedrooms needed" components to within base-3 rounding (validated in notebook 01:
residual +42).

The denominator is `total_stated`, the households that gave a usable answer.
Dividing by `total` would include non-response and understate the rate wherever
non-response is higher.

**The threshold is the top quartile of the area crowding rate — ≥ 0.0775
(7.75%).** That gives a positive class of **572 SA2s, a base rate of 25.06%.**
A national-average cut would leave roughly 6% positives and make recall
uninformative; the quartile also matches what the client does with the result —
rank areas for assessment rather than label them.

Predicting the majority class every time scores **74.9% accuracy and 0.00 recall
on the crowded class.** That is the benchmark every figure below is read against.

### Suppression

Suppression is not missing-at-random and it sets the boundary of what the model
can see.

| | |
|---|---|
| Suppressed or non-applicable cells | **31,010** across the measure columns |
| SA2s that lose the crowding rate entirely | **112** |
| Mean suppressed cells, areas retained | **2.7** |
| Mean suppressed cells, areas dropped | **221.1** |
| Correlation, suppression vs crowding rate | **0.116** |

The 112 dropped areas are excluded from the model. They are systematically the
small ones — which is a statement about who the census can describe, not just a
data-cleaning footnote.

Two numeric sentinels were found and mapped to missing: `-999` for a suppressed
cell and `-997` for a category not collected. `-999` was caught by notebook 01's
reconciliation check, which summed the crowding index to a negative total.
`-997` was caught in notebook 02, in a column whose every value was the sentinel —
which is why a missing-value count reported zero for it.

### The ranking is noisy at the top

| SA2 | Crowded | Households | Rate |
|---|---|---|---|
| Fiordland | 3 | 3 | 1.000 |
| Islands Thames-Coromandel District | 3 | 3 | 1.000 |
| Takanini Industrial | 3 | 6 | 0.500 |
| Ōtara West | 243 | 612 | 0.397 |

The two highest rates come from three households each, and they outrank Ōtara
West at 612 households. Treating SA2s as equally-weighted units biases any
ordering toward tiny areas, so a **minimum size floor of 50 households** is
applied before a ranking is used. SA2s under 20 households: **21**; under 50:
**51**; under 100: **82**.

### What predicts crowding

| Feature | n | R² |
|---|---|---|
| Households paying under $200 weekly rent | 2,230 | **0.3293** |
| Households with no motor vehicle | 2,274 | **0.0245** |

One rent bracket explains about a third of the variance in area crowding rate.
The direction is as expected and the strength is the strongest single signal in
the data.

**Read this cautiously.** A low-rent share sits close to a restatement of
crowding — the same circularity that made household composition and household
size ineligible as features. Part of that 0.329 is definition rather than
prediction, which is why the model is not carried by any one variable.

### Clustering

K-Means on the scaled socio-economic profile. **50 numeric features** — the
income, rent, tenure, landlord, motor-vehicle and telecommunications bracket
**shares** — with the suppression count excluded from the matrix.

`k = 5`, chosen as a working partition. Cluster sizes:

| Cluster | n | Name |
|---|---|---|
| 0 | 684 | Mainstream mixed-tenure suburbs |
| 1 | 400 | Low-rent owner-occupied |
| 2 | 406 | Lower-income, one-car households |
| 3 | 552 | High-income, high-rent |
| 4 | 353 | State and social housing |

**How well-separated are they?** The silhouette peaks at **k = 2 (0.175)** and
declines from there, with no elbow in the inertia curve. Both point to the
socio-economic profile varying along a gradient rather than falling into
distinct groups. The five clusters are reported as a working partition that
gives interpretable, mappable groups — not as a discovered natural structure.

### Classification

One scikit-learn `Pipeline` throughout, so imputation and scaling refit inside
every fold. Stratified 75/25 split, seed 42. Models compared: logistic baseline,
KNN, random forest.

**Random forest chosen**, on cross-validated recall with PR-AUC as tie-breaker.

| Metric | Value |
|---|---|
| Recall, crowded class | **0.7762** (±0.0219 across 5 folds) |
| PR-AUC | **0.8736** |
| ROC-AUC | **0.9417** |
| Accuracy | **0.8820** |
| Base rate | 0.25 |

Hyperparameters tuned on PR-AUC rather than accuracy, because the client ranks
areas rather than labelling them.

**Held-out test scores** — [paste from 04's test-scores cell]:

| Feature set | Recall | Precision | PR-AUC | ROC-AUC | Accuracy |
|---|---|---|---|---|---|
| area profile | [ ] | [ ] | [ ] | [ ] | [ ] |
| + cluster label | [ ] | [ ] | [ ] | [ ] | [ ] |

### The boundaries comparison — not run

The ARI/AMI comparison between the data-driven clusters and the administrative
geographies is **not answered in this project.** It needs a link from SA2 up to
territorial authority and regional council:

- the territorial-authority shapefile holds 68 polygons and carries no SA2 reference
- the SA2 shapefile carries the SA2 code and no higher geography
- no concordance table was present in the inputs

This is the brief's second question, so it is named as a scope limitation rather
than left as a stub. The fix is one file — the Stats NZ "Statistical Area 2
Higher Geographies" table from Datafinder — joined on the SA2 code. It is a
plain CSV join with no geometry, and runs in seconds once present.

---

## Findings from model CHOICE = forest

**1. The census profile does carry signal about crowding.** A random forest on
50 socio-economic area variables found **77.6% of crowded areas** against a
25% base rate, with PR-AUC 0.874. The result is stable across folds (±0.022), so
it is not an artefact of one split. Area-level monitoring of crowding is
plausible on this evidence.

**2. The best single predictor is a rent bracket, and that is partly circular.**
Households paying under $200 weekly rent explain **R² = 0.329** of the variance
in crowding rate — far more than any other variable. But rent and crowding are
close to stating the same fact twice, so this is evidence that the profile
carries signal, not that rent causes crowding.

**3. The clustering found a public-housing concentration without being asked to.**
Tenure was not a target; the clusters were built from the whole profile. Cluster
4 — **353 SA2s, about 15% of the country** — has a Kāinga Ora tenancy share of
**0.228 against a national 0.070**, more than three times the rate. That is a
need-assessment shortlist derived from census data rather than drawn boundaries.

**4. But the areas form a gradient, not distinct groups.** The silhouette peaks
at k = 2 and declines; the inertia curve has no elbow. A partition of the country
into N kinds of place is a convenience for reporting, not a fact the data
supports. Any boundary — administrative or data-driven — cuts through a
continuum.

**5. The ranking needs a size floor before it is usable.** Two areas score 100%
crowding from three households each. For a client who prioritises by ordering,
that ordering is actively misleading without a minimum household count.

**6. Suppression defines who the analysis describes.** 112 SA2s lose the
crowding rate entirely, averaging 221 suppressed cells against 2.7 for retained
areas. The model describes the areas where the census can be published, and
those are systematically the larger ones.

---

## Limitations from model CHOICE = forest


An honest list is a strength here, not a confession.

**Ecological fallacy — the leading limitation.** An SA2's socio-economic
profile says nothing about any individual household in it. The model describes
areas. It cannot be read as a statement about a person or a family, and no
result here identifies which households are crowded. This is the caveat the
work should be read with first.

**The target is a construct, not a measurement.** The crowding index is derived
from household composition against a bedroom requirement. It is a definition,
and a different definition would give different numbers.

**Circularity.** Rent, income and tenure sit close to the definition of crowding.
The association between them and the target is not independent evidence, and the
0.329 R² on the low-rent bracket is partly restatement. Household composition
and household size were excluded from the feature set for exactly this reason —
crowding is defined as composition against a bedroom requirement — and their
contribution was tested separately rather than folded in.

**Suppression is not missing-at-random.** Counts are fixed-random-rounded to base
3, and sensitive cells are suppressed. Suppression concentrates in small areas —
221 cells per dropped area against 2.7 for retained — so it biases the result
toward large urban SA2s and the model is blind to the areas it cannot see.

**Small areas distort the rate.** An SA2 with 9 households and one crowded
household shows 11.1%; move that household and it is 0% or 22%. A minimum size
floor of 50 households is applied, but areas just above the floor remain noisy.

**The clusters are not a natural classification.** The silhouette peaks at
k = 2 (0.175) and declines, which is weak structure by any conventional reading.
Low values describe a continuum, and the five clusters should not be treated as
discrete kinds of place.

**One point in time, and the instrument is being replaced.** The 2023 Census is a
single snapshot — and the last full field-enumeration census New Zealand will
take. The next moves to 2030 under an admin-data-first model, and household
crowding is derived from household composition, which administrative data does
not capture the way a census form does. Any monitoring built on this baseline
needs a stated plan for that transition rather than an assumption of a routine
refresh.

**No causal claim.** Every association reported here is observed in one census
snapshot. Nothing in this work is evidence that income or rent causes crowding,
and nothing here predicts it.

**The boundaries question is unanswered.** The comparison against regional
council and territorial authority did not run — see Results. Evidence either way
was a deliverable, and a null result would have been useful; neither was
produced.

## Conclusions
## Conclusions

### 1. Model Selection & Class-Imbalance Context
- **Cross-validated performance:** Tuning achieved a best cross-validated PR-AUC of **`0.8767`** across `1712` training SA2s and `571` held-out test SA2s.
- **Imbalanced target baseline:** Positive (crowded) SA2 base rates are **`0.2506`** in train and **`0.2504`** in test (~25% positive). Because a majority-class dummy predictor achieves ~75% accuracy with **zero recall** on crowded SA2s, held-out evaluation focuses on `pr_auc`, `roc_auc`, `recall_pos`, `precision_pos`, `f1_pos`, and confusion counts (`tp`, `fn`, `fp`, `tn`).

### 2. Held-Out Test Results by Feature Set
| Feature Set | PR-AUC | Δ PR-AUC | Recall (+) | Precision (+) | F1 (+) | ROC-AUC | TP | TN |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `area profile` | `0.8633` | baseline | `0.8531` | `0.7305` | `0.7871` | `0.9298` | — | `383` |
| `+ cluster` | `0.8656` | `+0.0023` | `0.8462` | `0.7246` | `0.7806` | `0.9319` | `121` | `382` |
| `+ TA` | `0.8826` | `+0.0193` | `0.8252` | `0.7516` | `0.7867` | `0.9457` | `118` | `389` |
| `+ cluster + TA` | `0.8829` | `+0.0196` | `0.8252` | `0.7516` | `0.7867` | `0.9459` | `118` | `389` |

- **Key takeaway:** Territorial Authority (`+ TA`) provides the main test lift (`+0.0193` PR-AUC and `+0.0159` ROC-AUC over `area profile`), trading a small recall dip (`0.8531` to `0.8252`) for higher precision (`0.7305` to `0.7516`) and fewer false positives (`389` vs. `383` true negatives). Adding `cluster` on top of `+ TA` (`+ cluster + TA`) changes PR-AUC by only `+0.0003` (`0.8829` vs. `0.8826`).

### 3. Clusters vs. Territorial Authority Boundaries
- K-Means cluster labels show low-to-moderate agreement with `ta_name` (**ARI = `0.1007`**, **NMI = `0.1755`**; regional council is not in the input frame), indicating that unsupervised clusters capture cross-boundary housing and area profiles rather than simply reproducing territorial boundaries.