import pandas as pd
import random

random.seed(42)

districts = [
    "Bastar",
    "Sukma",
    "Bijapur",
    "Dantewada",
    "Narayanpur"
]

genders = [
    "Male",
    "Female"
]

skills = [
    "Agriculture",
    "Tailoring",
    "Handloom",
    "Hospitality",
    "Driving",
    "Carpentry",
    "Construction",
    "Livestock",
    "Food Processing"
]

placements = {
    "Agriculture": ["Agriculture", "Livestock"],
    "Tailoring": ["Tailoring", "Handloom"],
    "Handloom": ["Handloom", "Tailoring"],
    "Hospitality": ["Cafe/Hospitality", "Food Processing"],
    "Driving": ["Driving", "Logistics"],
    "Carpentry": ["Carpentry", "Construction"],
    "Construction": ["Construction", "Carpentry"],
    "Livestock": ["Livestock", "Agriculture"],
    "Food Processing": ["Food Processing", "Cafe/Hospitality"]
}

rows = []

for i in range(1, 101):

    district = random.choice(districts)

    gender = random.choice(genders)

    skill = random.choice(skills)

    placement = random.choice(
        placements[skill]
    )

    income = random.randint(
        6500,
        14000
    )

    month3 = random.choices(
        ["Retained", "Dropped"],
        weights=[85, 15]
    )[0]

    month12 = random.choices(
        ["Retained", "Dropped"],
        weights=[75, 25]
    )[0]

    month24 = random.choices(
        ["Retained", "Dropped", "Not Due"],
        weights=[65, 15, 20]
    )[0]

    if month12 == "Dropped":

        status = "Flagged"

    elif month3 == "Dropped":

        status = "Flagged"

    else:

        status = "Stable"

    rows.append({
        "Beneficiary_ID": f"B{i:03d}",
        "District": district,
        "Gender": gender,
        "Primary_Skill": skill,
        "Placement": placement,
        "Monthly_Income": income,
        "Month_3_Status": month3,
        "Month_12_Status": month12,
        "Month_24_Status": month24,
        "Overall_Status": status
    })

df = pd.DataFrame(rows)

df.to_csv(
    "data/beneficiaries.csv",
    index=False
)

print("Dataset created successfully!")

print(df.head())