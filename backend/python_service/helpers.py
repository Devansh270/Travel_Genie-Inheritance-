import re
import os
import pandas as pd

# ---------- Dataset Path ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned", "final_dataset_clean.csv")

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(
        f"Dataset not found at: {DATA_PATH}\n"
        "Make sure final_dataset_clean.csv exists inside python_service/data/cleaned/"
    )

df = pd.read_csv(DATA_PATH)
df.columns = df.columns.str.strip().str.lower()

for col in ["place_name", "description", "category", "budget"]:
    df[col] = df[col].astype(str).str.lower()


# ---------- Extraction ----------
def extract_city(q):
    m = re.search(r"(trip to|visit|to)\s+([a-z\s]+)", q.lower())
    return m.group(2).strip() if m else None


def extract_days(q):
    m = re.search(r"(\d+)\s*day", q.lower())
    return int(m.group(1)) if m else 3


def extract_budget(q):
    q = q.lower()
    if "low" in q or "cheap" in q:
        return "low"
    if "high" in q or "luxury" in q:
        return "high"
    return "medium"


def extract_category(q):
    q = q.lower()
    for c in ["historical", "religious", "nature"]:
        if c in q:
            return c
    return "any"


# ---------- Itinerary Generator ----------
def generate_itinerary(city, days, budget, category):
    city = city.lower()

    # Filter by city
    f = df[
        df["place_name"].str.contains(city, na=False) |
        df["description"].str.contains(city, na=False)
    ]

    # Filter category
    if category != "any":
        fc = f[f["category"].str.contains(category, na=False)]
        if not fc.empty:
            f = fc

    # Filter budget
    fb = f[f["budget"].str.contains(budget, na=False)]
    if not fb.empty:
        f = fb

    # If nothing matches, fallback to whole dataset
    if f.empty:
        f = df

    # 🔥 ENSURE EXACT NUMBER OF DAYS
    if len(f) < days:
        repeats = (days // len(f)) + 1
        f = pd.concat([f] * repeats)

    return f.sample(days)


# ---------- Clean Output ----------
def format_itinerary(itin):
    return "\n".join(
        f"Day {i}: Visit {r.place_name.title()}."
        for i, r in enumerate(itin.itertuples(), 1)
    )
