import time

import streamlit as st
import pandas as pd
from google import genai
import re


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Supply Chain Analytics",
    layout="wide"
)


# ============================================================
# LOAD ML PREDICTIONS
# ============================================================

@st.cache_data
def load_predictions():
    return pd.read_csv(
        r"app/supplier_delay_predictions.csv"
    )


try:
    df = load_predictions()
except FileNotFoundError:
    df = None


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("Supply Chain")

page = st.sidebar.radio(
    "Navigate",
    [
        "Power BI Dashboard",
        "Supplier Risk",
        "AI Assistant"
    ]
)


# ============================================================
# PAGE 1 — POWER BI DASHBOARD
# ============================================================

if page == "Power BI Dashboard":

    st.title("Supply Chain Analytics Dashboard")

    st.markdown(
        """
        ### Interactive Power BI Dashboard

        Explore supplier performance, inventory, production,
        logistics and forecasting insights.
        """
    )

    st.divider()

    POWER_BI_URL = (
        "https://app.powerbi.com/reportEmbed?"
        "reportId=0e62e4ee-58cf-47f9-a88e-782df338c611"
        "&autoAuth=true"
        "&ctid=d4963ce2-af94-4122-95a9-644e8b01624d"
    )

    st.iframe(
        POWER_BI_URL,
        height=800
    )


# ============================================================
# PAGE 2 — SUPPLIER RISK
# ============================================================

elif page == "Supplier Risk":

    st.title("Supplier Delivery Risk")

    st.markdown(
        """
        Machine Learning powered prediction of purchase-order
        delivery risk.
        """
    )

    if df is None:

        st.error(
            "supplier_delay_predictions.csv was not found. "
            "Please place it inside the app folder."
        )

        st.stop()

    # --------------------------------------------------------
    # DATA PREPARATION
    # --------------------------------------------------------

    df["late_probability"] = pd.to_numeric(
        df["late_probability"],
        errors="coerce"
    )

    df["late_probability_pct"] = (
        df["late_probability"] * 100
    )

    # --------------------------------------------------------
    # KPI CALCULATIONS
    # --------------------------------------------------------

    total_orders = len(df)

    predicted_late = (
        df["predicted_is_late"] == 1
    ).sum()

    high_risk = (
        df["risk_level"] == "High"
    ).sum()

    average_probability = (
        df["late_probability"].mean() * 100
    )

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Orders",
            total_orders
        )

    with col2:
        st.metric(
            "Predicted Late Orders",
            predicted_late
        )

    with col3:
        st.metric(
            "High Risk Orders",
            high_risk
        )

    with col4:
        st.metric(
            "Average Late Probability",
            f"{average_probability:.1f}%"
        )

    st.divider()

    # --------------------------------------------------------
    # RISK DISTRIBUTION
    # --------------------------------------------------------

    st.subheader("Risk Distribution")

    risk_counts = (
        df["risk_level"]
        .value_counts()
        .reindex(
            ["Low", "Medium", "High"]
        )
        .fillna(0)
    )

    col1, col2 = st.columns(2)

    with col1:

        st.bar_chart(risk_counts)

    with col2:

        st.dataframe(
            risk_counts.reset_index(),
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # --------------------------------------------------------
    # SUPPLIER RISK
    # --------------------------------------------------------

    st.subheader("Supplier Risk Analysis")

    supplier_risk = (
        df.groupby("supplier_id")
        .agg(
            orders=("supplier_id", "count"),
            avg_late_probability=(
                "late_probability",
                "mean"
            )
        )
        .reset_index()
    )

    supplier_risk["avg_late_probability"] = (
        supplier_risk["avg_late_probability"] * 100
    )

    supplier_risk = supplier_risk.sort_values(
        "avg_late_probability",
        ascending=False
    )

    st.bar_chart(
        supplier_risk.set_index(
            "supplier_id"
        )["avg_late_probability"]
    )

    st.divider()

    # --------------------------------------------------------
    # ORDER RISK TABLE
    # --------------------------------------------------------

    st.subheader("Purchase Order Risk")

    display_columns = [
        "supplier_id",
        "sku",
        "quantity",
        "lead_time_days",
        "late_probability_pct",
        "risk_level"
    ]

    available_columns = [
        column
        for column in display_columns
        if column in df.columns
    ]

    risk_table = df[
        available_columns
    ].copy()

    if "late_probability_pct" in risk_table.columns:

        risk_table["late_probability_pct"] = (
            risk_table["late_probability_pct"].round(1)
        )

    st.dataframe(
        risk_table.sort_values(
            "late_probability_pct",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# PAGE 3 — AI ASSISTANT
# ============================================================

elif page == "AI Assistant":

    st.title("AI Supply Chain Assistant")

    st.markdown(
        """
        Ask questions about suppliers, purchase orders,
        delivery risk and Machine Learning predictions.
        """
    )

    st.divider()

    # --------------------------------------------------------
    # CHECK DATA
    # --------------------------------------------------------

    if df is None:

        st.error(
            "supplier_delay_predictions.csv was not found."
        )

        st.stop()

    # --------------------------------------------------------
    # INITIALIZE GEMINI
    # --------------------------------------------------------

    try:

        client = genai.Client(
            api_key=st.secrets["GEMINI_API_KEY"]
        )

    except Exception:

        st.error(
            "Gemini API key is not configured. "
            "Add GEMINI_API_KEY to the Streamlit Cloud Secrets."
        )

        st.stop()

    # --------------------------------------------------------
    # QUESTION INPUT
    # --------------------------------------------------------

    question = st.text_input(
        "Ask a supply-chain question:",
        placeholder="Which risk level has the most orders?"
    )

    if question:

        question_lower = question.lower()

        # ----------------------------------------------------
        # IDENTIFY SUPPLIER AND SKU
        # ----------------------------------------------------

        supplier_matches = [
            supplier
            for supplier in df["supplier_id"].astype(str).unique()
            if supplier.lower() in question_lower
        ]

        sku_matches = [
            sku
            for sku in df["sku"].astype(str).unique()
            if sku.lower() in question_lower
        ]

        # ----------------------------------------------------
        # OVERALL DATA SUMMARY
        # ----------------------------------------------------

        total_orders = len(df)

        risk_distribution = (
            df["risk_level"]
            .value_counts()
            .reindex(["Low", "Medium", "High"])
            .fillna(0)
            .astype(int)
        )

        risk_percentages = (
            risk_distribution / total_orders * 100
        ).round(1)

        average_late_probability = (
            df["late_probability"].mean() * 100
        )

        predicted_late_orders = (
            df["predicted_is_late"] == 1
        ).sum()

        # ----------------------------------------------------
        # SUPPLIER SUMMARY
        # ----------------------------------------------------

        supplier_summary = (
            df.groupby("supplier_id")
            .agg(
                orders=("supplier_id", "count"),
                average_late_probability=(
                    "late_probability",
                    "mean"
                ),
                high_risk_orders=(
                    "risk_level",
                    lambda x: (x == "High").sum()
                ),
                medium_risk_orders=(
                    "risk_level",
                    lambda x: (x == "Medium").sum()
                ),
                low_risk_orders=(
                    "risk_level",
                    lambda x: (x == "Low").sum()
                )
            )
            .reset_index()
        )

        supplier_summary["average_late_probability"] = (
            supplier_summary["average_late_probability"] * 100
        ).round(1)

        supplier_summary = supplier_summary.sort_values(
            "average_late_probability",
            ascending=False
        )

        # ----------------------------------------------------
        # SKU SUMMARY
        # ----------------------------------------------------

        sku_summary = (
            df.groupby("sku")
            .agg(
                orders=("sku", "count"),
                average_late_probability=(
                    "late_probability",
                    "mean"
                ),
                high_risk_orders=(
                    "risk_level",
                    lambda x: (x == "High").sum()
                ),
                medium_risk_orders=(
                    "risk_level",
                    lambda x: (x == "Medium").sum()
                ),
                low_risk_orders=(
                    "risk_level",
                    lambda x: (x == "Low").sum()
                )
            )
            .reset_index()
        )

        sku_summary["average_late_probability"] = (
            sku_summary["average_late_probability"] * 100
        ).round(1)

        sku_summary = sku_summary.sort_values(
            "average_late_probability",
            ascending=False
        )

        # ----------------------------------------------------
        # TOP RISK ORDERS
        # ----------------------------------------------------

        top_risk_orders = (
            df.sort_values(
                "late_probability",
                ascending=False
            )
            .head(10)
            .copy()
        )

        top_risk_orders["late_probability"] = (
            top_risk_orders["late_probability"] * 100
        ).round(1)

        # ----------------------------------------------------
        # DETERMINE RELEVANT DATA
        # ----------------------------------------------------

        relevant_df = df.copy()

        # Specific supplier question
        if supplier_matches:

            relevant_df = relevant_df[
                relevant_df["supplier_id"]
                .astype(str)
                .isin(supplier_matches)
            ]

        # Specific SKU question
        if sku_matches:

            relevant_df = relevant_df[
                relevant_df["sku"]
                .astype(str)
                .isin(sku_matches)
            ]

        # ----------------------------------------------------
        # BUILD CONTEXT FOR GEMINI
        # ----------------------------------------------------

        context_parts = []

        # Overall statistics

        context_parts.append(
            f"""
OVERALL DATA SUMMARY

Total purchase orders: {total_orders}

Risk distribution:
Low: {risk_distribution["Low"]} orders ({risk_percentages["Low"]}%)
Medium: {risk_distribution["Medium"]} orders ({risk_percentages["Medium"]}%)
High: {risk_distribution["High"]} orders ({risk_percentages["High"]}%)

Average late probability:
{average_late_probability:.1f}%

Predicted late orders:
{predicted_late_orders}
"""
        )

        # ----------------------------------------------------
        # SUPPLIER INFORMATION
        # ----------------------------------------------------

        if supplier_matches:

            selected_suppliers = supplier_summary[
                supplier_summary["supplier_id"]
                .astype(str)
                .isin(supplier_matches)
            ]

            context_parts.append(
                """
SELECTED SUPPLIER INFORMATION

""" +
                selected_suppliers.to_string(index=False)
            )

        else:

            context_parts.append(
                """
SUPPLIER RISK SUMMARY

""" +
                supplier_summary.head(10).to_string(index=False)
            )

        # ----------------------------------------------------
        # SKU INFORMATION
        # ----------------------------------------------------

        if sku_matches:

            selected_skus = sku_summary[
                sku_summary["sku"]
                .astype(str)
                .isin(sku_matches)
            ]

            context_parts.append(
                """
SELECTED SKU INFORMATION

""" +
                selected_skus.to_string(index=False)
            )

        else:

            context_parts.append(
                """
SKU RISK SUMMARY

""" +
                sku_summary.head(10).to_string(index=False)
            )

        # ----------------------------------------------------
        # SPECIFIC ORDER DATA
        # ----------------------------------------------------

        if supplier_matches or sku_matches:

            context_parts.append(
                """
RELEVANT PURCHASE ORDERS

""" +
                relevant_df.head(20).to_string(index=False)
            )

        # ----------------------------------------------------
        # TOP RISK ORDERS
        # ----------------------------------------------------

        context_parts.append(
            """
TOP 10 HIGHEST-RISK PURCHASE ORDERS

""" +
            top_risk_orders.to_string(index=False)
        )

        context = "\n\n".join(context_parts)

        # ----------------------------------------------------
        # AI PROMPT
        # ----------------------------------------------------

        prompt = f"""
You are a Supply Chain Analytics Assistant.

You are answering questions about a supply-chain
Machine Learning prediction dataset.

Use ONLY the information provided in the analytical
context below.

IMPORTANT RULES:

1. Do not invent facts.
2. Do not assume information that is not provided.
3. Use the calculated statistics in the context when
   answering numerical questions.
4. If the question asks for a count, percentage,
   comparison, ranking, or average, use the calculated
   values provided by the application.
5. Clearly distinguish between:
   - Model prediction
   - Observed information in the dataset
   - Business recommendation
6. If the available information is insufficient,
   explicitly say so.
7. Keep the answer concise and business-oriented.
8. If a supplier or SKU is mentioned, focus on that
   supplier or SKU.
9. If the user asks about Low, Medium, or High risk,
   use the complete risk distribution provided below.
10. Do not claim that a risk category does not exist
    unless the calculated risk distribution shows zero
    records for that category.

ANALYTICAL CONTEXT:

{context}

USER QUESTION:

{question}

Provide a clear answer based on the analytical context.
"""

        # ----------------------------------------------------
        # CALL GEMINI
        # ----------------------------------------------------

        with st.spinner("Analyzing supply-chain data..."):

            response = None

            for attempt in range(3):

                try:

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt
                    )

                    break

                except Exception as e:

                    error_message = str(e)

                    if (
                        "503" in error_message
                        or "UNAVAILABLE" in error_message
                    ):

                        if attempt < 2:

                            import time
                            time.sleep(3)

                        else:

                            st.error(
                                "Gemini is temporarily unavailable. "
                                "Please try again shortly."
                            )

                            st.stop()

                    else:

                        st.error(
                            f"Gemini API error: {error_message}"
                        )

                        st.stop()

        # ----------------------------------------------------
        # DISPLAY ANSWER
        # ----------------------------------------------------

        st.subheader("Analysis")

        st.write(response.text)

        # ----------------------------------------------------
        # SHOW CALCULATED SUMMARY
        # ----------------------------------------------------

        with st.expander("View analytical summary"):

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Total Orders",
                    total_orders
                )

            with col2:
                st.metric(
                    "Low Risk",
                    int(risk_distribution["Low"])
                )

            with col3:
                st.metric(
                    "Medium Risk",
                    int(risk_distribution["Medium"])
                )

            with col4:
                st.metric(
                    "High Risk",
                    int(risk_distribution["High"])
                )

            st.subheader("Risk Distribution")

            risk_display = pd.DataFrame(
                {
                    "Risk Level": [
                        "Low",
                        "Medium",
                        "High"
                    ],
                    "Orders": [
                        int(risk_distribution["Low"]),
                        int(risk_distribution["Medium"]),
                        int(risk_distribution["High"])
                    ],
                    "Percentage": [
                        f'{risk_percentages["Low"]:.1f}%',
                        f'{risk_percentages["Medium"]:.1f}%',
                        f'{risk_percentages["High"]:.1f}%'
                    ]
                }
            )

            st.dataframe(
                risk_display,
                use_container_width=True,
                hide_index=True
            )

        # ----------------------------------------------------
        # SHOW DATA USED
        # ----------------------------------------------------

        with st.expander("View relevant data"):

            if supplier_matches or sku_matches:

                st.dataframe(
                    relevant_df,
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.dataframe(
                    top_risk_orders,
                    use_container_width=True,
                    hide_index=True
                )