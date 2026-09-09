Supply Chain Executive Dashboard

An interactive Power BI Supply Chain Analytics Dashboard designed to
provide an executive-level view of supplier performance, purchasing
activity, logistics costs, production downtime, and demand trends.

The project follows a Bronze → Silver → Gold data-layer
architecture: the Bronze layer contains the raw source CSVs, the Silver
layer contains cleaned and processed datasets, and the Gold layer
contains joined, business-ready tables used for Power BI reporting.

📊 Dashboard Preview

Executive Overview
![Alt text](powerbi/Screenshots/Executive_Overview.png)


Filtered Supplier View
![Alt text](powerbi/Screenshots/Filtered_Supplier_view.png)


🎯 Project Objective

The objective of this project is to turn operational supply-chain data
into an interactive dashboard that helps decision-makers answer
questions such as:

How are order volumes changing over time?

Which suppliers have the highest delivery delays?

What are the major causes of production downtime?

How much is being spent on logistics?

How does forecasted demand compare with historical demand?

Which suppliers or SKUs may require operational attention?

How do supply-chain KPIs change when filtering by supplier, SKU, or
year?

🗂️ Data Sources

The project starts with the following CSV datasets in the Bronze
layer:

Dataset                             Description

suppliers.csv                     Supplier details, locations, and
ratings

purchase_orders.csv               Purchase order dates, quantities,
promised delivery dates, and actual
delivery dates

inventory.csv                     SKU-level inventory, warehouse
information, and reorder levels

production.csv                    Production output, downtime hours,
and downtime reasons

logistics.csv                     Shipment cost, transport mode, and
transit delays

sales_forecast.csv                Historical demand and forecasted
demand

Data Architecture

                SUPPLY CHAIN CSV FILES
                          │
                          ▼
                 ┌─────────────────┐
                 │  BRONZE LAYER   │
                 │    Raw Data     │
                 │ Original CSVs   │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │  SILVER LAYER   │
                 │ Processed Data  │
                 │ Cleaned and     │
                 │ standardized    │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │   GOLD LAYER    │
                 │  Joined Tables  │
                 │ Business-ready  │
                 │ analytical data │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │     POWER BI    │
                 │ Executive       │
                 │ Dashboard       │
                 └─────────────────┘

Bronze Layer --- Raw Data

The Bronze layer contains the original source datasets in their raw
form. These files represent the operational data collected from
different supply-chain processes.

Silver Layer --- Processed Data

The Silver layer contains the processed versions of the Bronze datasets.
Data is cleaned and standardized so that it is suitable for downstream
analysis and modeling.

Gold Layer --- Joined Business Tables

The Gold layer contains joined and business-ready tables created from
the processed Silver-layer data. This layer brings related supply-chain
data together so that Power BI can calculate KPIs and support
cross-functional analysis.

The Gold layer is therefore the primary analytical layer consumed by the
Power BI dashboard.


📌 Key KPIs

The dashboard provides four primary executive KPIs:

1. Total Logistics Cost

Measures the overall logistics/shipment cost across the selected data.

Current overall dashboard value: 1.75M

2. Total Downtime Hours

Measures accumulated production downtime.

Current overall dashboard value: 2.38K hours

3. Total Orders

Shows the number of purchase orders represented in the selected data.

Current overall dashboard value: 800 orders

4. Average Delivery Delay Days

Measures the average difference between promised and actual delivery.

Current overall dashboard value: 3.37 days

All KPI values respond dynamically to dashboard filters.

📈 Dashboard Visuals

Total Orders by Year

A yearly trend showing how the number of orders changes over time.

Observed values in the overall dashboard:

Year   Orders

2019      112
2020      140
2021      130
2022      132
2023      142
2024      144

The dashboard shows an overall upward movement in order volume, with
2024 having the highest displayed order count.

Total Downtime Hours by Downtime Reason

This visualization breaks production downtime down by cause.

Downtime Reason       Hours

Maintenance             544
Material Shortage       515
Labor Issue             479
None                    420
Machine Failure         419

Key observation: Maintenance and material shortages are the two
largest downtime categories in the displayed dataset.

Average Delivery Delay Days by Supplier

The supplier comparison helps identify suppliers with relatively high or
low delivery delays.

The overall dashboard shows supplier-level average delays ranging
approximately from 2.89 to 4.33 days.

Examples:

Supplier        Avg. Delivery Delay

Supplier_10               4.33 days
Supplier_8                3.65 days
Supplier_2                3.57 days
Supplier_4                3.43 days
Supplier_9                3.47 days
Supplier_5                3.11 days
Supplier_3                3.02 days
Supplier_7                2.98 days
Supplier_1                2.89 days

This enables procurement teams to identify suppliers that may require
delivery-performance improvement.

Total Forecasted Demand vs Total Historical Demand

The demand visualization compares historical demand with forecasted
demand by year.

This provides a high-level view of demand evolution and helps identify
periods where forecasted demand differs from historical demand.

🎛️ Interactive Filters

The dashboard includes slicers for:

SKU

Year

Supplier Name

These filters allow users to move from an organization-wide view to a
more targeted analysis.

For example, users can select one or more suppliers and immediately
evaluate:

Order volume

Average delivery delay

Logistics cost

Downtime

Demand trends

🔍 Example Filtered Analysis

The filtered dashboard demonstrates how the report changes dynamically
based on selections.

For the displayed supplier selection:

Supplier        Avg. Delivery Delay   Total Orders

Supplier_10               3.71 days             17
Supplier_3                3.06 days             16
Total                     3.39 days             33

The filtered KPI cards also update to reflect the selected data.

💡 Business Questions Answered

The dashboard is designed around practical supply-chain decision-making:

Supplier Performance

Which suppliers experience the highest delivery delays?

Which suppliers handle the largest number of orders?

Are certain suppliers consistently underperforming?

Procurement

How is order volume changing over time?

Which suppliers contribute significantly to purchasing activity?

Where could supplier performance improvement have the greatest
impact?

Production

What are the largest sources of downtime?

Is maintenance a major contributor to lost production time?

Are material shortages creating significant operational disruption?

Logistics

What is the total logistics expenditure?

How does logistics cost change with the selected supplier, SKU, or
year?

Are delivery delays creating potential supply-chain risk?

Demand Planning

How does forecasted demand compare with historical demand?

Are demand levels increasing or decreasing across years?

Which periods may require closer inventory and procurement planning?

🧮 Analytical Measures

Typical business metrics represented in the dashboard include:

Total Logistics Cost
= SUM(Logistics Shipment Cost)

Total Downtime Hours
= SUM(Production Downtime Hours)

Total Orders
= COUNT / COUNTROWS(Purchase Orders)

Average Delivery Delay Days
= AVERAGE(Actual Delivery Date - Promised Delivery Date)

Historical Demand
= SUM(Historical Demand)

Forecasted Demand
= SUM(Forecasted Demand)

The exact implementation can vary depending on the final Gold-layer
schema and Power BI model.

🛠️ Tools & Technologies

Power BI --- dashboarding, interactive reporting, KPI
visualization

CSV --- source datasets

Data transformation / modeling --- preparation of analytical
Gold-layer data

Power BI data model / DAX --- analytical measures and dynamic
KPIs

📁 Suggested Repository Structure

supply-chain-dashboard/
│
├── README.md
│
├── data/
│   ├── bronze/
│   │   └── <bronze-layer-files>
│   │
│   └── silver/
|   |   └── <silver-layer-files>
│   |
│   └── gold/
│       └── <gold-layer-files>
├── powerbi/
│   └── supply_chain_dashboard.pbix
│
└── images/
    ├── dashboard_overview.png
    └── dashboard_filtered.png

🚀 How to Use

Open the Power BI .pbix file.

Refresh the data model if the source files have changed.

Use the SKU, Year, and Supplier Name slicers to filter
the report.

Review the KPI cards for the selected scope.

Analyze yearly order trends.

Compare downtime reasons.

Evaluate supplier delivery performance.

Compare forecasted and historical demand.

📊 Executive Takeaways

Based on the overall dashboard view:

800 orders are represented in the displayed dataset.

Total logistics cost is approximately 1.75M.

Total production downtime is approximately 2.38K hours.

Average delivery delay is approximately 3.37 days.

Maintenance is the largest displayed downtime category at 544
hours.

Material Shortage is the second-largest downtime category at
515 hours.

Supplier_10 has the highest displayed average delivery delay at
4.33 days.

Supplier_1 has the lowest displayed average delivery delay at
2.89 days.

Order volume reaches its highest displayed level in 2024 with 144
orders.

These metrics can be used as a starting point for deeper root-cause
analysis and supply-chain optimization.

🔮 Potential Future Enhancements

Possible extensions to the project include:

Supplier risk scoring

Inventory stockout and reorder analysis

OTIF (On-Time In-Full) analysis

Purchase-order lead-time analysis

Logistics cost by transport mode

Forecast accuracy metrics such as MAPE

Supplier rating vs delivery-performance analysis

Inventory turnover analysis

Downtime cost estimation

Automated alerts for high delivery delays or low inventory

Drill-through pages for SKU and supplier-level investigation

👤 Project

Supply Chain Analytics & Executive Dashboard

Built to demonstrate end-to-end supply-chain data analysis, business KPI
development, data modeling, and executive reporting using Power BI.