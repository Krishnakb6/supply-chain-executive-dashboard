# Machine Learning - Supplier Delivery Risk Prediction

This module extends the Supply Chain & Manufacturing Analytics Platform with a Machine Learning model that predicts whether a purchase order is likely to be delivered late.

The current workflow is in `supplier_delay_prediction_fixed.ipynb`. It reads
the feature dataset in this folder and writes matching prediction files to
both the `ml/` and `app/` folders.

## Objective

The problem is formulated as binary classification:

```text
Will this purchase order be delivered late?
```

Target:

```text
is_late = 1  -> Late
is_late = 0  -> Not Late
```

The target is derived from:

```text
delivery_delay_days > 0
```

A negative delay indicates an early delivery, zero indicates on-time delivery, and a positive delay indicates a late delivery.

## Dataset

The ML feature dataset contains approximately 800 purchase orders and includes:

```text
supplier_id
location
rating
quantity
lead_time_days
sku
order_date
order_year
order_month
order_quarter
order_day_of_week
delivery_delay_days
is_late
```

The data covers 2019–2025.

## Features

The model uses:

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

`delivery_delay_days` is deliberately excluded because it directly describes the delivery outcome and would introduce target leakage.

## Workflow

```text
Purchase Order Data
        |
        v
Supplier Enrichment
        |
        v
Feature Preparation
        |
        v
Target Creation
        |
        v
Categorical Encoding
        |
        v
80/20 Stratified Split
        |
        v
Random Forest Classifier
        |
        v
Late Probability
        |
        v
Risk Category
```

Categorical variables are encoded with OneHotEncoder.

## Model

The initial model is a Random Forest Classifier.

Random Forest was selected as a practical baseline because it can capture nonlinear relationships and interactions while working well with mixed numerical and categorical-derived features.

The model produces:

```text
predicted_is_late
late_probability
```

## Evaluation

Current test-set results:

| Metric | Result |
|---|---:|
| Accuracy | 76.25% |
| Class 0 Precision | 61% |
| Class 0 Recall | 39% |
| Class 0 F1 | 47% |
| Class 1 Precision | 80% |
| Class 1 Recall | 91% |
| Class 1 F1 | 85% |
| Macro F1 | 66% |
| Weighted F1 | 74% |

The test set contains:

```text
44 non-late orders
116 late orders
```

The target is therefore imbalanced toward late orders.

## Business Interpretation

Accuracy alone is not sufficient for this use case.

The primary objective is to identify orders likely to be late.

The model achieves:

```text
91% recall for late orders
85% F1 for late orders
```

This supports proactive actions such as:

- Supplier follow-up
- Expediting
- Alternative sourcing
- Inventory planning
- Customer communication
- Prioritization of operational attention

## Risk Classification

| Late Probability | Risk Level |
|---|---|
| 0%–40% | Low |
| 40%–70% | Medium |
| 70%–100% | High |

These thresholds are business rules and are not learned by the model.

## Prediction Output

The model generates:

```text
supplier_delay_predictions.csv
```

Important fields include:

```text
supplier_id
sku
quantity
lead_time_days
late_probability
predicted_is_late
risk_level
```

The Streamlit application consumes this prediction dataset.

The notebook currently writes identical prediction files to both:

```text
app/supplier_delay_predictions.csv
ml/supplier_delay_predictions.csv
```

The app reads the copy in `app/`.

## Streamlit Integration

The prediction output powers the Supplier Risk page, which provides:

- Total order count
- Predicted late order count
- High-risk order count
- Average late probability
- Risk distribution
- Supplier-level risk analysis
- Purchase-order risk table

The same dataset is provided as context to the Gemini AI Assistant.

## AI Assistant

The architecture is:

```text
User Question
      |
      v
Streamlit
      |
      v
Relevant ML Prediction Records
      |
      v
Gemini API
      |
      v
Business Explanation
```

The assistant is instructed to:

- Use only supplied supply-chain data
- Avoid inventing facts
- Explain results in business language
- Distinguish predictions from observed information
- Separate recommendations from data
- State when information is insufficient

## Key Files

```text
ml/
├── README.md
├── ml_purchase_order_features.csv
├── supplier_delay_prediction_fixed.ipynb
└── supplier_delay_predictions.csv
```

The notebook covers data loading, feature preparation, encoding, train/test
splitting, Random Forest training, evaluation, predictions, risk
classification, and export to both application output locations.

## Run the Notebook

From the repository root:

```powershell
.\.venv\Scripts\Activate.ps1
jupyter notebook ml\supplier_delay_prediction_fixed.ipynb
```

Alternatively, open the notebook in VS Code and select the project `.venv`
kernel. Run the cells from top to bottom so that the model and prediction
outputs are created in the expected order.

## Limitations

- Relatively small dataset
- Imbalanced target classes
- Supplier and SKU identifiers are categorical features
- Limited operational features
- No extensive hyperparameter optimization
- No cross-validation in the initial implementation
- No formal probability calibration
- Manually selected risk thresholds
- Random train/test splitting may not fully represent future production performance

This should be considered a portfolio-level predictive prototype rather than a production decision system.

## Future Improvements

### Model

- Hyperparameter tuning
- Cross-validation
- Class-weight optimization
- Probability calibration
- Gradient Boosting comparison
- XGBoost/LightGBM comparison
- Business-cost-based threshold optimization

### Feature Engineering

Potential additions:

- Supplier historical late rate
- Historical average delay
- Supplier order frequency
- Rolling supplier performance
- Warehouse information
- Logistics transit performance
- Seasonal demand
- Inventory availability
- Production constraints

### Explainability

- Feature importance
- SHAP values
- Individual prediction explanations
- Supplier risk drivers

### Productionization

- Scheduled retraining
- Model monitoring
- Data drift monitoring
- Direct Databricks/Gold integration
- Automated high-risk alerts

## Summary

This module demonstrates an end-to-end predictive analytics workflow:

```text
Databricks
   |
   v
dbt
   |
   v
Purchase Order Features
   |
   v
Random Forest
   |
   v
Late Probability
   |
   v
Risk Level
   |
   v
Streamlit
   |
   v
Gemini AI Assistant
```

It extends the wider platform from descriptive supply chain analytics into predictive supplier risk management.
