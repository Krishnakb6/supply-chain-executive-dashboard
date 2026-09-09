SELECT
    purchase_order_id,
    order_date,
    sku,
    supplier_id,
    quantity,
    promised_delivery_date,
    actual_delivery_date,

    DATEDIFF(actual_delivery_date, order_date) AS lead_time_days,

    DATEDIFF(actual_delivery_date, promised_delivery_date) AS delivery_delay_days

from {{ ref('brz_purchase_orders') }}