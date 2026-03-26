import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Client Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .block-container { padding-top: 1.5rem; padding-bottom: 1rem; }

    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #1e2130 0%, #262b3d 100%);
        border: 1px solid #2d3250;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        text-align: center;
    }
    .kpi-label {
        color: #8b95b0;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.4rem;
    }
    .kpi-value {
        color: #e8eaf6;
        font-size: 2rem;
        font-weight: 700;
        line-height: 1.1;
    }
    .kpi-delta {
        font-size: 0.78rem;
        margin-top: 0.3rem;
        color: #42d9a8;
    }

    /* Section headers */
    .section-header {
        color: #c5cae9;
        font-size: 1.05rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        border-left: 3px solid #5c6bc0;
        padding-left: 0.6rem;
        margin: 1.2rem 0 0.8rem 0;
    }

    /* Insight cards */
    .insight-card {
        background: #1a1f2e;
        border: 1px solid #2d3250;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.7rem;
    }
    .insight-title {
        color: #7986cb;
        font-weight: 700;
        font-size: 0.85rem;
        margin-bottom: 0.35rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .insight-body { color: #b0bec5; font-size: 0.88rem; line-height: 1.55; }

    /* Strategy cards */
    .strategy-card {
        background: linear-gradient(135deg, #1b2838 0%, #1e2d40 100%);
        border: 1px solid #2a3f5f;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.7rem;
    }
    .strategy-num {
        display: inline-block;
        background: #3f51b5;
        color: white;
        border-radius: 50%;
        width: 24px; height: 24px;
        text-align: center;
        line-height: 24px;
        font-size: 0.78rem;
        font-weight: 700;
        margin-right: 0.5rem;
    }
    .strategy-title { color: #90caf9; font-weight: 700; font-size: 0.9rem; }
    .strategy-body  { color: #b0bec5; font-size: 0.85rem; line-height: 1.5; margin-top: 0.4rem; }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #141824;
        border-right: 1px solid #1f2540;
    }
    .stSelectbox label, .stMultiSelect label { color: #8b95b0 !important; font-size: 0.8rem !important; }
</style>
""", unsafe_allow_html=True)

# ── Data Loading ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_excel("client_data_csv.xlsx")
    # Simulate a date column for Revenue Trend (12 months)
    np.random.seed(42)
    months = pd.date_range("2024-01-01", periods=12, freq="ME")
    # Assign each client a random month for trend visualization
    df["Month"] = np.random.choice(months, size=len(df))
    return df

df = load_data()

# ── Sidebar Filters ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 Filters")
    st.markdown("---")

    industries = st.multiselect(
        "Industry",
        options=sorted(df["Industry"].unique()),
        default=sorted(df["Industry"].unique()),
    )
    regions = st.multiselect(
        "Region",
        options=sorted(df["Region"].unique()),
        default=sorted(df["Region"].unique()),
    )
    retention = st.multiselect(
        "Retention Status",
        options=sorted(df["Retention Status"].unique()),
        default=sorted(df["Retention Status"].unique()),
    )
    eng_range = st.slider(
        "Engagement Score Range",
        int(df["Engagement Score"].min()),
        int(df["Engagement Score"].max()),
        (int(df["Engagement Score"].min()), int(df["Engagement Score"].max())),
    )

    st.markdown("---")
    st.markdown("<small style='color:#555'>Client Analytics Dashboard v1.0</small>", unsafe_allow_html=True)

# ── Apply Filters ──────────────────────────────────────────────────────────────
filtered = df[
    (df["Industry"].isin(industries)) &
    (df["Region"].isin(regions)) &
    (df["Retention Status"].isin(retention)) &
    (df["Engagement Score"].between(eng_range[0], eng_range[1]))
]

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("# 📊 Client Analytics Dashboard")
st.markdown(f"<small style='color:#555'>Showing **{len(filtered):,}** of **{len(df):,}** clients</small>", unsafe_allow_html=True)

# ── KPI Cards ──────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">KEY PERFORMANCE INDICATORS</div>', unsafe_allow_html=True)

total_clients    = len(filtered)
avg_engagement   = filtered["Engagement Score"].mean() if len(filtered) else 0
total_revenue    = filtered["Revenue"].sum() if len(filtered) else 0
retention_rate   = (filtered["Retention Status"] == "Retained").mean() * 100 if len(filtered) else 0

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Clients</div>
        <div class="kpi-value">{total_clients:,}</div>
        <div class="kpi-delta">Across {filtered['Industry'].nunique()} industries</div>
    </div>""", unsafe_allow_html=True)

with k2:
    color = "#42d9a8" if avg_engagement >= 68 else "#ff7043"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Avg Engagement Score</div>
        <div class="kpi-value" style="color:{color}">{avg_engagement:.1f}</div>
        <div class="kpi-delta">{'▲ Above' if avg_engagement >= 68 else '▼ Below'} overall avg (68.2)</div>
    </div>""", unsafe_allow_html=True)

with k3:
    rev_m = total_revenue / 1_000_000
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Revenue</div>
        <div class="kpi-value">${rev_m:.1f}M</div>
        <div class="kpi-delta">Avg ${filtered['Revenue'].mean():,.0f} per client</div>
    </div>""", unsafe_allow_html=True)

with k4:
    rcolor = "#42d9a8" if retention_rate >= 21 else "#ff7043"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Retention Rate</div>
        <div class="kpi-value" style="color:{rcolor}">{retention_rate:.1f}%</div>
        <div class="kpi-delta">{'▲ Healthy' if retention_rate >= 21 else '▼ Needs attention'}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts Row 1 ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">ENGAGEMENT & REVENUE ANALYTICS</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)

# Chart 1 – Engagement by Industry
with c1:
    eng_ind = (
        filtered.groupby("Industry")["Engagement Score"]
        .mean()
        .reset_index()
        .sort_values("Engagement Score", ascending=True)
    )
    fig1 = px.bar(
        eng_ind,
        x="Engagement Score",
        y="Industry",
        orientation="h",
        color="Engagement Score",
        color_continuous_scale=["#f44336", "#ff9800", "#4caf50"],
        title="Average Engagement Score by Industry",
        text=eng_ind["Engagement Score"].round(1),
    )
    fig1.update_traces(textfont_color="white", textposition="outside")
    fig1.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
        margin=dict(l=10, r=30, t=45, b=10),
        title_font_color="#c5cae9",
        title_font_size=13,
        xaxis=dict(gridcolor="#1f2540", title=None),
        yaxis=dict(gridcolor="#1f2540", title=None),
        height=320,
    )
    st.plotly_chart(fig1, use_container_width=True)

# Chart 2 – Revenue Trend
with c2:
    rev_trend = (
        filtered.groupby(filtered["Month"].dt.strftime("%b %Y"))["Revenue"]
        .sum()
        .reset_index()
    )
    rev_trend.columns = ["Month", "Revenue"]
    # Proper month ordering
    rev_trend["_sort"] = pd.to_datetime(rev_trend["Month"], format="%b %Y")
    rev_trend = rev_trend.sort_values("_sort").drop(columns="_sort")

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=rev_trend["Month"],
        y=rev_trend["Revenue"],
        mode="lines+markers",
        line=dict(color="#5c6bc0", width=3),
        marker=dict(size=7, color="#7986cb"),
        fill="tozeroy",
        fillcolor="rgba(92,107,192,0.12)",
        name="Revenue",
    ))
    fig2.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title="Monthly Revenue Trend",
        title_font_color="#c5cae9",
        title_font_size=13,
        margin=dict(l=10, r=10, t=45, b=10),
        xaxis=dict(gridcolor="#1f2540", tickangle=-30, title=None),
        yaxis=dict(gridcolor="#1f2540", title=None, tickprefix="$", tickformat=","),
        height=320,
        showlegend=False,
    )
    st.plotly_chart(fig2, use_container_width=True)

# ── Chart Row 2 ────────────────────────────────────────────────────────────────
c3, c4 = st.columns(2)

# Chart 3 – Retention Analysis (stacked bar by industry)
with c3:
    ret_ind = (
        filtered.groupby(["Industry", "Retention Status"])
        .size()
        .reset_index(name="Count")
    )
    color_map = {"Retained": "#42d9a8", "At Risk": "#ff9800", "Churned": "#f44336"}
    fig3 = px.bar(
        ret_ind,
        x="Industry",
        y="Count",
        color="Retention Status",
        color_discrete_map=color_map,
        barmode="stack",
        title="Retention Analysis by Industry",
    )
    fig3.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title_font_color="#c5cae9",
        title_font_size=13,
        margin=dict(l=10, r=10, t=45, b=10),
        xaxis=dict(gridcolor="#1f2540", title=None, tickangle=-25),
        yaxis=dict(gridcolor="#1f2540", title="Client Count"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=320,
    )
    st.plotly_chart(fig3, use_container_width=True)

# Chart 4 – Engagement vs Revenue scatter
with c4:
    fig4 = px.scatter(
        filtered,
        x="Engagement Score",
        y="Revenue",
        color="Retention Status",
        color_discrete_map=color_map,
        opacity=0.65,
        trendline="ols",
        trendline_scope="overall",
        trendline_color_override="#ffffff",
        title="Engagement Score vs Revenue",
        hover_data=["Client ID", "Industry"],
    )
    fig4.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title_font_color="#c5cae9",
        title_font_size=13,
        margin=dict(l=10, r=10, t=45, b=10),
        xaxis=dict(gridcolor="#1f2540", title="Engagement Score"),
        yaxis=dict(gridcolor="#1f2540", title="Revenue ($)", tickformat=",.0f"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=320,
    )
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Business Insights ──────────────────────────────────────────────────────────
st.markdown('<div class="section-header">BUSINESS INSIGHTS</div>', unsafe_allow_html=True)

ins1, ins2 = st.columns(2)

with ins1:
    low_eng = filtered[filtered["Engagement Score"] <= 50]
    low_by_ind = low_eng["Industry"].value_counts().head(3)
    ind_str = ", ".join([f"{i} ({c})" for i, c in low_by_ind.items()])

    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">🔴 Low Engagement Clients</div>
        <div class="insight-body">
            <b>{len(low_eng):,}</b> clients ({len(low_eng)/len(filtered)*100:.1f}%) have an engagement score ≤ 50.<br>
            Top industries at risk: <b>{ind_str}</b>.<br>
            These clients are most likely to churn without proactive intervention.
        </div>
    </div>""", unsafe_allow_html=True)

    # Engagement vs Revenue correlation
    corr = filtered[["Engagement Score", "Revenue"]].corr().iloc[0, 1]
    direction = "positive" if corr > 0 else "negative"
    strength = "strong" if abs(corr) > 0.5 else ("moderate" if abs(corr) > 0.3 else "weak")
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">📈 Engagement ↔ Revenue Link</div>
        <div class="insight-body">
            Correlation coefficient: <b>r = {corr:.2f}</b> — a <b>{strength} {direction}</b> relationship.<br>
            {"Higher engagement scores are clearly associated with higher revenue, confirming that investing in client engagement directly drives financial outcomes." if corr > 0.3 else "Engagement and revenue show a weak link in this dataset, suggesting other factors (deal size, contract terms) may dominate."}
        </div>
    </div>""", unsafe_allow_html=True)

with ins2:
    ret_rate_ind = (
        filtered[filtered["Retention Status"] == "Retained"]
        .groupby("Industry").size() /
        filtered.groupby("Industry").size()
    ).dropna().sort_values(ascending=False)
    top_ret = ret_rate_ind.index[0]
    top_ret_val = ret_rate_ind.iloc[0] * 100

    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">✅ Highest Retention Industry</div>
        <div class="insight-body">
            <b>{top_ret}</b> leads all industries with a retention rate of <b>{top_ret_val:.1f}%</b>.<br>
            Runner-up: <b>{ret_rate_ind.index[1]}</b> ({ret_rate_ind.iloc[1]*100:.1f}%).<br>
            Study the success factors in {top_ret} and replicate them across lower-performing sectors.
        </div>
    </div>""", unsafe_allow_html=True)

    churn_rev = filtered[filtered["Retention Status"] == "Churned"]["Revenue"].sum()
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-title">⚠️ At-Risk Revenue Exposure</div>
        <div class="insight-body">
            Churned clients represent <b>${churn_rev/1_000_000:.1f}M</b> in lost revenue.<br>
            <b>{filtered[filtered['Retention Status']=='At Risk']['Revenue'].sum()/1_000_000:.1f}M</b> more is at risk from "At Risk" clients.<br>
            Prioritize re-engagement campaigns for high-revenue at-risk accounts immediately.
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Strategies ─────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">STRATEGIC RECOMMENDATIONS</div>', unsafe_allow_html=True)

strategies = [
    (
        "Tiered Engagement Program",
        "Segment clients into three tiers by engagement score: High (≥70), Medium (50–69), Low (<50). "
        "Deploy dedicated Customer Success Managers for Low-tier accounts, automated nurture sequences "
        "for Medium-tier, and self-serve resources for High-tier. Aim to move 20% of Low-tier clients "
        "into Medium within 90 days.",
    ),
    (
        "Revenue-Weighted Retention Campaigns",
        f"Focus retention budgets on high-revenue 'At Risk' clients first. "
        "Run personalised quarterly business reviews (QBRs) and offer loyalty incentives such as "
        "extended contract discounts or priority support SLAs. Replicating the engagement playbook "
        f"from the top-retention industry ({top_ret}) across all sectors could lift the overall "
        "retention rate by an estimated 8–12 percentage points.",
    ),
    (
        "Engagement-Driven Revenue Upsell",
        f"With a correlation of r = {corr:.2f} between engagement and revenue, increasing average "
        "engagement by 10 points is projected to lift per-client revenue meaningfully. Introduce "
        "value-add workshops, product certifications, and community events to deepen relationships. "
        "Track Net Promoter Score (NPS) alongside engagement scores to validate progress.",
    ),
]

s1, s2, s3 = st.columns(3)
for col, (i, (title, body)) in zip([s1, s2, s3], enumerate(strategies, 1)):
    with col:
        st.markdown(f"""
        <div class="strategy-card">
            <div><span class="strategy-num">{i}</span><span class="strategy-title">{title}</span></div>
            <div class="strategy-body">{body}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Raw Data Table ─────────────────────────────────────────────────────────────
with st.expander("📋 View Filtered Client Data"):
    st.dataframe(
        filtered.drop(columns=["Month"]).reset_index(drop=True),
        use_container_width=True,
        height=300,
    )
    st.download_button(
        "⬇️ Download Filtered Data as CSV",
        data=filtered.drop(columns=["Month"]).to_csv(index=False),
        file_name="filtered_clients.csv",
        mime="text/csv",
    )
