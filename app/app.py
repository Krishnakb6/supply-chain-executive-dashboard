import time

import streamlit as st
import pandas as pd
from google import genai


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
            "Add GEMINI_API_KEY to app/.streamlit/secrets.toml"
        )

        st.stop()

    # --------------------------------------------------------
    # QUESTION INPUT
    # --------------------------------------------------------

    question = st.text_input(
        "Ask a supply-chain question:",
        placeholder="Why is S007 SKU0014 high risk?"
    )

    if question:

        # ----------------------------------------------------
        # FIND RELEVANT ORDER/SUPPLIER DATA
        # ----------------------------------------------------

        supplier_matches = [
            supplier
            for supplier in df["supplier_id"].astype(str).unique()
            if supplier.lower() in question.lower()
        ]

        sku_matches = [
            sku
            for sku in df["sku"].astype(str).unique()
            if sku.lower() in question.lower()
        ]

        # ----------------------------------------------------
        # FILTER RELEVANT DATA
        # ----------------------------------------------------

        relevant_df = df.copy()

        if supplier_matches:

            relevant_df = relevant_df[
                relevant_df["supplier_id"]
                .astype(str)
                .isin(supplier_matches)
            ]

        if sku_matches:

            relevant_df = relevant_df[
                relevant_df["sku"]
                .astype(str)
                .isin(sku_matches)
            ]

        # If no specific supplier or SKU was mentioned,
        # provide high-risk orders as context.

        if not supplier_matches and not sku_matches:

            relevant_df = relevant_df[
                relevant_df["risk_level"] == "High"
            ]

        # Limit context size

        relevant_df = relevant_df.head(10)

        # ----------------------------------------------------
        # CREATE CONTEXT
        # ----------------------------------------------------

        context = relevant_df.to_string(
            index=False
        )

        # ----------------------------------------------------
        # AI PROMPT
        # ----------------------------------------------------

        prompt = f"""
You are a Supply Chain Analytics Assistant.

Answer the user's question using ONLY the
supply-chain data provided below.

Do not invent facts that are not present in the data.

Explain the result in simple business language.

If discussing risk, clearly distinguish between:

1. Model prediction
2. Observed historical information
3. Business recommendation

If the available data is insufficient to answer the
question, clearly say that the available data is
insufficient rather than making up an answer.

Supply Chain Data:

{context}

User Question:

{question}
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

                    if "503" in error_message or "UNAVAILABLE" in error_message:

                        if attempt < 2:
                            time.sleep(3)
                        else:
                            st.error(
                                "Gemini is temporarily unavailable because "
                                "the model is experiencing high demand. "
                                "Please try again shortly."
                            )
                            st.stop()

                    else:

                        st.error(
                            f"Gemini API error: {error_message}"
                        )
                        st.stop()

            answer = response.text

        # ----------------------------------------------------
        # DISPLAY RESPONSE
        # ----------------------------------------------------

        st.subheader("Analysis")

        st.write(answer)

        # ----------------------------------------------------
        # SHOW DATA USED
        # ----------------------------------------------------

        with st.expander(
            "View data used for this answer"
        ):

            st.dataframe(
                relevant_df,
                use_container_width=True,
                hide_index=True
            )