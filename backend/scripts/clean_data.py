import pandas as pd

# =========================
# CONFIG
# =========================
INPUT_CSV = "data/cleaned/final_dataset.csv"
OUTPUT_CSV = "data/cleaned/final_dataset_clean.csv"

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(INPUT_CSV)

print("Original rows:", len(df))

# =========================
# NORMALIZE COLUMNS
# =========================
df.columns = df.columns.str.strip().str.lower()

# Ensure required columns exist
required_cols = ["city", "place_name", "description", "category", "budget"]
for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"Missing required column: {col}")

# Normalize text data
for col in ["city", "place_name", "description", "category", "budget"]:
    df[col] = df[col].astype(str).str.strip().str.lower()

# =========================
# CLEANING RULE
# =========================
# Rule:
# Keep a row ONLY if the city name appears in either:
# - description
# - place_name
def is_valid_row(row):
    city = row["city"]
    return (city in row["description"]) or (city in row["place_name"])

clean_df = df[df.apply(is_valid_row, axis=1)]

print("After city validation:", len(clean_df))

# =========================
# OPTIONAL: REMOVE DUPLICATES
# =========================
clean_df = clean_df.drop_duplicates(
    subset=["city", "place_name"], keep="first"
)

print("After removing duplicates:", len(clean_df))

# =========================
# SAVE CLEAN DATA
# =========================
clean_df.to_csv(OUTPUT_CSV, index=False)

print(f"\n✅ Cleaned dataset saved to: {OUTPUT_CSV}")
