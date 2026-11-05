# Inputs

Four files. Put them here with these exact names, then notebook 01 will run.
Nothing in this folder is committed except this README — see `.gitignore`.

## 1. `households_by_sa2.csv`

**Source:** [Aotearoa Data Explorer](https://explore.data.stats.govt.nz/) → 2023 Census
→ Families and households / Housing → totals by topic for households by SA2.

**Want:** 2013, 2018 and 2023 rows, all SA2s, export as CSV.

Variables to include (level 1 of each classification unless noted):

- Count of households in occupied private dwellings
- Household crowding index (levels 1 and 2)
- Household composition
- Tenure of household
- Sector of landlord *(rented occupied private dwellings only)*
- Total household income, and median total household income
- Weekly rent, and median weekly rent *(rented occupied private dwellings only)*
- Number of motor vehicles
- Access to telecommunication systems
- Number of usual residents, and average number of usual residents

## 2. `individuals_by_sa2.csv`

**Source:** same Explorer, totals by topic for individuals by SA2.

- Census usually resident population count
- Age (5-year groups) and age (life cycle groups), plus median age
- Total personal income age 15+, and median personal income age 15+
- Labour force status
- Highest qualification
- Study participation
- Field of study
- Main means of travel to work

## 3. `sa2_higher_geographies.csv`

**Source:** [Datafinder](https://datafinder.stats.govt.nz/) — "Statistical Area 2
Higher Geographies" (concordance) for the matching year.

One row per SA2, giving SA2 code and name plus SA3, territorial authority and
regional council. Keep the CSV even though you also have the boundary file — a
plain join table is easier to debug than a spatial join.

## 4. `sa2_2023_generalised.gpkg`

**Source:** [Datafinder layer 111227](https://datafinder.stats.govt.nz/layer/111227-statistical-area-2-2023-generalised/)
— SA2 2023 (generalised). Download as GeoPackage.

Use **generalised**, not high-definition: the HD file is very large and the extra
precision changes nothing at this scale. 2,395 SA2s, of which 16 have empty or
null geometry — notebook 01 drops those explicitly and says so.

## Reproducing the download

*[Replace with your actual click path and access date. A reader must be able to
get byte-identical inputs — or at least know why they might not.]*

Example to adapt:

1. Go to Aotearoa Data Explorer, filter to 2023 Census.
2. Search the table title, open it, set geography = Statistical area 2.
3. Export → CSV. Save as `households_by_sa2.csv` here.
4. Repeat for individuals.
5. Datafinder → search "Statistical Area 2 Higher Geographies" → download CSV.
6. Datafinder → layer 111227 → download GeoPackage (generalised).

**Accessed:** [date].

## A note on the licence

Everything above is **CC BY 4.0**, Statistics New Zealand. Reuse is allowed with
credit — state it in the top-level README, which this project does.
