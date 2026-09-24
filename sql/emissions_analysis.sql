-- Scope 3 Travel Emissions Analysis
-- SQL Analysis Queries
-----------------------

-- Purpose:
-- Analyze estimated CO2 emissions from simulated employee travel
-- activity classified as GHG Protocol Scope 3 Category 6
-- (Business Travel) and Category 7 (Employee Commuting).
---------------------------------------------------------

-- Database:
-- PostgreSQL
-------------

-- Note:
-- Travel activity is simulated for portfolio purposes.
-- Emissions are estimates based on EPA 2025 transportation
-- emission factors.

-- ============================================================
-- 1. DATASET OVERVIEW
-- ============================================================

-- Total number of travel records and total estimated emissions.

SELECT
COUNT(*) AS travel_records,
ROUND(SUM(co2_kg), 2) AS total_co2_kg,
ROUND(AVG(co2_kg), 2) AS avg_co2_per_record
FROM travel_activity;

-- ============================================================
-- 2. EMISSIONS BY SCOPE 3 CATEGORY
-- ============================================================

-- Compare travel volume and estimated emissions between
-- Business Travel and Employee Commuting.

SELECT
scope_3_category,
COUNT(*) AS travel_records,
ROUND(SUM(co2_kg), 2) AS total_co2_kg,
ROUND(AVG(co2_kg), 2) AS avg_co2_per_record
FROM travel_activity
GROUP BY scope_3_category
ORDER BY total_co2_kg DESC;

-- ============================================================
-- 3. SHARE OF TOTAL EMISSIONS BY SCOPE 3 CATEGORY
-- ============================================================

-- Calculate each Scope 3 category's percentage of total
-- estimated emissions.

SELECT
scope_3_category,
COUNT(*) AS travel_records,
ROUND(SUM(co2_kg), 2) AS total_co2_kg,
ROUND(
100.0 * SUM(co2_kg) /
SUM(SUM(co2_kg)) OVER (),
2
) AS co2_share_pct
FROM travel_activity
GROUP BY scope_3_category
ORDER BY co2_share_pct DESC;

-- ============================================================
-- 4. EMISSIONS BY TRANSPORTATION MODE
-- ============================================================

-- Identify which transportation modes contribute the most
-- estimated CO2 emissions.

SELECT
vehicle_type,
COUNT(*) AS travel_records,
ROUND(SUM(co2_kg), 2) AS total_co2_kg,
ROUND(AVG(co2_kg), 2) AS avg_co2_per_record
FROM travel_activity
GROUP BY vehicle_type
ORDER BY total_co2_kg DESC;

-- ============================================================
-- 5. TRANSPORTATION MODE SHARE OF TOTAL EMISSIONS
-- ============================================================

-- Calculate the percentage of total estimated emissions
-- attributable to each transportation mode.

SELECT
vehicle_type,
COUNT(*) AS travel_records,
ROUND(SUM(co2_kg), 2) AS total_co2_kg,
ROUND(
100.0 * SUM(co2_kg) /
SUM(SUM(co2_kg)) OVER (),
2
) AS co2_share_pct
FROM travel_activity
GROUP BY vehicle_type
ORDER BY co2_share_pct DESC;

-- ============================================================
-- 6. BUSINESS TRAVEL VS. EMPLOYEE COMMUTING
-- ============================================================

-- Compare the number of records, total emissions, and
-- average emissions per record for each Scope 3 category.

SELECT
scope_3_category,
COUNT(*) AS travel_records,
ROUND(SUM(co2_kg), 2) AS total_co2_kg,
ROUND(AVG(co2_kg), 2) AS avg_co2_per_record
FROM travel_activity
WHERE scope_3_category IN (
'Category 6 - Business Travel',
'Category 7 - Employee Commuting'
)
GROUP BY scope_3_category
ORDER BY scope_3_category;

-- ============================================================
-- 7. BUSINESS TRAVEL: AIR VS. GROUND
-- ============================================================

-- Compare air and ground Business Travel by travel volume
-- and estimated emissions.

SELECT
CASE
WHEN vehicle_type LIKE 'Air Travel%' THEN 'Air Travel'
ELSE 'Ground Travel'
END AS business_travel_mode,
COUNT(*) AS travel_records,
ROUND(SUM(co2_kg), 2) AS total_co2_kg
FROM travel_activity
WHERE scope_3_category = 'Category 6 - Business Travel'
GROUP BY
CASE
WHEN vehicle_type LIKE 'Air Travel%' THEN 'Air Travel'
ELSE 'Ground Travel'
END
ORDER BY total_co2_kg DESC;

-- ============================================================
-- 8. AIR TRAVEL SHARE OF BUSINESS TRAVEL RECORDS
-- ============================================================

-- Calculate the percentage of Business Travel records
-- that involve air travel.

SELECT
COUNT(*) AS business_travel_records,
COUNT(*) FILTER (
WHERE vehicle_type LIKE 'Air Travel%'
) AS air_travel_records,
ROUND(
100.0 * COUNT(*) FILTER (
WHERE vehicle_type LIKE 'Air Travel%'
) / COUNT(*),
2
) AS air_travel_record_share_pct
FROM travel_activity
WHERE scope_3_category = 'Category 6 - Business Travel';

-- ============================================================
-- 9. AIR TRAVEL SHARE OF BUSINESS TRAVEL EMISSIONS
-- ============================================================

-- Calculate the percentage of Business Travel emissions
-- attributable to air travel.

SELECT
ROUND(SUM(co2_kg), 2) AS business_travel_co2_kg,
ROUND(
SUM(co2_kg) FILTER (
WHERE vehicle_type LIKE 'Air Travel%'
),
2
) AS air_travel_co2_kg,
ROUND(
100.0 * SUM(co2_kg) FILTER (
WHERE vehicle_type LIKE 'Air Travel%'
) / SUM(co2_kg),
2
) AS air_travel_co2_share_pct
FROM travel_activity
WHERE scope_3_category = 'Category 6 - Business Travel';

-- ============================================================
-- 10. MONTHLY EMISSIONS
-- ============================================================

-- Examine estimated emissions and travel volume by month.

SELECT
TO_CHAR(travel_date, 'YYYY-MM') AS month,
COUNT(*) AS travel_records,
ROUND(SUM(co2_kg), 2) AS total_co2_kg,
ROUND(AVG(co2_kg), 2) AS avg_co2_per_record
FROM travel_activity
GROUP BY TO_CHAR(travel_date, 'YYYY-MM')
ORDER BY month;

-- ============================================================
-- 11. MONTHLY EMISSIONS BY SCOPE 3 CATEGORY
-- ============================================================

-- Examine monthly emissions separately for Business Travel
-- and Employee Commuting.

SELECT
TO_CHAR(travel_date, 'YYYY-MM') AS month,
scope_3_category,
COUNT(*) AS travel_records,
ROUND(SUM(co2_kg), 2) AS total_co2_kg,
ROUND(AVG(co2_kg), 2) AS avg_co2_per_record
FROM travel_activity
GROUP BY
TO_CHAR(travel_date, 'YYYY-MM'),
scope_3_category
ORDER BY
month,
scope_3_category;

-- ============================================================
-- 12. EMISSIONS BY ORIGIN STATE
-- ============================================================

-- Compare travel activity and estimated emissions by
-- employee origin state.

SELECT
COALESCE(origin_state, 'Other') AS origin_state,
COUNT(*) AS travel_records,
ROUND(SUM(co2_kg), 2) AS total_co2_kg,
ROUND(AVG(co2_kg), 2) AS avg_co2_per_record
FROM travel_activity
GROUP BY COALESCE(origin_state, 'Other')
ORDER BY total_co2_kg DESC;

-- ============================================================
-- 13. EMISSION FACTOR / ACTIVITY UNIT CHECK
-- ============================================================

-- Review the transportation modes and activity units being
-- used in the calculated dataset.

SELECT
vehicle_type,
activity_unit,
COUNT(*) AS travel_records
FROM travel_activity
GROUP BY
vehicle_type,
activity_unit
ORDER BY
vehicle_type,
activity_unit;

-- ============================================================
-- 14. MISSING VALUE CHECK
-- ============================================================

-- Identify missing values in key analytical fields.

SELECT
COUNT(*) FILTER (WHERE travel_date IS NULL) AS missing_travel_date,
COUNT(*) FILTER (WHERE vehicle_type IS NULL) AS missing_vehicle_type,
COUNT(*) FILTER (WHERE distance IS NULL) AS missing_distance,
COUNT(*) FILTER (WHERE activity_unit IS NULL) AS missing_activity_unit,
COUNT(*) FILTER (WHERE co2_kg IS NULL) AS missing_co2
FROM travel_activity;

-- ============================================================
-- 15. EMISSION CALCULATION COMPLETENESS
-- ============================================================

-- Confirm that calculated emissions exist for all travel
-- records.

SELECT
COUNT(*) AS total_records,
COUNT(co2_kg) AS records_with_co2,
COUNT(*) - COUNT(co2_kg) AS records_missing_co2
FROM travel_activity;

-- ============================================================
-- 16. HEADLINE KPI SUMMARY
-- ============================================================

-- Reproduce the main metrics used in the project summary.

SELECT
COUNT(*) AS travel_records_analyzed,

```
ROUND(
    SUM(co2_kg),
    2
) AS total_estimated_co2_kg,

ROUND(
    100.0 * SUM(co2_kg) FILTER (
        WHERE scope_3_category = 'Category 6 - Business Travel'
    ) / SUM(co2_kg),
    2
) AS business_travel_co2_share_pct,

ROUND(
    100.0 * COUNT(*) FILTER (
        WHERE scope_3_category = 'Category 6 - Business Travel'
          AND vehicle_type LIKE 'Air Travel%'
    )
    /
    COUNT(*) FILTER (
        WHERE scope_3_category = 'Category 6 - Business Travel'
    ),
    2
) AS air_travel_share_of_business_records_pct,

ROUND(
    100.0 * SUM(co2_kg) FILTER (
        WHERE scope_3_category = 'Category 6 - Business Travel'
          AND vehicle_type LIKE 'Air Travel%'
    )
    /
    SUM(co2_kg) FILTER (
        WHERE scope_3_category = 'Category 6 - Business Travel'
    ),
    2
) AS air_travel_share_of_business_co2_pct,

ROUND(
    AVG(co2_kg),
    2
) AS avg_co2_per_travel_record_kg
```

FROM travel_activity;
