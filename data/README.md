# Inputs

Place the expected source files in this folder using the exact filenames/patterns below so Notebooks `01` and `03` can run from raw inputs. Nothing in this directory is committed to Git except this `README.md` (see `.gitignore`).
Provided to Google Classroom upload for MiniProject 2 a zipped folder that is all the data for this project.
## 1. `2023-census-totals-by-topic-for-households-by-statistical-ar.csv`

**Source:** [Aotearoa Data Explorer](https://datafinder.stats.govt.nz/layer/120892-2023-census-totals-by-topic-for-households-by-statistical-area-2/) → 2023 Census → Families and households / Housing → totals by topic for households by SA2.

**Want:** All SA2s exported as CSV (including household crowding, housing, income, and rent variables used in the project).

Key variables included:
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

## 2. `2023_census_totals_by_topic_for-households_by_sa2_lookup_table.csv`

**Source:** Stats NZ — 2023 Census household topic SA2 lookup table (matching the SA2 household totals dataset).

Used to map and validate SA2 codes/labels alongside the household topic table.

## 3. `statistical-area-2-2023-generalised.shp` *(and sidecar files: `.shx`, `.dbf`, `.prj`, `.cpg`)*

**Source:** [Stats NZ Datafinder — Statistical Area 2 (2023 Generalised)](https://datafinder.stats.govt.nz/layer/111194-territorial-authority-2023-generalised/) (clipped would have been a better choice as Auckland is a Unitary Authority and therefore includes near shore waters in it boundary).

Use **generalised** boundaries rather than high-definition files to keep file sizes manageable and spatial operations fast at national SA2 scale.

## 4. `territorial-authority-2023-generalised.shp` *(and sidecar files: `.shx`, `.dbf`, `.prj`, `.cpg`)*

**Source:** [Territorial Authority 2023 (generalised)](https://datafinder.stats.govt.nz/layer/111194-territorial-authority-2023-generalised/) 
(clipped would have been a better choice.) 

Used in Notebook `03` (`sorted(DATA.glob("*territorial-authority*.shp"))`) to resolve `ta_name` for SA2s and evaluate cluster alignment against territorial authorities (note: regional council is not included in the input frame).

## Reproducing the Download

1. Open [Aotearoa Data Explorer](https://explore.data.stats.govt.nz/) and select **2023 Census** household topic data by Statistical Area 2, exporting as CSV (`2023-census-totals-by-topic-for-households-by-statistical-ar.csv`) along with the matching SA2 lookup table (`2023_census_totals_by_topic_for-households_by_sa2_lookup_table.csv`).
2. Download the **Statistical Area 2 (2023 Generalised)** boundary layer (`statistical-area-2-2023-generalised.shp` and sidecar files) from Stats NZ Datafinder.
3. Download the **Territorial Authority** boundary shapefile (`*territorial-authority*.shp` and sidecar files) from Stats NZ Datafinder.
4. Place all files in this folder (`DATA`) before running Notebooks `01`–`04`. *(Pre-computed outputs in `outputs/` allow `05_conclusions.ipynb` to run even when raw inputs are absent.)*

**Accessed:** [Insert access date, e.g., November 2026].

## Licence & Attribution

Underlying datasets and geographic boundaries are sourced from **Statistics New Zealand (Stats NZ)** under **CC BY 4.0**. Reuse is permitted with appropriate attribution, as noted in the root `README.md`.