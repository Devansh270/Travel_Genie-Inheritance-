import re
import os
import pandas as pd

# Build absolute path safely
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


def generate_itinerary(city, days, budget, category):
    city = city.lower()

    def valid(row):
        text = row.place_name + " " + row.description
        return city in text

    f = df[df.apply(valid, axis=1)]

    if category != "any":
        fc = f[f.category.str.contains(category)]
        if not fc.empty:
            f = fc

    fb = f[f.budget.str.contains(budget)]
    if not fb.empty:
        f = fb

    if f.empty:
        return df.sample(min(days, len(df)))

    return f.sample(min(days, len(f)))


def format_itinerary(itin):
    return "\n".join(
        f"Day {i}: Visit {r.place_name.title()}. {r.description}"
        for i, r in enumerate(itin.itertuples(), 1)
    )
