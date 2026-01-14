import streamlit as st
import pandas as pd
import numpy as np
import requests
#import plotly.express as px
from openai import OpenAI

client = OpenAI(api_key=["sk-abcdef1234567890abcdef1234567890abcdef12"])  # For Streamlit Cloud

st.set_page_config(page_title="SmartProcure AI", layout="wide")
st.title("🤖 SmartProcure AI – Autonomous Strategic Sourcing Platform")

# -------------------------
# 1. Supplier Data Lake
# -------------------------
st.header("1️⃣ Supplier Data Lake")

data_source = st.radio("Select Data Source", ["Upload CSV", "Fetch from Internet (URL)"])

if data_source == "Upload CSV":
    uploaded_file = st.file_uploader("Upload Supplier KPI Dataset (CSV)", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)

elif data_source == "Fetch from Internet (URL)":
    url = st.text_input("Enter CSV URL (GitHub raw / public dataset)")
    if url:
        df = pd.read_csv(url)

if 'df' in locals():
    st.dataframe(df)

    # -------------------------
    # 2. MCDA Ranking
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

    fig_risk = px.scatter(ranked_df, x="Cost", y="Risk", size="Score",
                          color="Supplier", title="Cost vs Risk Portfolio")
    st.plotly_chart(fig_risk, use_container_width=True)

    # -------------------------
    # 4. Risk Forecast
    # -------------------------
    st.header("3️⃣ AI Risk Forecast")
    ranked_df["Disruption_Prob"] = np.random.uniform(0.05, 0.3, len(ranked_df))
    st.dataframe(ranked_df[["Supplier", "Disruption_Prob"]])

    # -------------------------
    # 5. Optimization
    # -------------------------
    st.header("4️⃣ Optimal Order Allocation")

    total_demand = st.number_input("Total Demand", 100, 10000, 1000)
    ranked_df["Allocation"] = (ranked_df["Score"] / ranked_df["Score"].sum()) * total_demand
    st.dataframe(ranked_df[["Supplier", "Allocation"]])

    fig_alloc = px.pie(ranked_df, names="Supplier", values="Allocation",
                       title="Optimal Order Allocation")
    st.plotly_chart(fig_alloc, use_container_width=True)

    # -------------------------
    # 6. GPT Negotiation Agent
    # -------------------------
    st.header("5️⃣ GPT Negotiation Agent")

    supplier = st.selectbox("Select Supplier", ranked_df["Supplier"])
    offer = st.number_input("Supplier Offer Price", value=100.0)
    target = st.number_input("Target Price", value=90.0)

    if st.button("Run AI Negotiation"):
        prompt = f"""
        You are a procurement negotiation expert.
        Supplier: {supplier}
        Offered Price: {offer}
        Target Price: {target}
        Recommend negotiation strategy, counter price, and contract terms.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        st.success("🧠 GPT Negotiation Recommendation")
        st.write(response.choices[0].message.content)

    # -------------------------
    # 7. Smart PO Generator
    # -------------------------
    st.header("6️⃣ Auto PO Generator")

    if st.button("Generate Smart PO"):
        po_prompt = f"""
        Create a professional purchase order with SLA, penalties and risk clauses
        for supplier {supplier}, quantity {int(total_demand*0.4)}, target price {target}.
        """

        po = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": po_prompt}]
        )

        st.text_area("📄 AI Generated Purchase Order", po.choices[0].message.content, height=300)

    # -------------------------
    # 8. Scenario Simulation
    # -------------------------
    st.header("7️⃣ What-if Scenario")

    disruption = st.slider("Disruption Level %", 0, 50, 10)
    ranked_df["Adjusted_Risk"] = ranked_df["Risk"] * (1 + disruption/100)
    st.dataframe(ranked_df[["Supplier", "Adjusted_Risk"]])
