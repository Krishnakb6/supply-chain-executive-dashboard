# Supply Chain & Manufacturing Analytics Platform

An end-to-end supply chain analytics project combining Databricks, dbt, Medallion Architecture, Power BI, Machine Learning, Streamlit, and a Gemini-powered AI assistant.

## Live Demo

[Open the deployed Streamlit application](https://supply-chain-executive-dashboardgit-5hkwf72ebxr2pgphedbjad.streamlit.app/)

The deployed app may require Streamlit authentication. The Gemini AI Assistant
also requires `GEMINI_API_KEY` to be configured in the deployment secrets.

## Overview

The platform transforms raw operational data into analytical datasets, interactive business dashboards, supplier delivery-risk predictions, and a natural-language analytics interface.

```text
Raw CSV Files
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
     +------------------+
     |                  |
     v                  v
 Power BI          Machine Learning
                        |
                        v
                   Streamlit
                        |
                        v
                  Gemini AI
```

## Data Sources

| Dataset | Description |
|---|---|
| `suppliers.csv` | Supplier details, location, and ratings |
| `purchase_orders.csv` | Purchase orders, quantities, promised/actual delivery information |
| `inventory.csv` | SKU-level inventory, warehouse stock, and reorder information |
| `production.csv` | Production output, downtime hours, and downtime reasons |
| `logistics.csv` | Shipment cost, transport mode, and transit delays |
| `sales_forecast.csv` | Historical demand and forecasted demand |
| `calendar.csv` | Date dimension |

The source data covers 2019–2025.

## Data Engineering

### Databricks

Databricks is used as the primary data engineering environment. Raw CSV data is ingested into the Bronze layer and transformed through dbt into Silver and Gold analytical datasets.

### Medallion Architecture

**Bronze**
- Raw source data
- Minimal transformation
- Source traceability

**Silver**
- Cleaned and standardized datasets
- Data type handling
- Preparation for downstream analytics

**Gold**

```text
dim_calendar
dim_product
dim_suppliers
dim_warehouse

fact_inventory
fact_logistics
fact_production
fact_purchase
fact_sales_forecast
```

The Gold layer is designed for reporting, analytics, and Machine Learning use cases.

## dbt

dbt manages SQL transformations and dependencies between Silver and Gold models using `ref()`.

Example:

```sql
select
    s.supplier_name,
    s.location,
    s.rating,
    po.quantity,
    po.lead_time_days,
    po.delivery_delay_days,
    po.sku,
    po.order_date,
    po.supplier_id
from {{ ref('silver_purchase_orders') }} po
left join {{ ref('silver_supplier') }} s
    on po.supplier_id = s.supplier_id
```

## Power BI

Power BI provides the business-facing analytics layer covering:

- Supplier performance
- Inventory
- Production
- Logistics
- Sales forecasting
- Purchase orders

The report is embedded in the Streamlit application.

See [powerbi/Readme.md](powerbi/Readme.md) for Power BI documentation.

## Machine Learning

The project includes a Random Forest classification model that predicts whether a purchase order is likely to be delivered late.

Target:

```text
is_late = 1  -> Late
is_late = 0  -> Not Late
```

The target is derived from:

```text
delivery_delay_days > 0
```

`delivery_delay_days` is excluded from model inputs because it represents the outcome and would cause target leakage.

### Features

```text
supplier_id
location
rating
quantity
lead_time_days
sku
order_year
order_month
order_quarter
order_day_of_week
```

### Current Results

| Metric | Result |
|---|---:|
| Accuracy | 76.25% |
| Late-class Precision | 80% |
| Late-class Recall | 91% |
| Late-class F1 | 85% |
| Weighted F1 | 74% |

The late class is the primary business focus, making recall and F1 particularly important.

### Risk Rules

| Late Probability | Risk |
|---|---|
| 0–40% | Low |
| 40–70% | Medium |
| 70–100% | High |

These are business-defined thresholds, not learned model thresholds.

See [ml/Readme.md](ml/Readme.md) for the complete ML documentation.

The reproducible notebook is `ml/supplier_delay_prediction_fixed.ipynb`. It
reads `ml/ml_purchase_order_features.csv` and writes the prediction output to
both locations below:

```text
app/supplier_delay_predictions.csv
ml/supplier_delay_predictions.csv
```

## Streamlit Application

The Streamlit application contains:

```text
Power BI Dashboard
Supplier Risk
AI Assistant
```

### Supplier Risk

The risk page provides:

- Total orders
- Predicted late orders
- High-risk orders
- Average late probability
- Risk distribution
- Supplier-level risk analysis
- Purchase-order risk table

### AI Assistant

The AI Assistant uses the Gemini API to answer natural-language questions using the Machine Learning prediction dataset as context.

Example questions:

```text
Why is S007 SKU0014 high risk?
What can you tell me about supplier S007?
Which orders are high risk?
Why does this order have a high late probability?
What action should we take for high-risk orders?
```

The assistant is instructed to distinguish between model predictions, observed information, and business recommendations.

## Project Structure

```text
Supply_Chain_Project/
│
├── app/
│   ├── app.py
│   ├── supplier_delay_predictions.csv
│   └── .streamlit/
│       └── secrets.toml
│
├── ml/
│   ├── Readme.md
│   ├── supplier_delay_prediction_fixed.ipynb
│   ├── ml_purchase_order_features.csv
│   └── supplier_delay_predictions.csv
│
├── powerbi/
│   ├── Readme.md
│   └── Screenshots/
│
├── Supply_Chain_Project/
│   ├── dbt_project.yml
│   ├── profiles.yml
│   └── models/
│
├── src/
│   └── supply_chain_project/
│
├── README.md
└── .gitignore
```

Never commit `app/.streamlit/secrets.toml` or any API key.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | ML and application development |
| Pandas | Data manipulation |
| Scikit-learn | Machine Learning |
| Random Forest | Delivery-risk classification |
| Databricks | Data engineering |
| dbt | SQL transformations |
| Power BI | Business intelligence |
| Streamlit | Application interface |
| Gemini API | AI assistant |
| GitHub | Version control and documentation |

## Business Value

The platform supports:

- Earlier identification of supplier delivery risks
- Supplier performance monitoring
- Proactive purchase-order management
- Centralized supply chain visibility
- Data-driven prioritization of high-risk orders
- Natural-language access to analytical information

The ML component extends the platform from descriptive analytics toward predictive analytics.

## Limitations

- Relatively small dataset
- Imbalanced target classes
- Limited operational features
- Initial model without extensive hyperparameter tuning
- Manually defined risk thresholds
- Current AI Assistant uses the prediction CSV as context
- Current Power BI embedding depends on report authentication/access

## Future Enhancements

- Hyperparameter tuning
- Cross-validation
- Feature importance and SHAP explanations
- Time-aware model validation
- Real-time data pipelines
- Direct Gold-layer integration
- Automated high-risk alerts
- Supplier optimization
- More advanced AI data querying
- Cloud deployment

## Getting Started

```bash
git clone <your-github-repository-url>
cd Supply_Chain_Project

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt

streamlit run app/app.py
```

To run the ML notebook, open `ml/supplier_delay_prediction_fixed.ipynb` in
VS Code, select the `.venv` Python interpreter, and run the cells in order.

The app expects the prediction CSV at
`app/supplier_delay_predictions.csv`. The AI Assistant also requires a
Gemini API key configured through Streamlit secrets.

Create `app/.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

Never commit this file.

## Author

Krishna Kiriti

Supply Chain Analytics | Data Engineering | Business Intelligence | Machine Learning
