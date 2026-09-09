select *,
CASE
    When current_stock<=reorder_level then 'Reorder'
    else 'Sufficient'
    END AS inventory_status
from {{ ref('brz_inventory') }}