# ===========================================================================
# CELL A — feature selection, for the END of notebook 02
#
# Replaces the commented-out "TODO: persist the feature choices" block.
# Writes outputs/feature_spec.json in the shape notebooks 03/04/05 already read:
#
#     spec["numeric"]  spec["categorical"]  spec["target"]  spec["leaky_or_id"]
#
# Three decisions are encoded here, each justified in the markdown above it.
# ===========================================================================

import json
import numpy as np
import pandas as pd

# Confirm the sentinel fix actually landed before building features on it.
mp2.assert_no_sentinels(df)

# ---------------------------------------------------------------------------
# 1. The three exclusions
# ---------------------------------------------------------------------------

# (a) The target itself. Every crowding index column, plus the four derived
#     columns 01 wrote. Including any of these would leak the answer.
TARGET_PREFIX = "household_crowding_index_"
DERIVED_TARGET = {"crowded_count", "crowding_base", "crowding_rate",
                  "crowded_top_quartile", "crowded_n"}

# (b) The outcome restated. Crowding is household composition measured against
#     a bedroom requirement, so household size and composition ARE the target
#     expressed differently. The brief asks whether the area's *profile* can
#     stand in for a direct measurement; feeding in the measurement defeats it.
#     Held out of the primary feature set and used once as a sensitivity run.
DEFINITION_PREFIXES = (
    "household_composition_",
    "number_of_usual_residents_in_household_",
    "count_of_households_in_occupied_private_dwellings",
)

# ---------------------------------------------------------------------------
# 2. Bracket families, converted to shares of their own stated total
# ---------------------------------------------------------------------------
# A raw count bracket is large in any big suburb regardless of composition.
# Dividing by the stated total turns "how many households" into "what share of
# households", which is what makes the clustering reflect composition rather
# than area size. The denominator is used and then dropped.

SHARE_FAMILIES = {
    "total_household_income": "total_household_income_total_stated",
    "weekly_rent_paid_by_household": "weekly_rent_paid_by_household_total_stated",
    "sector_of_landlord": "sector_of_landlord_total_stated",
    "tenure_of_household": "tenure_of_household_total_stated",
    "number_of_motor_vehicles": "number_of_motor_vehicles_total_stated",
    "access_to_telecommunication_systems_total_responses":
        "access_to_telecommunication_systems_total_responses_total_stated",
}

# Dropped after use. Denominators are scale variables; medians are derived from
# the same brackets; "not stated" and "not elsewhere included" are non-response
# and residual buckets, not socio-economic profile.
DROP_SUFFIXES = ("_total_stated", "_total", "_median",
                 "_not_stated", "_not_elsewhere_included", "_unidentifiable",
                 "_average")


def _is_denominator(col):
    return col in SHARE_FAMILIES.values()


def _share_denominator(col):
    """The stated total this bracket belongs to, or None if it is not a bracket."""
    if _is_denominator(col):
        return None
    for prefix, denom in SHARE_FAMILIES.items():
        if col.startswith(prefix + "_"):
            return denom
    return None


def _excluded(col):
    if col.startswith(TARGET_PREFIX) or col in DERIVED_TARGET:
        return "target"
    if any(col.startswith(p) for p in DEFINITION_PREFIXES):
        return "definition"
    return None


# ---------------------------------------------------------------------------
# 3. Classify every column in the frame
# ---------------------------------------------------------------------------

measure_cols = [c for c in df.columns
                if c not in ("sa2_code", "sa2_name")
                and pd.api.types.is_numeric_dtype(df[c])]

rows = []
for c in measure_cols:
    why = _excluded(c)
    if why:
        rows.append({"column": c, "role": why})
        continue
    denom = _share_denominator(c)
    if denom is not None:
        rows.append({"column": c, "role": "share", "denominator": denom})
    elif c.endswith(DROP_SUFFIXES):
        rows.append({"column": c, "role": "denominator"})
    else:
        rows.append({"column": c, "role": "keep"})

roles = pd.DataFrame(rows)
print(roles["role"].value_counts().to_string())
print()

# ---------------------------------------------------------------------------
# 4. Build the share columns, then select the feature list
# ---------------------------------------------------------------------------

share_rows = roles[roles["role"] == "share"]
for _, r in share_rows.iterrows():
    col, denom = r["column"], r["denominator"]
    if denom not in df.columns:
        raise KeyError(f"{col!r} expects denominator {denom!r}, which is not in the frame")
    df[f"{col}_share"] = (df[col] / df[denom].replace(0, np.nan)).astype("float64")

NUMERIC = (list(roles.loc[roles["role"] == "keep", "column"])
           + [f"{c}_share" for c in share_rows["column"]])

# ---------------------------------------------------------------------------
# 5. Categoricals — attached by the spatial cell below, or already present
# ---------------------------------------------------------------------------

CATEGORICAL = [c for c in df.columns if not pd.api.types.is_numeric_dtype(df[c])
               and c not in ("sa2_name",)]

# ---------------------------------------------------------------------------
# 6. Verify before writing: nothing leaky, nothing degenerate
# ---------------------------------------------------------------------------

leaked = [c for c in NUMERIC + CATEGORICAL
          if c.startswith(TARGET_PREFIX) or c in DERIVED_TARGET
          or any(c.startswith(p) for p in DEFINITION_PREFIXES)]
assert not leaked, f"excluded columns reached the feature list: {leaked}"

# A share column that is entirely missing is a column to drop, not to impute.
all_missing = [c for c in NUMERIC if df[c].isna().all()]
assert not all_missing, f"feature columns with no observed values: {all_missing}"

# The shares of a family should sum to ~1 where the denominator is present.
for prefix, denom in SHARE_FAMILIES.items():
    fam = [c for c in NUMERIC if c.startswith(prefix + "_") and c.endswith("_share")]
    if not fam:
        continue
    total = df.loc[df[denom].notna(), fam].sum(axis=1, min_count=1)
    print(f"{prefix:58s} n={len(fam):2d}  "
          f"share sum  median {total.median():.3f}  "
          f"p05 {total.quantile(0.05):.3f}  p95 {total.quantile(0.95):.3f}")

# ---------------------------------------------------------------------------
# 7. Write the spec
# ---------------------------------------------------------------------------

spec = {
    "numeric": NUMERIC,
    "categorical": CATEGORICAL,
    "target": "crowded_top_quartile",
    "leaky_or_id": sorted(set(
        [c for c in df.columns if c.startswith(TARGET_PREFIX)]
        + list(DERIVED_TARGET)
        + ["sa2_code", "sa2_name", "geometry"]
        + [c for c in df.columns if any(c.startswith(p) for p in DEFINITION_PREFIXES)]
    )),
    "definition_only": [c for c in df.columns
                        if any(c.startswith(p) for p in DEFINITION_PREFIXES)],
    "share_denominators": SHARE_FAMILIES,
    "target_cohort": "crowded_top_quartile",
    "n_rows": int(len(df)),
    "n_numeric": len(NUMERIC),
    "n_categorical": len(CATEGORICAL),
}

(mp2.OUT / "feature_spec.json").write_text(json.dumps(spec, indent=2))

print()
print(f"numeric features     : {len(NUMERIC)}")
print(f"categorical features : {len(CATEGORICAL)}  {CATEGORICAL}")
print(f"excluded as target   : {len([c for c in spec['leaky_or_id'] if c.startswith(TARGET_PREFIX)])}")
print(f"excluded as definition: {len(spec['definition_only'])}")
print()
print("written:", mp2.OUT / "feature_spec.json")
print()
print("numeric feature list:")
for i, c in enumerate(NUMERIC, 1):
    print(f"  {i:2d}. {c}")
