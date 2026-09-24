import pandas as pd
import numpy as np

# Make results reproducible
np.random.seed(42)

# Number of simulated travel records
N = 5000

# Employee home states
states = [
    "California",
    "Texas",
    "New York",
    "Washington",
    "Colorado",
    "Florida",
    "Illinois",
    "Massachusetts",
    "Georgia",
    "Other"
]

state_probabilities = [
    0.35,  # California
    0.12,  # Texas
    0.10,  # New York
    0.08,  # Washington
    0.07,  # Colorado
    0.06,  # Florida
    0.05,  # Illinois
    0.04,  # Massachusetts
    0.04,  # Georgia
    0.09   # Other
]

# EPA transportation factors loaded into PostgreSQL
vehicle_types = [
    "Passenger Car",
    "Light-Duty Truck",
    "Motorcycle",
    "Intercity Rail - Northeast Corridor",
    "Intercity Rail - Other Routes",
    "Intercity Rail - National Average",
    "Commuter Rail",
    "Transit Rail (i.e. Subway, Tram)",
    "Bus",
    "Air Travel - Short Haul (< 300 miles)",
    "Air Travel - Medium Haul (>= 300 miles, < 2300 miles)",
    "Air Travel - Long Haul (>= 2300 miles)"
]

# Generate employee IDs
employee_ids = [f"E{1000 + i}" for i in range(1, 101)]

records = []

for travel_id in range(1, N + 1):

    employee_id = np.random.choice(employee_ids)

    state = np.random.choice(
        states,
        p=state_probabilities
    )

    travel_type = np.random.choice(
        ["Employee Commuting", "Business Travel"],
        p=[0.70, 0.30]
    )

    if travel_type == "Employee Commuting":

        # Commuting is primarily by car, but includes
        # public transportation and motorcycles.
        vehicle_type = np.random.choice(
            [
                "Passenger Car",
                "Light-Duty Truck",
                "Motorcycle",
                "Commuter Rail",
                "Transit Rail (i.e. Subway, Tram)",
                "Bus"
            ],
            p=[0.55, 0.12, 0.04, 0.08, 0.13, 0.08]
        )

        purpose = "Commute"

        # Typical one-way commuting distance
        distance = round(
            np.random.uniform(3, 40),
            1
        )

        destination_state = state

    else:

        # Business travel can use any of the EPA
        # transportation categories.
        vehicle_type = np.random.choice(
            vehicle_types,
            p=[
                0.12,  # Passenger Car
                0.05,  # Light-Duty Truck
                0.01,  # Motorcycle
                0.06,  # Intercity Rail - Northeast Corridor
                0.06,  # Intercity Rail - Other Routes
                0.04,  # Intercity Rail - National Average
                0.03,  # Commuter Rail
                0.03,  # Transit Rail
                0.04,  # Bus
                0.12,  # Air - Short Haul
                0.35,  # Air - Medium Haul
                0.09   # Air - Long Haul
            ]
        )

        purpose = np.random.choice(
            [
                "Client Meeting",
                "Conference",
                "Off-site Meeting",
                "Site Visit"
            ]
        )

        # Distance depends on the transportation mode.
        if "Short Haul" in vehicle_type:
            distance = round(
                np.random.uniform(100, 299),
                1
            )

        elif "Medium Haul" in vehicle_type:
            distance = round(
                np.random.uniform(300, 1800),
                1
            )

        elif "Long Haul" in vehicle_type:
            distance = round(
                np.random.uniform(2300, 4500),
                1
            )

        elif "Northeast Corridor" in vehicle_type:
            distance = round(
                np.random.uniform(50, 450),
                1
            )

        elif "Other Routes" in vehicle_type:
            distance = round(
                np.random.uniform(100, 800),
                1
            )

        elif "National Average" in vehicle_type:
            distance = round(
                np.random.uniform(100, 800),
                1
            )

        elif "Rail" in vehicle_type:
            distance = round(
                np.random.uniform(10, 100),
                1
            )

        elif vehicle_type == "Bus":
            distance = round(
                np.random.uniform(5, 100),
                1
            )

        else:
            distance = round(
                np.random.uniform(5, 100),
                1
            )

        # Business travel can cross state lines.
        destination_state = np.random.choice(states)

    # Match the activity unit to the EPA factor.
    if vehicle_type in [
        "Passenger Car",
        "Light-Duty Truck",
        "Motorcycle"
    ]:
        activity_unit = "vehicle-mile"
    else:
        activity_unit = "passenger-mile"

    # Generate a date during 2025.
    travel_date = pd.Timestamp(
        np.random.choice(
            pd.date_range(
                "2025-01-01",
                "2025-12-31"
            )
        )
    )

    records.append([
        travel_id,
        employee_id,
        travel_date,
        travel_type,
        vehicle_type,
        distance,
        activity_unit,
        purpose,
        state,
        destination_state
    ])


# Create DataFrame
df = pd.DataFrame(
    records,
    columns=[
        "travel_id",
        "employee_id",
        "travel_date",
        "travel_type",
        "vehicle_type",
        "distance",
        "activity_unit",
        "purpose",
        "origin_state",
        "destination_state"
    ]
)

# Sort chronologically
df = df.sort_values(
    "travel_date"
).reset_index(drop=True)

# Display the sample
print(df.head(10).to_string(index=False))

# Save the sample
df.to_csv(
    "data/processed/travel_activity.csv",
    index=False
)

print(f"\nGenerated {len(df)} travel records.")
print(
    "Saved to "
    "data/processed/travel_activity.csv"
)