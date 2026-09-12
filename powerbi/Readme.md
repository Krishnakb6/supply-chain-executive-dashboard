# Power BI - Supply Chain Analytics Dashboard

This folder documents the Power BI component of the Supply Chain & Manufacturing Analytics Platform.

Power BI provides the business-facing visualization layer for supplier performance, inventory, production, logistics, purchase orders, and forecasting.

## Dashboard Purpose

The dashboard provides a consolidated view of supply chain operations and supports questions such as:

- How are suppliers performing?
- Where are delivery delays occurring?
- What is the current inventory position?
- How is production performing?
- What logistics issues are occurring?
- How does demand compare with forecasts?
- Which areas require management attention?

## Data Architecture

Power BI consumes the business-ready Gold layer produced through Databricks and dbt.

```text
CSV Sources
     |
     v
Databricks Bronze
     |
     v
dbt Silver
     |
     v
dbt Gold
     |
     v
Power BI
```

## Gold Tables

### Dimensions

```text
dim_calendar
dim_product
dim_suppliers
dim_warehouse
```

### Facts

```text
fact_inventory
fact_logistics
fact_production
fact_purchase
fact_sales_forecast
```

These tables form the analytical foundation for reporting.

## Dashboard Areas

### Supplier Performance

Supplier analysis focuses on supplier characteristics and purchasing performance.

Relevant metrics include:

- Supplier rating
- Purchase volume
- Delivery performance
- Delivery delays
- Supplier comparisons

### Purchase Orders

Purchase-order analysis provides visibility into:

- Order quantities
- Lead times
- Delivery delays
- Supplier performance
- SKU-level purchasing activity

This area connects with the Machine Learning delivery-risk model.

### Inventory

Inventory analysis provides SKU and warehouse-level visibility.

Questions include:

- Which SKUs have low stock?
- Which warehouses have inventory pressure?
- Which products are approaching reorder levels?
- How is inventory distributed?

### Production

Production analysis focuses on output and downtime.

Relevant information includes:

- Production output
- Downtime hours
- Downtime reasons
- Production performance

### Logistics

Logistics analysis covers:

- Shipment cost
- Transport mode
- Transit delays
- Logistics performance

### Sales Forecasting

Forecast analysis compares historical demand with forecasted demand.

It provides visibility into:

- Demand trends
- Forecast performance
- Demand planning
- Potential supply-demand gaps

## Streamlit Integration

The Power BI report is embedded into the Streamlit application through a dedicated dashboard page.

The current implementation uses:

```python
st.iframe(
    POWER_BI_URL,
    height=800
)
```

The report uses a Power BI `reportEmbed` URL.

## Authentication

The current Power BI report uses an authenticated embed configuration.

Users may need to sign in and have appropriate access to the Power BI report.

Therefore, the current implementation should not be treated as an anonymous public embed.

For production customer-facing applications, Power BI Embedded or another appropriate deployment architecture may be required.

## Application Architecture

```text
                 SUPPLY CHAIN DATA
                        |
                        v
                 Databricks + dbt
                        |
                        v
                    Gold Layer
                        |
             +----------+----------+
             |                     |
             v                     v
         Power BI             ML Dataset
             |                     |
             v                     v
       Streamlit App        Random Forest
                                   |
                                   v
                            Supplier Risk
                                   |
                                   v
                              Gemini AI
```

This combines:

- Descriptive analytics
- Diagnostic analysis
- Predictive analytics
- Natural-language analytics

## Business Value

The Power BI dashboard provides:

- Centralized supply chain visibility
- Supplier performance monitoring
- Inventory visibility
- Production monitoring
- Logistics analysis
- Forecast analysis
- Interactive filtering and exploration

The Machine Learning component extends descriptive reporting by identifying purchase orders with elevated delivery risk.

## Relationship with Machine Learning

```text
Power BI
    |
    +-- What happened?
    +-- Where did it happen?
    +-- How is performance changing?

Machine Learning
    |
    +-- What is likely to happen?
    +-- Which orders are at risk?
    +-- Which suppliers require attention?
```

Together they support both historical analysis and predictive decision support.

## Repository Organization

Recommended structure:

```text
powerbi/
├── Readme.md
├── Screenshots/
│   ├── Executive_Overview.png
│   ├── Supplier_View.png
│   └── ...
└── <Power BI project/report files>
```

This repository currently stores dashboard screenshots in `powerbi/Screenshots/`.
Add the Power BI report file or workspace export to this folder when it is
available; the report itself is not required to run the Streamlit app because
the app embeds the configured Power BI report URL.

Screenshots can be referenced from the main GitHub README.

## Dashboard Documentation

Recommended dashboard pages to document:

```text
Executive Overview
Supplier Performance
Inventory Analysis
Production Analysis
Logistics Analysis
Forecast Analysis
```

For each page, document:

- Purpose
- Main KPIs
- Important visuals
- Filters
- Business questions answered

## Deployment Considerations

Before publishing:

1. Confirm the report does not expose confidential data.
2. Do not publish credentials.
3. Do not commit API keys.
4. Verify Power BI sharing and authentication settings.
5. Test the Streamlit application using the intended viewer account.
6. If anonymous public access is required, use an appropriate Power BI publishing/deployment method rather than relying on an authenticated embed URL.

## Future Improvements

- Executive KPI page
- Supplier drill-through
- Warehouse drill-through
- Product-level analysis
- Dynamic KPI cards
- Advanced DAX measures
- Conditional formatting
- Forecast accuracy metrics
- Supplier risk integration
- ML prediction overlays
- Automated refresh
- Row-level security

## Summary

Power BI provides the interactive business intelligence layer of the project.

## Local Validation Checklist

Before publishing the report or sharing the app:

1. Confirm the report URL opens for the intended viewer account.
2. Confirm all Gold-layer tables refresh successfully.
3. Check that slicers and drill-through pages return data.
4. Verify that screenshots do not expose confidential information.

The overall platform connects:

```text
Data Engineering
       |
       v
Business Intelligence
       |
       v
Predictive Analytics
       |
       v
AI-Assisted Analysis
```

This creates an end-to-end supply chain analytics experience.
