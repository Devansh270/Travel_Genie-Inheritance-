import pandas as pd
from pathlib import Path

# Base project directory (avoids hardcoded paths)
BASE_DIR = Path(__file__).resolve().parent.parent

# Countries we want to keep in the dataset
ALLOWED = ["India", "United States", "Iran"]

raw_path = BASE_DIR / "data" / "raw" / "raw_cost.csv"
clean_path = BASE_DIR / "data" / "cleaned" / "cost_cleaned.csv"

df = pd.read_csv(raw_path)

# Normalize column names (lowercase + underscores)
df.columns = (
    df.columns
      .str.strip()
      .str.lower()
      .str.replace(" ", "_")
)

# Keep only selected countries and remove missing values
df = df[df["country"].isin(ALLOWED)]
df = df.dropna()

# Convert cost index into budget category
def budget(cost):
    if cost < 40:
        return "Low"
    elif cost < 70:
        return "Medium"
    else:
        return "High"

df["budget_level"] = df["cost_index"].apply(budget)

# Save cleaned dataset
df.to_csv(clean_path, index=False)

print("Cost cleaned successfully")