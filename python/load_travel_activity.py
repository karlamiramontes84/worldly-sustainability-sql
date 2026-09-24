import pandas as pd
import psycopg2

# Load the processed CSV
csv_path = "data/processed/travel_activity.csv"
df = pd.read_csv(csv_path)

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="worldly_sustainability",
    user="postgres",
    password=input("Enter your PostgreSQL password: "),
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

# Insert records
for _, row in df.iterrows():
    cursor.execute(
        """
        INSERT INTO raw.travel_activity (
            travel_id,
            employee_id,
            travel_date,
            travel_type,
            vehicle_type,
            distance,
            activity_unit,
            purpose,
            origin_state,
            destination_state
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            int(row["travel_id"]),
            row["employee_id"],
            row["travel_date"],
            row["travel_type"],
            row["vehicle_type"],
            float(row["distance"]),
            row["activity_unit"],
            row["purpose"],
            row["origin_state"],
            row["destination_state"]
        )
    )

conn.commit()

print(f"Successfully loaded {len(df)} records.")

cursor.close()
conn.close()