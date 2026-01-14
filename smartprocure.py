import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="SmartProcure AI", layout="wide")
st.title("🤖 SmartProcure AI – Autonomous Strategic Sourcing Platform")
st.markdown("AI-driven Procurement | Supplier Intelligence | Optimization | Negotiation Agent")

# -------------------------
# Mock LLM Negotiation Engine
# -------------------------
def mock_gpt_negotiation(supplier, offer, target):
    if offer <= target:
        return f"""
        🟢 Decision: Accept Offer  
        Supplier: {supplier}  
        Final Price: {offer}  
        Strategy: Long-term contract with volume commitment  
        SLA: 98% OTIF, Defect <0.5%  
        Risk Clause: Dual sourcing if risk > 20%
        """
    else:
        return f"""
        🟠 Decision: Counter Offer  
        Supplier: {supplier}  
        Counter Price: {target}  
        Strategy: Longer tenure + higher volume to reduce cost  
        SLA: 97% OTIF, Penalty 1% per delay day  
        Risk Clause: Backup supplier activation
        """

# -------------------------
# 1. Supplier Data Lake
# -------------------------
st.header("1️⃣ Supplier Data Lake")

data_source = st.radio("Select Data Source", ["Upload CSV", "Use Demo Dataset"])

df = None  # Initialize to avoid NameError

if data_source == "Upload CSV":
    uploaded_file = st.file_uploader("Upload Supplier KPI Dataset (CSV)", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)

else:
    df = pd.DataFrame({
        "Supplier": ["Alpha Ltd", "Beta Corp", "Gamma Inc", "Delta Pvt"],
        "Cost": [95, 102, 98, 110],
        "Quality": [0.92, 0.89, 0.94, 0.87],
        "Delivery": [0.95, 0.91, 0.93, 0.88],
        "Risk": [0.15, 0.25, 0.18, 0.30]
    })

# Proceed only if df exists
if df is not None:

    st.subheader("📂 Supplier Data Lake")
    st.dataframe(df)

    # -------------------------
    # 2. MCDA Supplier Ranking
    # -------------------------
    st.header("2️⃣ Dynamic Supplier Ranking (MCDA)")

    w_cost = st.slider("Cost Weight", 0.0, 1.0, 0.25)
    w_quality = st.slider("Quality Weight", 0.0, 1.0, 0.25)
    w_delivery = st.slider("Delivery Weight", 0.0, 1.0, 0.25)
    w_risk = st.slider("Risk Weight", 0.0, 1.0, 0.25)

    df["Score"] = (
        w_cost * (1 / df["Cost"]) +
        w_quality * df["Quality"] +
        w_delivery * df["Delivery"] +
        w_risk * (1 / df["Risk"])
    )

    ranked_df = df.sort_values("Score", ascending=False)
    st.dataframe(ranked_df)

    # -------------------------
    # 3. Executive Dashboard
    # -------------------------
    st.header("📊 Executive Procurement Dashboard")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Avg Cost", round(df["Cost"].mean(), 2))
    col2.metric("Avg Quality", round(df["Quality"].mean(), 2))
    col3.metric("Avg Delivery", round(df["Delivery"].mean(), 2))
    col4.metric("Avg Risk", round(df["Risk"].mean(), 2))

    fig_score = px.bar(ranked_df, x="Supplier", y="Score", title="Supplier Performance Score")
    st.plotly_chart(fig_score, use_container_width=True)

    fig_risk = px.scatter(ranked_df, x="Cost", y="Risk", size="Score", color="Supplier",
                          title="Cost vs Risk Portfolio")
    st.plotly_chart(fig_risk, use_container_width=True)

    # -------------------------
    # 4. Risk Forecast
    # -------------------------
    st.header("3️⃣ AI Disruption Risk Forecast")

    ranked_df["Disruption_Probability"] = np.random.uniform(0.05, 0.3, len(ranked_df))
    st.dataframe(ranked_df[["Supplier", "Disruption_Probability"]])

    # -------------------------
    # 5. Order Allocation Optimization
    # -------------------------
    st.header("4️⃣ Optimal Order Allocation")

    total_demand = st.number_input("Total Demand Quantity", 100, 10000, 1000)
    ranked_df["Allocation"] = (ranked_df["Score"] / ranked_df["Score"].sum()) * total_demand
    st.dataframe(ranked_df[["Supplier", "Allocation"]])

    fig_alloc = px.pie(ranked_df, names="Supplier", values="Allocation",
                       title="AI-Based Order Allocation")
    st.plotly_chart(fig_alloc, use_container_width=True)

    # -------------------------
    # 6. Negotiation Agent
    # -------------------------
    st.header("5️⃣ AI Negotiation Agent (LLM Simulated)")

    supplier = st.selectbox("Select Supplier for Negotiation", ranked_df["Supplier"])
    offer = st.number_input("Supplier Offered Price", value=100.0)
    target = st.number_input("Your Target Price", value=95.0)

    if st.button("Run AI Negotiation"):
        result = mock_gpt_negotiation(supplier, offer, target)
        st.success("🧠 Negotiation Strategy Generated")
        st.write(result)

    # -------------------------
    # 7. Smart Purchase Order Generator
    # -------------------------
    st.header("6️⃣ Smart Purchase Order Generator")

    if st.button("Generate Smart PO"):
        po_text = f"""
        SMARTPROCURE AI – PURCHASE ORDER

        Supplier: {supplier}
        Quantity: {int(total_demand*0.4)}
        Target Price: ₹{target}
        SLA: 98% On-Time Delivery
        Quality: <0.5% Defect Rate
        Payment Terms: Net 30
        Penalty: 1% per day delay
        Risk Clause: Dual sourcing if disruption probability > 20%
        """
        st.text_area("Auto-Generated PO", po_text, height=300)

    # -------------------------
    # 8. Scenario Simulation
    # -------------------------
    st.header("7️⃣ What-if Scenario Simulation")

    disruption = st.slider("Simulate Disruption Level (%)", 0, 50, 10)
    ranked_df["Adjusted_Risk"] = ranked_df["Risk"] * (1 + disruption / 100)
    st.dataframe(ranked_df[["Supplier", "Adjusted_Risk"]])
