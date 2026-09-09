select l.shipment_id,l.purchase_order_id,l.transport_mode,l.shipment_cost,l.transit_delay_days,p.supplier_id,
p.sku from {{ ref('silver_logistics') }} l left join {{ ref('silver_purchase_orders') }} p 
on l.purchase_order_id=p.purchase_order_id