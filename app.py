# app.py

import pandas as pd
import streamlit as st
import plotly.express as px

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Client KPI Dashboard", layout="wide")

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("full_client_dataset_1000_rows.csv")
    return df

df = load_data()

# -----------------------------
# Title
# -----------------------------
st.title("📊 Client KPI Dashboard")

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

industry_filter = st.sidebar.multiselect(
    "Select Industry",
    options=df["Industry"].unique(),
    default=df["Industry"].unique()
)

region_filter = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

filtered_df = df[
    (df["Industry"].isin(industry_filter)) &
    (df["Region"].isin(region_filter))
]

# -----------------------------
# KPI Metrics
# -----------------------------
total_clients = filtered_df["Client ID"].nunique()
total_revenue = filtered_df["Revenue"].sum()
avg_engagement = filtered_df["Engagement Score"].mean()
retention_rate = (
    filtered_df[filtered_df["Retention Status"] == "Retained"].shape[0]
    / filtered_df.shape[0]
) * 100

# -----------------------------
# Display KPIs
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Clients", total_clients)
col2.metric("Total Revenue", f"₹{total_revenue:,.0f}")
col3.metric("Avg Engagement Score", f"{avg_engagement:.2f}")
col4.metric("Retention Rate", f"{retention_rate:.1f}%")

# -----------------------------
# Charts
# -----------------------------

# Revenue by Industry
fig1 = px.bar(
    filtered_df.groupby("Industry")["Revenue"].sum().reset_index(),
    x="Industry",
    y="Revenue",
    title="Revenue by Industry"
)

# Revenue by Region
fig2 = px.pie(
    filtered_df,
    names="Region",
    values="Revenue",
    title="Revenue Distribution by Region"
)

# Engagement Score Distribution
fig3 = px.histogram(
    filtered_df,
    x="Engagement Score",
    nbins=20,
    title="Engagement Score Distribution"
)

# Meetings vs Revenue
fig4 = px.scatter(
    filtered_df,
    x="Meetings Count",
    y="Revenue",
    color="Industry",
    title="Meetings vs Revenue"
)

# -----------------------------
# Show Charts
# -----------------------------
st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)

col5, col6 = st.columns(2)
col5.plotly_chart(fig3, use_container_width=True)
col6.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# Data Table
# -----------------------------
st.subheader("Filtered Data")
st.dataframe(filtered_df)
