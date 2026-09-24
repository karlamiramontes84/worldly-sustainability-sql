import pandas as pd

# Load the simulated travel data
df = pd.read_csv("data/processed/travel_activity.csv")

# 1. Row count
print("ROW COUNT")
print(len(df))

# 2. Missing values
print("\nMISSING VALUES")
print(df.isna().sum())

# 3. Travel type distribution
print("\nTRAVEL TYPE")
print(df["travel_type"].value_counts())
print(df["travel_type"].value_counts(normalize=True))

# 4. Transportation type distribution
print("\nVEHICLE TYPE")
print(df["vehicle_type"].value_counts())

# 5. Origin state distribution
print("\nORIGIN STATE")
print(df["origin_state"].value_counts())

# 6. Activity unit distribution
print("\nACTIVITY UNIT")
print(df["activity_unit"].value_counts())

# 7. Check that vehicle-based modes use vehicle-miles
vehicle_modes = [
    "Passenger Car",
    "Light-Duty Truck",
    "Motorcycle"
]

vehicle_mode_errors = df[
    df["vehicle_type"].isin(vehicle_modes)
    & (df["activity_unit"] != "vehicle-mile")
]

print("\nVEHICLE-MILE CHECK")
print(f"Errors: {len(vehicle_mode_errors)}")

# 8. Check that all other modes use passenger-miles
passenger_mode_errors = df[
    ~df["vehicle_type"].isin(vehicle_modes)
    & (df["activity_unit"] != "passenger-mile")
]

print("\nPASSENGER-MILE CHECK")
print(f"Errors: {len(passenger_mode_errors)}")