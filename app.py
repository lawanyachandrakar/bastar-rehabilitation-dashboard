import streamlit as st
import pandas as pd
import plotly.express as px


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Bastar Rehabilitation Tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv("data/beneficiaries.csv")


# =========================================================
# RISK CLASSIFICATION
# =========================================================

def calculate_risk(row):

    # RED:
    # Employment has not been retained at 12 months
    if row["Month_12_Status"] == "Dropped":
        return "RED"

    # AMBER:
    # Employment was lost within first 3 months
    elif row["Month_3_Status"] == "Dropped":
        return "AMBER"

    # AMBER:
    # Income is below the illustrative prototype threshold
    elif row["Monthly_Income"] < 8000:
        return "AMBER"

    # GREEN:
    # No current warning condition
    else:
        return "GREEN"


df["Risk_Level"] = df.apply(
    calculate_risk,
    axis=1
)


# =========================================================
# TITLE
# =========================================================

st.title(
    "Bastar Rehabilitation & Livelihood Tracker"
)

st.subheader(
    "From placement counts to sustainable livelihood outcomes"
)

st.write(
    """
    A proposed monitoring dashboard for tracking livelihood
    outcomes following rehabilitation and placement across
    Bastar, Sukma, Bijapur, Dantewada and Narayanpur.
    """
)


# =========================================================
# IMPORTANT DATA DISCLAIMER
# =========================================================

st.warning(
    """
    **DEMONSTRATION PROTOTYPE**

    Beneficiary-level data displayed in this dashboard is
    synthetic and created solely for academic demonstration.
    It does not represent actual government beneficiary records.

    Risk categories and income thresholds are illustrative
    prototype assumptions and are not official government
    classifications.
    """
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("Dashboard Filters")

st.sidebar.caption(
    "Use these filters to examine different groups of beneficiaries."
)


# District filter

district_filter = st.sidebar.multiselect(
    "District",
    options=sorted(df["District"].unique()),
    default=sorted(df["District"].unique())
)


# Gender filter

gender_filter = st.sidebar.multiselect(
    "Gender",
    options=sorted(df["Gender"].unique()),
    default=sorted(df["Gender"].unique())
)


# Placement filter

placement_filter = st.sidebar.multiselect(
    "Placement",
    options=sorted(df["Placement"].unique()),
    default=sorted(df["Placement"].unique())
)


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df[
    (df["District"].isin(district_filter))
    &
    (df["Gender"].isin(gender_filter))
    &
    (df["Placement"].isin(placement_filter))
].copy()


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_beneficiaries = len(filtered_df)


# 3-month retention

if total_beneficiaries > 0:

    retained_3m = (
        filtered_df["Month_3_Status"]
        .eq("Retained")
        .mean()
        * 100
    )

else:

    retained_3m = 0


# Average income

if total_beneficiaries > 0:

    average_income = (
        filtered_df["Monthly_Income"]
        .mean()
    )

else:

    average_income = 0


# Women

women_count = (
    filtered_df["Gender"]
    .eq("Female")
    .sum()
)


# Risk categories

green_cases = (
    filtered_df["Risk_Level"]
    .eq("GREEN")
    .sum()
)

amber_cases = (
    filtered_df["Risk_Level"]
    .eq("AMBER")
    .sum()
)

red_cases = (
    filtered_df["Risk_Level"]
    .eq("RED")
    .sum()
)

priority_cases_count = amber_cases + red_cases


# =========================================================
# KPI CARDS
# =========================================================

st.divider()

k1, k2, k3, k4, k5 = st.columns(5)


k1.metric(
    "Beneficiaries",
    total_beneficiaries
)


k2.metric(
    "3-Month Retention",
    f"{retained_3m:.1f}%"
)


k3.metric(
    "Average Income",
    f"₹{average_income:,.0f}"
)


k4.metric(
    "Women",
    women_count
)


k5.metric(
    "Priority Cases",
    priority_cases_count
)


# =========================================================
# SECTION 1 — DISTRICT OVERVIEW
# =========================================================

st.divider()

st.header(
    "1. District Overview"
)

st.write(
    """
    Distribution of beneficiaries across the five districts
    covered by the proposed monitoring framework.
    """
)


district_summary = (
    filtered_df
    .groupby("District")
    .agg(
        Beneficiaries=(
            "Beneficiary_ID",
            "count"
        ),
        Average_Income=(
            "Monthly_Income",
            "mean"
        )
    )
    .reset_index()
)


fig_district = px.bar(
    district_summary,
    x="District",
    y="Beneficiaries",
    title="Beneficiaries by District",
    labels={
        "Beneficiaries": "Number of Beneficiaries",
        "District": "District"
    }
)


st.plotly_chart(
    fig_district,
    use_container_width=True
)


# =========================================================
# SECTION 2 — PLACEMENT DISTRIBUTION
# =========================================================

st.header(
    "2. Placement Distribution"
)

st.write(
    """
    Shows the livelihood sectors represented in the
    demonstration dataset.
    """
)


placement_counts = (
    filtered_df["Placement"]
    .value_counts()
    .reset_index()
)


placement_counts.columns = [
    "Placement",
    "Count"
]


fig_placement = px.pie(
    placement_counts,
    names="Placement",
    values="Count",
    title="Types of Livelihood Placement"
)


st.plotly_chart(
    fig_placement,
    use_container_width=True
)


# =========================================================
# SECTION 3 — GENDER & LIVELIHOOD
# =========================================================

st.header(
    "3. Gender & Livelihood Outcomes"
)

st.write(
    """
    Gender-disaggregated income data can help identify whether
    women and men are accessing comparable livelihood outcomes.
    """
)


gender_income = (
    filtered_df
    .groupby("Gender")
    ["Monthly_Income"]
    .mean()
    .reset_index()
)


fig_gender = px.bar(
    gender_income,
    x="Gender",
    y="Monthly_Income",
    title="Average Monthly Income by Gender",
    labels={
        "Monthly_Income": "Average Monthly Income (₹)",
        "Gender": "Gender"
    }
)


st.plotly_chart(
    fig_gender,
    use_container_width=True
)


# =========================================================
# SECTION 4 — RETENTION
# =========================================================

st.header(
    "4. Livelihood Retention"
)

st.write(
    """
    The proposed system follows beneficiaries at 3, 12 and
    24 months rather than stopping measurement at placement.
    """
)


# 3 months

total_3m = len(filtered_df)

retained_3m_count = (
    filtered_df["Month_3_Status"]
    .eq("Retained")
    .sum()
)


if total_3m > 0:

    retention_3m = (
        retained_3m_count
        / total_3m
        * 100
    )

else:

    retention_3m = 0


# 12 months

total_12m = len(filtered_df)

retained_12m_count = (
    filtered_df["Month_12_Status"]
    .eq("Retained")
    .sum()
)


if total_12m > 0:

    retention_12m = (
        retained_12m_count
        / total_12m
        * 100
    )

else:

    retention_12m = 0


# 24 months
# IMPORTANT:
# People marked "Not Due" are excluded.

month24_due = filtered_df[
    filtered_df["Month_24_Status"] != "Not Due"
]


total_24m = len(month24_due)


retained_24m_count = (
    month24_due["Month_24_Status"]
    .eq("Retained")
    .sum()
)


if total_24m > 0:

    retention_24m = (
        retained_24m_count
        / total_24m
        * 100
    )

else:

    retention_24m = 0


retention_df = pd.DataFrame({

    "Checkpoint": [
        "3 Months",
        "12 Months",
        "24 Months"
    ],

    "Retention": [
        retention_3m,
        retention_12m,
        retention_24m
    ]
})


fig_retention = px.bar(
    retention_df,
    x="Checkpoint",
    y="Retention",
    range_y=[0, 100],
    title="Retention Across Follow-up Checkpoints",
    labels={
        "Retention": "Retention (%)",
        "Checkpoint": "Follow-up Checkpoint"
    }
)


st.plotly_chart(
    fig_retention,
    use_container_width=True
)


# =========================================================
# SECTION 5 — RISK / INTERVENTION
# =========================================================

st.header(
    "5. Cases Requiring Intervention"
)

st.write(
    """
    The proposed dashboard does not treat placement as the final
    outcome. It flags cases where livelihood instability suggests
    that additional administrative or partner support may be needed.
    """
)


# ---------------------------------------------------------
# RISK SUMMARY
# ---------------------------------------------------------

r1, r2, r3 = st.columns(3)


r1.metric(
    "GREEN — Stable",
    green_cases
)


r2.metric(
    "AMBER — Follow-up",
    amber_cases
)


r3.metric(
    "RED — Intervention",
    red_cases
)


# ---------------------------------------------------------
# EXPLANATION
# ---------------------------------------------------------

st.info(
    """
    **Illustrative risk logic**

    GREEN = no current warning condition.

    AMBER = employment was lost within 3 months OR monthly
    income is below the illustrative ₹8,000 threshold.

    RED = employment was not retained at 12 months.

    These thresholds are proposed for this prototype and would
    need validation before operational use.
    """
)


# ---------------------------------------------------------
# PRIORITY CASES
# ---------------------------------------------------------

priority_cases = filtered_df[
    filtered_df["Risk_Level"].isin(
        ["RED", "AMBER"]
    )
].copy()


if len(priority_cases) == 0:

    st.success(
        "No cases currently require intervention."
    )

else:

    st.subheader(
        "Priority Cases"
    )

    priority_cases = priority_cases[
        [
            "Beneficiary_ID",
            "District",
            "Gender",
            "Primary_Skill",
            "Placement",
            "Monthly_Income",
            "Month_3_Status",
            "Month_12_Status",
            "Month_24_Status",
            "Risk_Level"
        ]
    ].sort_values(
        "Risk_Level"
    )


    st.dataframe(
        priority_cases,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# SECTION 6 — BENEFICIARY DATABASE
# =========================================================

st.header(
    "6. Beneficiary Tracking Database"
)

st.write(
    """
    A district administration could use this view to review
    individual placement and follow-up records.
    """
)


display_columns = [
    "Beneficiary_ID",
    "District",
    "Gender",
    "Primary_Skill",
    "Placement",
    "Monthly_Income",
    "Month_3_Status",
    "Month_12_Status",
    "Month_24_Status",
    "Risk_Level"
]


st.dataframe(
    filtered_df[display_columns],
    use_container_width=True,
    hide_index=True
)


# =========================================================
# SECTION 7 — SKILLS TO LOCAL MARKET MATCHING
# =========================================================

st.divider()

st.header(
    "7. Skills-to-Local-Market Matching"
)

st.write(
    """
    This demonstrates the second part of the proposed intervention:
    matching an individual's existing skills with potential local
    livelihood pathways.
    """
)


st.info(
    """
    The scores below are illustrative. They demonstrate the logic
    of a future AI-assisted matching system and are NOT actual
    recommendations for real beneficiaries.
    """
)


selected_id = st.selectbox(
    "Select a beneficiary",
    df["Beneficiary_ID"]
)


person = df[
    df["Beneficiary_ID"] == selected_id
].iloc[0]


# ---------------------------------------------------------
# BENEFICIARY PROFILE
# ---------------------------------------------------------

p1, p2, p3, p4 = st.columns(4)


p1.metric(
    "Beneficiary",
    person["Beneficiary_ID"]
)


p2.metric(
    "District",
    person["District"]
)


p3.metric(
    "Gender",
    person["Gender"]
)


p4.metric(
    "Primary Skill",
    person["Primary_Skill"]
)


# ---------------------------------------------------------
# MATCHING RULES
# ---------------------------------------------------------

matching_rules = {

    "Agriculture": [
        ("Agriculture", 94),
        ("Livestock", 82),
        ("Food Processing", 61)
    ],

    "Tailoring": [
        ("Tailoring", 94),
        ("Handloom", 88),
        ("Hospitality", 38)
    ],

    "Handloom": [
        ("Handloom", 96),
        ("Tailoring", 87),
        ("Hospitality", 41)
    ],

    "Hospitality": [
        ("Cafe/Hospitality", 95),
        ("Food Processing", 79),
        ("Tailoring", 35)
    ],

    "Driving": [
        ("Driving", 96),
        ("Logistics", 85),
        ("Construction", 45)
    ],

    "Carpentry": [
        ("Carpentry", 95),
        ("Construction", 82),
        ("Agriculture", 42)
    ],

    "Construction": [
        ("Construction", 94),
        ("Carpentry", 86),
        ("Logistics", 47)
    ],

    "Livestock": [
        ("Livestock", 94),
        ("Agriculture", 84),
        ("Food Processing", 55)
    ],

    "Food Processing": [
        ("Food Processing", 95),
        ("Cafe/Hospitality", 82),
        ("Agriculture", 52)
    ]
}


matches = matching_rules.get(
    person["Primary_Skill"],
    []
)


match_df = pd.DataFrame(
    matches,
    columns=[
        "Potential Livelihood",
        "Match Score"
    ]
)


# Highest match first

match_df = match_df.sort_values(
    "Match Score",
    ascending=True
)


fig_match = px.bar(
    match_df,
    x="Match Score",
    y="Potential Livelihood",
    orientation="h",
    range_x=[0, 100],
    title="Potential Livelihood Matches",
    labels={
        "Match Score": "Illustrative Match Score",
        "Potential Livelihood": "Potential Livelihood"
    }
)


st.plotly_chart(
    fig_match,
    use_container_width=True
)


# ---------------------------------------------------------
# TOP RECOMMENDATION
# ---------------------------------------------------------

best_match = (
    match_df
    .sort_values(
        "Match Score",
        ascending=False
    )
    .iloc[0]
)


st.success(
    f"""
    **Highest-scoring pathway in this prototype:**
    {best_match["Potential Livelihood"]}
    ({best_match["Match Score"]}% illustrative match)

    This is a demonstration of ranking logic only. A real system
    would require validated local labour-market data and human
    review before any placement decision.
    """
)


# =========================================================
# SECTION 8 — PROPOSED WORKFLOW
# =========================================================

st.divider()

st.header(
    "8. Proposed Rehabilitation Monitoring Workflow"
)

st.markdown(
    """
    **1. Surrender & Intake**

    Record skills, gender, circumstances and preferences.

    ↓

    **2. Skills-to-Market Matching**

    Compare beneficiary profile with available local livelihood
    opportunities.

    ↓

    **3. Placement**

    Provide training and facilitate placement.

    ↓

    **4. Follow-up**

    Review livelihood status at 3, 12 and 24 months.

    ↓

    **5. Risk Detection**

    Identify livelihood instability.

    ↓

    **6. Human Intervention**

    Re-training, re-matching, counselling or additional support
    where appropriate.
    """
)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    """
    Academic prototype | Bastar rehabilitation and livelihood
    monitoring | Beneficiary-level dataset is synthetic.

    AI is proposed only as a tool for structuring information
    and surfacing patterns. Decisions remain with district
    officials and relevant practitioners.
    """
)