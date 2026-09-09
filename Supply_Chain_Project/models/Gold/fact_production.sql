SELECT
    production_id,
    production_date,
    sku,
    output_quantity,
    downtime_hours,
    downtime_reason,

    YEAR(production_date) AS year,
    QUARTER(production_date) AS quarter,
    MONTH(production_date) AS month,
    DAY(production_date) AS day,
    WEEKOFYEAR(production_date) AS week,
    DAYOFWEEK(production_date) AS day_of_week

FROM {{ ref('silver_production') }}