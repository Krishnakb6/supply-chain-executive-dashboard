select
    po.supplier_id,
    s.location,
    s.rating,
    po.quantity,
    po.lead_time_days,
    po.sku,
    po.order_date,

    year(po.order_date) as order_year,
    month(po.order_date) as order_month,
    quarter(po.order_date) as order_quarter,
    dayofweek(po.order_date) as order_day_of_week,

    po.delivery_delay_days,

    case
        when po.delivery_delay_days > 0 then 1
        else 0
    end as is_late

from {{ ref('silver_purchase_orders') }} po

left join {{ ref('silver_supplier') }} s
    on po.supplier_id = s.supplier_id