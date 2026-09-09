select shipment_id,purchase_order_id,transport_mode,shipment_cost,transit_delay_days
from {{ref('brz_logistics')}}