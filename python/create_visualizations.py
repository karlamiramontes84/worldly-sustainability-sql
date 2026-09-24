import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import numpy as np

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="worldly_sustainability",
    user="postgres",
    password=input("Enter PostgreSQL password: "),
    host="localhost",
    port="5432"
)

# Load analysis data
query = """
SELECT *
FROM analysis.travel_emissions;
"""

df = pd.read_sql(query, conn)

conn.close()

# Calculate CO2 by transportation mode
mode_emissions = (
    df.groupby("vehicle_type")["co2_kg"]
    .sum()
    .sort_values()
)

# Create horizontal bar chart
plt.figure(figsize=(10, 7))

bars = plt.barh(
    mode_emissions.index,
    mode_emissions.values
)

plt.xlabel("Estimated CO₂ (kg)")
plt.ylabel("Transportation Mode")
plt.title("Estimated CO₂ Emissions by Transportation Mode")

# Add values to the end of each bar
for bar in bars:
    value = bar.get_width()
    plt.text(
        value + 1000,
        bar.get_y() + bar.get_height() / 2,
        f"{value:,.0f}",
        va="center"
    )

plt.xlim(0, 100000)

plt.tight_layout()

# Save the chart
plt.savefig(
    "visualizations/co2_by_transportation_mode.png",
    dpi=300
)

plt.show()

# ----------------------------------------
# Chart 2: Average CO2 per Trip
# ----------------------------------------

category_summary = (
    df.groupby("scope_3_category")
    .agg(
        trips=("travel_id", "count"),
        total_co2_kg=("co2_kg", "sum"),
        avg_co2_per_trip=("co2_kg", "mean")
    )
    .sort_values("avg_co2_per_trip")
)

plt.figure(figsize=(10, 6))

bars = plt.bar(
    category_summary.index,
    category_summary["avg_co2_per_trip"]
)

plt.xlabel("Scope 3 Category")
plt.ylabel("Average Estimated CO₂ per Trip (kg)")
plt.title("Average Estimated CO₂ per Trip by Scope 3 Category")

# Add trip count, total emissions, and average emissions
# Add annotations
for bar, (_, row) in zip(bars, category_summary.iterrows()):
    value = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        value + 5,
        f"{row['avg_co2_per_trip']:,.2f} kg/trip",
        ha="center",
        va="bottom",
        fontweight="bold",
        fontsize=11
    )

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        value + 0,
        f"{row['trips']:,} trips | {row['total_co2_kg']:,.0f} kg total",
        ha="center",
        va="bottom",
        fontsize=9
    )

plt.ylim(0, 155)

plt.tight_layout()

plt.savefig(
    "visualizations/avg_co2_per_trip.png",
    dpi=300
)

plt.show()

# ----------------------------------------
# Chart 3: Monthly Estimated CO2
# ----------------------------------------

monthly_summary = (
    df.assign(
        month=pd.to_datetime(df["travel_date"]).dt.to_period("M")
    )
    .groupby("month")
    .agg(
        trips=("travel_id", "count"),
        total_co2_kg=("co2_kg", "sum")
    )
    .reset_index()
)

# Convert month to string for plotting
monthly_summary["month_name"] = (monthly_summary["month"].dt.strftime("%b"))

plt.figure(figsize=(11, 6))

plt.plot(
    monthly_summary["month_name"],
    monthly_summary["total_co2_kg"],
    marker="o"
)

plt.xlabel("Month")
plt.ylabel("Estimated CO₂ (kg)")
plt.title("Monthly Estimated CO₂ Emissions")

# Add CO2 values above each point
for _, row in monthly_summary.iterrows():
    plt.text(
        row["month_name"],
        row["total_co2_kg"] + 500,
        f"{row['total_co2_kg']:,.0f}",
        ha="center",
        va="bottom",
        fontsize=9
    )

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "visualizations/monthly_co2.png",
    dpi=300
)

plt.show()

# ----------------------------------------
# Chart 4: Business Travel - Air vs. Ground
# ----------------------------------------
#print("\nSCOPE 3 CATEGORIES:")
#print(df["scope_3_category"].value_counts())
# Filter to business travel
business_travel = df[
    df["scope_3_category"] == "Category 6 - Business Travel"
].copy()

# Classify travel as air or ground
business_travel["travel_mode"] = business_travel["vehicle_type"].apply(
    lambda x: "Air Travel" if x.startswith("Air Travel") else "Ground Travel"
)

# Calculate trips and emissions
business_mode_summary = (
    business_travel
    .groupby("travel_mode")
    .agg(
        trips=("travel_id", "count"),
        total_co2_kg=("co2_kg", "sum")
    )
)

# Calculate percentages
business_mode_summary["trip_share"] = (
    100 * business_mode_summary["trips"]
    / business_mode_summary["trips"].sum()
)

business_mode_summary["emissions_share"] = (
    100 * business_mode_summary["total_co2_kg"]
    / business_mode_summary["total_co2_kg"].sum()
)

# Put Air Travel first
business_mode_summary = business_mode_summary.reindex(
    ["Air Travel", "Ground Travel"]
)

# Create chart
x = np.arange(len(business_mode_summary))
width = 0.35

plt.figure(figsize=(10, 6))

bars1 = plt.bar(
    x - width / 2,
    business_mode_summary["trip_share"],
    width,
    label="Share of Trips"
)

bars2 = plt.bar(
    x + width / 2,
    business_mode_summary["emissions_share"],
    width,
    label="Share of CO₂ Emissions"
)

plt.xlabel("Business Travel Mode")
plt.ylabel("Share (%)")
plt.title("Business Travel: Share of Trips vs. Share of CO₂ Emissions")

plt.xticks(
    x,
    business_mode_summary.index
)

plt.ylim(0, 105)

# Add percentage labels
for bar in bars1:
    value = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        value + 2,
        f"{value:.1f}%",
        ha="center",
        va="bottom"
    )

for bar in bars2:
    value = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        value + 2,
        f"{value:.1f}%",
        ha="center",
        va="bottom"
    )

plt.legend()

plt.tight_layout()

plt.savefig(
    "visualizations/business_air_vs_ground.png",
    dpi=300
)

plt.show()

# ----------------------------------------
# KPI Summary
# ----------------------------------------

total_records = len(df)

total_co2 = df["co2_kg"].sum()

business_co2 = df.loc[
    df["scope_3_category"] == "Category 6 - Business Travel",
    "co2_kg"
].sum()

business_share = 100 * business_co2 / total_co2

business_travel = df[
    df["scope_3_category"] == "Category 6 - Business Travel"
].copy()

air_travel = business_travel[
    business_travel["vehicle_type"].str.startswith("Air Travel")
].copy()

air_business_share = 100 * len(air_travel) / len(business_travel)

air_co2_share = 100 * air_travel["co2_kg"].sum() / business_co2

avg_co2_per_record = df["co2_kg"].mean()

# Create KPI summary
kpi_summary = pd.DataFrame({
    "metric": [
        "Travel Records Analyzed",
        "Total Estimated CO2 (kg)",
        "Business Travel CO2 Share (%)",
        "Air Travel Share of Business Travel Records (%)",
        "Air Travel Share of Business Travel CO2 (%)",
        "Average CO2 per Travel Record (kg)"
    ],
    "value": [
        total_records,
        total_co2,
        business_share,
        air_business_share,
        air_co2_share,
        avg_co2_per_record
    ]
})

# Save KPI summary
kpi_summary.to_csv(
    "visualizations/kpi_summary.csv",
    index=False
)

print("\nKPI SUMMARY")
print(kpi_summary.to_string(index=False))