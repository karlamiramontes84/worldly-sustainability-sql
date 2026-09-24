import pandas as pd
import psycopg2

# 1. Load the processed CSV
csv_path = "data/processed/category_6_7_emission_factors.csv"
df = pd.read_csv(csv_path)

print(f"CSV loaded: {len(df)} rows")
print("Columns:")
print(df.columns.tolist())

# 2. Basic checks
expected_columns = [
    "vehicle_type",
    "co2_factor_kg",
    "ch4_factor_g",
    "n2o_factor_g",
    "activity_unit",
    "category",
    "source_year"
]

if list(df.columns) != expected_columns:
    raise ValueError(
        f"Unexpected columns.\nExpected: {expected_columns}\n"
        f"Found: {df.columns.tolist()}"
    )

if len(df) != 12:
    raise ValueError(f"Expected 12 rows, but found {len(df)}")

if df.isnull().any().any():
    raise ValueError("The CSV contains missing values.")

print("CSV checks passed.")

# 3. Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="worldly_sustainability",
    user="postgres",
    password=input("Enter your PostgreSQL password: "),
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# 4. Insert the data
insert_query = """
    INSERT INTO raw.emission_factors
    (vehicle_type, co2_factor_kg, ch4_factor_g, n2o_factor_g,
     activity_unit, category, source_year)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
"""

try:
    for _, row in df.iterrows():
        cur.execute(
            insert_query,
            (
                row["vehicle_type"],
                row["co2_factor_kg"],
                row["ch4_factor_g"],
                row["n2o_factor_g"],
                row["activity_unit"],
                row["category"],
                row["source_year"]
            )
        )

    conn.commit()

    print(f"Successfully loaded {len(df)} rows into raw.emission_factors.")

except Exception as e:
    conn.rollback()
    print("Import failed. No data was committed.")
    print(f"Error: {e}")

finally:
    cur.close()
    conn.close()