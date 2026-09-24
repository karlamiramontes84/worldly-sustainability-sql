import pandas as pd

file_path = "data/raw/ghg-emission-factors-hub-2025.xlsx"

# Read the section of the EPA workbook containing Category 6/7
# Read the Category 6/7 table: one header row plus 12 data rows
df = pd.read_excel(
    file_path,
    sheet_name="Emission Factors Hub",
    header=0,
    skiprows=502,
    nrows=12
)

# Keep only the five columns containing the Category 6/7 table
df = df.iloc[:, 2:7]

# Display the extracted table
#print(df.to_string(index=False))

# Rename columns for database use
df.columns = [
    "vehicle_type",
    "co2_factor_kg",
    "ch4_factor_g",
    "n2o_factor_g",
    "activity_unit"
]

print (df.to_string(index=False))
#print(df["vehicle_type"].tolist())

# Remove EPA footnote letters from vehicle type names
df["vehicle_type"] = (
    df["vehicle_type"]
    .str.replace(r"\s+[A-E]$", "", regex=True)
    .str.strip()
)
#print(df["vehicle_type"].tolist())

# Add source metadata
df["category"] = "Scope 3 Category 6/7"
df["source_year"] = 2025

print(df.to_string(index=False))

# Check for missing values
print("\nMissing values:")
print(df.isna().sum())

# Check data types
print("\nData types:")
print(df.dtypes)

# Check for duplicate records
print("\nDuplicate rows:", df.duplicated().sum())

# Save cleaned data
output_path = "data/processed/category_6_7_emission_factors.csv"
df.to_csv(output_path, index=False)

print("\nCleaned data saved to:", output_path)