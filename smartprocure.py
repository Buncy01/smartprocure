
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="SmartProcure AI", layout="wide")

st.title("🤖 SmartProcure AI – Autonomous Strategic Sourcing Platform")
st.markdown("AI-driven Procurement | Supplier Intelligence | Optimization | Negotiation Agent")

# -------------------------
# 1. Supplier Data Lake
# -------------------------
st.header("1️⃣ Supplier Data Lake")

uploaded_file = st.file_uploader("Upload Supplier KPI Dataset (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)

    # -------------------------
    # 2. Multi-Criteria Scoring
    # -------------------------
    st.header("2️⃣ Dynamic Supplier Ranking (MCDA)")

    weights = {
        "Cost": st.slider("Cost Weight", 0.0, 1.0, 0.25),
        "Quality": st.slider("Quality Weight", 0.0, 1.0, 0.25),
        "Delivery": st.slider("Delivery Weight", 0.0, 1.0, 0.25),
        "Risk": st.slider("Risk Weight", 0.0, 1.0, 0.25)
    }

    df["Score"] = (
        weights["Cost"] * (1 / df["Cost"]) +
        weights["Quality"] * df["Quality"] +
        weights["Delivery"] * df["Delivery"] +
        weights["Risk"] * (1 / df["Risk"])
    )

    ranked_df = df.sort_values("Score", ascending=False)
    st.subheader("📊 Ranked Suppliers")
    st.dataframe(ranked_df)

    # -------------------------
    # 3. Risk Prediction (ML Placeholder)
    # -------------------------
    st.header("3️⃣ Supplier Disruption Risk Forecast")

    ranked_df["Predicted_Disruption_Probability"] = np.random.uniform(0.05, 0.3, len(ranked_df))
    st.dataframe(ranked_df[["Supplier", "Predicted_Disruption_Probability"]])

    # -------------------------
    # 4. Order Allocation Optimization
    # -------------------------
    st.header("4️⃣ Optimal Order Allocation (Multi-Objective)")

    total_demand = st.number_input("Total Demand Quantity", 100, 10000, 1000)

    ranked_df["Allocation_%"] = ranked_df["Score"] / ranked_df["Score"].sum()
    ranked_df["Allocated_Qty"] = (ranked_df["Allocation_%"] * total_demand).astype(int)

    st.dataframe(ranked_df[["Supplier", "Allocated_Qty", "Cost", "Quality", "Delivery"]])

    # -------------------------
    # 5. Negotiation Agent (LLM Simulation Logic)
    # -------------------------
    st.header("5️⃣ AI Negotiation Agent")

    selected_supplier = st.selectbox("Select Supplier to Negotiate With", ranked_df["Supplier"])

    offer_price = st.number_input("Supplier Offered Price", value=100.0)
    target_price = st.number_input("Your Target Price", value=90.0)

    if st.button("Run Negotiation Simulation"):
        if offer_price <= target_price:
            decision = "Accept Offer"
            strategy = "Proceed with long-term contract and volume commitment."
        else:
            decision = "Counter Offer"
            strategy = f"Propose ₹{target_price} with extended contract tenure and demand assurance."

        st.success(f"🧠 AI Decision: {decision}")
        st.info(f"📌 Recommended Strategy: {strategy}")

    # -------------------------
    # 6. Auto PO & Contract Generator
    # -------------------------
    st.header("6️⃣ Smart Purchase Order Generator")

    if st.button("Generate Smart PO"):
        po_text = f"""
        PURCHASE ORDER – SMARTPROCURE AI

        Supplier: {selected_supplier}
        Quantity: {int(total_demand * 0.4)}
        Price: ₹{target_price}
        SLA: 98% On-Time Delivery
        Quality: < 0.5% Defect Rate
        Risk Clause: Dual Sourcing Trigger if Disruption Probability > 20%
        Payment Terms: Net 30
        Penalty: 1% per day delay
        """

        st.text_area("📄 Auto-Generated PO & Contract", po_text, height=300)

    # -------------------------
    # 7. What-if Scenario Simulation
    # -------------------------
    st.header("7️⃣ Scenario Simulation")

    disruption_scenario = st.slider("Simulate Supply Disruption Level (%)", 0, 50, 10)

    ranked_df["Adjusted_Risk"] = ranked_df["Risk"] * (1 + disruption_scenario / 100)
    st.dataframe(ranked_df[["Supplier", "Adjusted_Risk"]])

    st.markdown("### 🔁 System Recommendation")
    st.write("Reallocate demand to low-risk, high-score suppliers and trigger renegotiation workflows.")

else:
    st.info("Upload a supplier KPI dataset to activate SmartProcure AI.")
