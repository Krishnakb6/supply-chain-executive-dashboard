select distinct production_id, date as production_date, Trim(sku) as sku,output_quantity,downtime_hours,
coalesce(downtime_reason,'No Downtime') as downtime_reason
from {{ ref('brz_production') }}