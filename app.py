import pandas as pd
import streamlit as st
import plotly.express as px

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(
    page_title="Client KPI Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("Client KPI Dashboard")
st.caption("Interactive KPI and chart dashboard")

# ----------------------------
# Load data
# ----------------------------
@st.cache_data
def load_data(file_path):
    df = pd.read_excel(file_path)

    # Clean column names
    df.columns = [col.strip() for col in df.columns]

    # Convert numeric columns
    numeric_cols = ["Engagement Score", "Meetings Count", "Revenue"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

# 🔥 UPDATED FILE NAME HERE
DATA_FILE = "full_client_dataset_1000_rows.xlsx"

try:
    df = load_data(DATA_FILE)
except FileNotFoundError:
    st.error(f"File not found: {DATA_FILE}")
    st.stop()

# ----------------------------
# KPIs
# ----------------------------
total_clients = df["Client ID"].nunique()
total_revenue = df["Revenue"].sum()
avg_engagement = df["Engagement Score"].mean()

retained = df[df["Retention Status"] == "Retained"].shape[0]
retention_rate = (retained / len(df)) * 100

# ----------------------------
# KPI Display
# ----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Clients", total_clients)
col2.metric("Total Revenue", f"₹{total_revenue:,.0f}")
col3.metric("Avg Engagement", f"{avg_engagement:.2f}")
col4.metric("Retention Rate", f"{retention_rate:.2f}%")

st.markdown("---")

# ----------------------------
# Charts
# ----------------------------

# Revenue by Industry
rev_industry = df.groupby("Industry")["Revenue"].sum().reset_index()

fig1 = px.bar(
    rev_industry,
    x="Industry",
    y="Revenue",
    title="Revenue by Industry"
)

st.plotly_chart(fig1, use_container_width=True)

# Retention Count
retention = df["Retention Status"].value_counts().reset_index()
retention.columns = ["Status", "Count"]

fig2 = px.pie(
    retention,
    names="Status",
    values="Count",
    title="Retention Distribution"
)

st.plotly_chart(fig2, use_container_width=True)

# Meetings vs Revenue
fig3 = px.scatter(
    df,
    x="Meetings Count",
    y="Revenue",
    color="Retention Status",
    size="Engagement Score",
    title="Meetings vs Revenue"
)

st.plotly_chart(fig3, use_container_width=True)

# ----------------------------
# Data Preview
# ----------------------------
st.subheader("Dataset Preview")
st.dataframe(df)
