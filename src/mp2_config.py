"""
mp2_config.py 

Setup file that can be edited when names or directories change.


Setup is:
  repo      C:\\Users\\akdux\\dsai-mini-project-2
  data      D:\\dsai\\dsai_projects\\Mini-Project-2-Data
"""

from pathlib import Path

# --- where the raw downloads live (NOT in the repo, they are large) -------
DATA = Path(r"D:\dsai\dsai_projects\Mini-Project-2-Data")

# --- where generated files go (small, inside the repo) -------------------
OUT = Path(__file__).resolve().parent.parent / "outputs"

# --- the exact file names, as they are on disk ----------------------
# These are the long names the Stats NZ download gives them. 
HOUSEHOLDS = DATA / "2023-census-totals-by-topic-for-households-by-statistical-ar.csv"
INDIVIDUALS = DATA / "2023-census-totals-by-topic-for-individuals-by-statistical-a.csv"
LOOKUP_HOUSEHOLDS = DATA / "2023_census_totals_by_topic_for_households_by_sa2_lookup_table.csv"
LOOKUP_INDIVIDUALS = DATA / "2023_census_totals_by_topic_for_individuals_by_sa2_part_1_lookup_table.csv"
BOUNDARIES = DATA / "statistical-area-2-2023-generalised.shp"

# --- the sentinel Stats NZ writes into a suppressed cell -----------------
SUPPRESSED_SENTINEL = -999

NZTM = 2193          # metres. Area and density must be computed in this.
YEAR = 2023
