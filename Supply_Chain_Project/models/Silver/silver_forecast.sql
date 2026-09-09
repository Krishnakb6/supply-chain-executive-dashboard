select date,sku,historical_demand,forecasted_demand,forecasted_demand - historical_demand as demand_bias,
round(1-abs((historical_demand-forecasted_demand)/NULLIF(historical_demand, 0))*100,2) as forecast_accuracy
from {{ ref('brz_sales_forecast') }}