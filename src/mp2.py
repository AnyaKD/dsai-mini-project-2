"""
Shared helpers for Mini Project 2 — SA2 census clustering and classification.

Import from a notebook with:

    import sys; sys.path.append("../src")
    import mp2

Everything here is mechanical: paths, loading, cleaning, the SA2 join,
the concordance attach, geometry, and feature-frame construction.
The analysis lives in the notebooks.
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

HOUSEHOLDS = DATA / "households_by_sa2.csv"
INDIVIDUALS = DATA / "individuals_by_sa2.csv"
CONCORDANCE = DATA / "sa2_higher_geographies.csv"
BOUNDARIES = DATA / "sa2_2023_generalised.gpkg"

# New Zealand Transverse Mercator — metres. Use this for any area,
# length or density calculation. Never compute area in EPSG:4326.
NZTM = 2193

CENSUS_YEAR = 2023


# --------------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------------

def load_raw(path: Path, **kwargs) -> pd.DataFrame:
    """Read a Stats NZ export. Tries UTF-8 then the common Windows encoding."""
    if not path.exists():
        raise FileNotFoundError(
            f"{path.name} not found. See data/README.md for what to download "
            f"and what to call it."
        )
    for enc in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            return pd.read_csv(path, encoding=enc, **kwargs)
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError(f"Could not decode {path.name} with any known encoding.")


def snapshot(df: pd.DataFrame, name: str = "dataframe") -> None:
    """Print the shape, dtypes and head — run this after every load."""
    print(f"{name}: {df.shape[0]:,} rows x {df.shape[1]:,} columns")
    print("-" * 60)
    print(df.dtypes.to_string())
    print("-" * 60)
    print(df.head().to_string())
    print()


# Stats NZ exports hide blanks as sentinel strings.
# Note: "Confidential" is suppression, not a zero, and not NaN. Keep the
# distinction — collapsing it into either one loses information you need.
NA_TOKENS = {"", "..", "...", "c", "C", "-", "n/a", "N/A", "na", "NA", "null", "Null"}
SUPPRESSED = {"confidential", "Confidential", "CONFIDENTIAL", "suppressed", "s"}


def read_measure(series: pd.Series) -> pd.Series:
    """
    Coerce a Stats NZ measure column to float, keeping suppression visible.

    Returns floats where a number exists, and NaN everywhere else. Codes
    suppression separately with `flag_suppressed` before calling this, if you
    need to distinguish it.
    """
    s = series.astype(str).str.strip()
    s = s.str.replace(",", "", regex=False)          # thousands separators
    s = s.str.replace(r"^\$", "", regex=True)        # leading $ on money columns
    s = s.str.replace(r"[%]$", "", regex=True)       # trailing %
    s = s.where(~s.isin(NA_TOKENS))                  # sentinels -> NaN
    return pd.to_numeric(s, errors="coerce")


def flag_suppressed(series: pd.Series) -> pd.Series:
    """True where a cell is suppressed (marked 'confidential'), not merely blank."""
    return series.astype(str).str.strip().str.lower().isin(
        {t.lower() for t in SUPPRESSED}
    )


# --------------------------------------------------------------------------
# Area codes and names
# --------------------------------------------------------------------------

SA2_CODE_RE = re.compile(r"^\s*(\d{6,7})\s*$")


def tidy_area_code(series: pd.Series) -> pd.Series:
    """
    Extract a bare numeric area code from a Stats NZ area label.

    Stats NZ writes areas as '1234567 Area Name' or '1234567.0'. This pulls
    the digits out and zero-pads to 7, matching the boundary file's SA2_code.
    """
    s = series.astype(str)
    digits = s.str.extract(r"(\d{4,8})", expand=False)
    return digits.str.zfill(7)


def tidy_area_name(series: pd.Series) -> pd.Series:
    """Strip the leading code and whitespace from an area label."""
    s = series.astype(str).str.strip()
    return s.str.replace(SA2_CODE_RE, "", regex=True).str.strip()


# --------------------------------------------------------------------------
# Assembly
# --------------------------------------------------------------------------

def assemble(households: pd.DataFrame, individuals: pd.DataFrame,
             concordance: pd.DataFrame,
             year: int = CENSUS_YEAR) -> pd.DataFrame:
    """
    Join the three non-spatial inputs into one analysis frame, one row per SA2.

    You will need to adapt the column-name arguments here to whatever your
    actual exports use — the Explorer renames columns per table. Print the
    columns of each input first and map them explicitly rather than guessing.
    """
    hh = households.copy()
    ind = individuals.copy()
    conc = concordance.copy()

    hh["sa2_code"] = tidy_area_code(hh["Year and area"])       # <- adapt
    ind["sa2_code"] = tidy_area_code(ind["Year and area"])     # <- adapt
    conc["sa2_code"] = tidy_area_code(conc["SA2_code"])        # <- adapt

    hh = hh[hh["Year and area"].astype(str).str.contains(str(year))]
    ind = ind[ind["Year and area"].astype(str).str.contains(str(year))]

    frame = hh.merge(
        ind.drop(columns=[c for c in ind.columns
                          if c.startswith("Census") or c == "Year and area"]),
        on="sa2_code", how="inner", validate="one_to_one",
    )
    frame = frame.merge(
        conc[["sa2_code", "SA2_name", "SA3_name",
              "Territorial_authority_name", "Regional_council_name"]],
        on="sa2_code", how="left", validate="one_to_one",
    )
    return frame


def attach_geometry(frame: pd.DataFrame,
                    boundaries_path: Path = BOUNDARIES,
                    code_column: str = "SA2_code") -> "pd.DataFrame":
    """
    Attach SA2 polygons, project to NZTM, and compute area and density.

    Requires geopandas. Returns a GeoDataFrame in EPSG:2193.

    The 16 SA2s with no digitised geometry are dropped here, and the count is
    printed — do not let them through silently.
    """
    import geopandas as gpd

    gdf = gpd.read_file(boundaries_path)
    if gdf.crs is None:
        raise ValueError("Boundary file has no CRS. Set it before projecting.")

    n_before = len(gdf)
    gdf = gdf[gdf.geometry.notna() & ~gdf.geometry.is_empty].copy()
    print(f"Dropped {n_before - len(gdf)} SA2s with null or empty geometry "
          f"({len(gdf):,} of {n_before:,} remain).")

    if gdf.crs.to_epsg() != NZTM:
        gdf = gdf.to_crs(epsg=NZTM)
        print(f"Projected to NZTM2000 (EPSG:{NZTM}) — metres, so area is real.")

    gdf["area_km2"] = gdf.geometry.area / 1e6

    gdf["sa2_code"] = tidy_area_code(gdf[code_column])
    out = gdf[["sa2_code", "area_km2", "geometry"]].merge(
        frame, on="sa2_code", how="inner", validate="one_to_one",
    )
    out = gpd.GeoDataFrame(out, geometry="geometry", crs=gdf.crs)

    if "usual_residents" in out.columns:
        out["density_per_km2"] = np.where(
            out["area_km2"] > 0, out["usual_residents"] / out["area_km2"], np.nan
        )
        print("Computed density_per_km2 from usual_residents.")

    print(f"Analysis frame: {len(out):,} SA2s with geometry.")
    return out


# --------------------------------------------------------------------------
# Suppression diagnostics
# --------------------------------------------------------------------------

def suppression_report(df: pd.DataFrame, columns: list[str] | None = None) -> pd.DataFrame:
    """
    Per-column suppression summary — the Module 2 work that matters here.

    Suppression is not missing-at-random: it concentrates in small areas.
    Report it rather than dropping it quietly.
    """
    cols = columns or [c for c in df.columns if df[c].isna().any()]
    rows = []
    for c in cols:
        n_missing = int(df[c].isna().sum())
        rows.append({
            "column": c,
            "missing": n_missing,
            "missing_pct": round(100 * n_missing / len(df), 2),
            "n_unique": int(df[c].nunique(dropna=True)),
        })
    out = pd.DataFrame(rows).sort_values("missing_pct", ascending=False)
    print(f"{len(out)} columns have missing values; "
          f"{len(out[out.missing_pct > 0])} of them are worth a look.")
    return out


def suppressed_share(df: pd.DataFrame) -> pd.Series:
    """Share of values in each row that are suppressed or missing."""
    numeric = df.select_dtypes(include=[np.number])
    if numeric.empty:
        return pd.Series(dtype=float)
    return numeric.isna().mean(axis=1)


# --------------------------------------------------------------------------
# Feature frames
# --------------------------------------------------------------------------

def split_features(df: pd.DataFrame, target: str,
                   drop: list[str] | None = None
                   ) -> tuple[pd.DataFrame, pd.Series, list[str], list[str]]:
    """
    Split into X, y and the numeric / categorical column lists a
    ColumnTransformer needs.

    Drops identifier and leakage columns. Keep this list explicit and
    commented — the only columns that should disappear are ones you can
    justify in the README.
    """
    leaky = drop or []
    id_cols = {"sa2_code", "SA2_name", "SA3_name",
               "Territorial_authority_name", "Regional_council_name",
               "geometry", "cluster", "cluster_kproto"}

    X = df.drop(columns=[c for c in [target, *leaky] if c in df.columns])
    X = X.drop(columns=[c for c in id_cols if c in X.columns])
    y = df[target]

    num_cols = X.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = [c for c in X.columns if c not in num_cols]
    return X, y, num_cols, cat_cols


def make_preprocessor(num_cols: list[str], cat_cols: list[str]):
    """
    ColumnTransformer: median-impute and scale numerics, one-hot categoricals.

    Median imputation is a defensible default for suppressed counts, but say
    in the README that you chose it and why.
    """
    from sklearn.compose import ColumnTransformer
    from sklearn.impute import SimpleImputer
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler

    numeric = Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
    ])
    categorical = Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])
    return ColumnTransformer([
        ("num", numeric, num_cols),
        ("cat", categorical, cat_cols),
    ])


# --------------------------------------------------------------------------
# Clustering
# --------------------------------------------------------------------------

def cluster_diagnostics(X_scaled: np.ndarray, k_range=range(2, 13),
                        seed: int = 42) -> pd.DataFrame:
    """
    Elbow (inertia) and silhouette across k. The scatter in silhouette is
    often more useful than the argmax — read it, do not just take the max.
    """
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score

    rows = []
    for k in k_range:
        km = KMeans(n_clusters=k, n_init=10, random_state=seed)
        labels = km.fit_predict(X_scaled)
        sil = silhouette_score(X_scaled, labels) if len(set(labels)) > 1 else np.nan
        rows.append({"k": k, "inertia": km.inertia_, "silhouette": sil})
    out = pd.DataFrame(rows)
    print(out.to_string(index=False))
    return out


def cluster_label_frame(df: pd.DataFrame, labels: np.ndarray,
                        column: str = "cluster") -> pd.DataFrame:
    """Attach cluster labels back onto the frame without mutating the input."""
    out = df.copy()
    out[column] = labels
    return out


def compare_to_admin(df: pd.DataFrame, cluster_col: str, admin_col: str) -> dict:
    """
    ARI and AMI between a data-driven clustering and an administrative geography.

    This is the quantitative answer to 'do natural groupings beat the drawn
    ones?' — and the number the README reports.
    """
    from sklearn.metrics import adjusted_mutual_info_score, adjusted_rand_score

    mask = df[admin_col].notna() & df[cluster_col].notna()
    a = df.loc[mask, cluster_col]
    b = df.loc[mask, admin_col]
    result = {
        "cluster_col": cluster_col,
        "admin_col": admin_col,
        "n": int(mask.sum()),
        "ari": round(adjusted_rand_score(b, a), 4),
        "ami": round(adjusted_mutual_info_score(b, a), 4),
    }
    print(result)
    return result


# --------------------------------------------------------------------------
# Classification
# --------------------------------------------------------------------------

def build_models(seed: int = 42) -> dict:
    """
    Candidate estimators, all intended to sit behind one preprocessor.
    Keys are what you print; swap or extend freely.
    """
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.neighbors import KNeighborsClassifier

    return {
        "logistic": LogisticRegression(
            max_iter=2000, class_weight="balanced", random_state=seed,
        ),
        "knn": KNeighborsClassifier(n_neighbors=5),
        "forest": RandomForestClassifier(
            n_estimators=400, min_samples_leaf=2,
            class_weight="balanced", n_jobs=-1, random_state=seed,
        ),
    }


def evaluate(model, X_test, y_test, threshold: float = 0.5) -> dict:
    """
    Recall and PR-AUC on the positive class, which is the costly error here.

    PR-AUC rather than ROC-AUC because the positive class is the minority;
    ROC flatters a rare-class model. Accuracy is reported but is not the
    decision metric — the base rate is printed alongside it so the reader can
    see what 'predicting the majority class' would already score.
    """
    from sklearn.metrics import (
        accuracy_score, average_precision_score, confusion_matrix,
        f1_score, precision_score, recall_score, roc_auc_score,
    )

    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(X_test)[:, 1]
    else:
        proba = model.decision_function(X_test)
    pred = (proba >= threshold).astype(int)

    cm = confusion_matrix(y_test, pred)
    return {
        "recall_pos": round(recall_score(y_test, pred, zero_division=0), 4),
        "precision_pos": round(precision_score(y_test, pred, zero_division=0), 4),
        "f1_pos": round(f1_score(y_test, pred, zero_division=0), 4),
        "pr_auc": round(average_precision_score(y_test, proba), 4),
        "roc_auc": round(roc_auc_score(y_test, proba), 4),
        "accuracy": round(accuracy_score(y_test, pred), 4),
        "base_rate": round(float(np.mean(y_test)), 4),
        "tn": int(cm[0, 0]), "fp": int(cm[0, 1]),
        "fn": int(cm[1, 0]), "tp": int(cm[1, 1]),
    }


def positive_rate_report(y: pd.Series, target_name: str = "target") -> None:
    """Always print the base rate before celebrating any accuracy score."""
    rate = float(np.mean(y))
    print(f"{target_name}: positive class = {rate:.2%} "
          f"({int(y.sum()):,} of {len(y):,})")
    print(f"A model that predicts the majority class every time scores "
          f"{max(rate, 1 - rate):.2%} accuracy and 0.00 recall on the "
          f"minority class.")
