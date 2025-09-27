# pip install streamlit plotly pandas openpyxl
# python -m streamlit run retail.py

# ==========================================
# Streamlit Retail Analytics Dashboard - Versi Profesional (Single Page + Border)
# ==========================================

import pandas as pd
import streamlit as st
import plotly.express as px

# ================================
# Load dataset
# ================================
@st.cache_data
def load_data():
    df = pd.read_excel("Online Retail.xlsx", engine="openpyxl")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]
    df["YearMonth"] = df["InvoiceDate"].dt.to_period("M").astype(str)
    df["Year"] = df["InvoiceDate"].dt.year
    df["Month"] = df["InvoiceDate"].dt.month
    return df

df = load_data()

# ================================
# Sidebar Filters
# ================================
st.set_page_config(page_title="Retail Analytics Dashboard", layout="wide")
st.sidebar.title("🔎 Filters")

years = sorted(df["Year"].unique())
selected_year = st.sidebar.selectbox("Pilih Tahun", options=["All"] + years)
if selected_year != "All":
    df = df[df["Year"] == selected_year]

months = sorted(df["Month"].unique())
selected_month = st.sidebar.selectbox("Pilih Bulan", options=["All"] + months)
if selected_month != "All":
    df = df[df["Month"] == selected_month]

# ================================
# KPI Metrics
# ================================
total_revenue = df["Revenue"].sum()
total_orders = df["InvoiceNo"].nunique()
total_customers = df["CustomerID"].nunique()
top_product = df.groupby("Description")["Quantity"].sum().idxmax()
aov = total_revenue / total_orders if total_orders > 0 else 0
purchase_freq = total_orders / total_customers if total_customers > 0 else 0
clv = aov * purchase_freq

# ================================
# Retention & Churn
# ================================
customer_month = df.groupby(["CustomerID", "YearMonth"]).size().reset_index(name="purchases")
retention = []
months = sorted(customer_month["YearMonth"].unique())

for i in range(1, len(months)):
    prev_month = customer_month[customer_month["YearMonth"] == months[i-1]]["CustomerID"].unique()
    curr_month = customer_month[customer_month["YearMonth"] == months[i]]["CustomerID"].unique()
    retained = len(set(prev_month) & set(curr_month))
    retention_rate = retained / len(prev_month) if len(prev_month) > 0 else 0
    retention.append({
        "Month": str(months[i]),
        "RetentionRate": retention_rate,
        "ChurnRate": 1 - retention_rate
    })

retention_df = pd.DataFrame(retention)

# ================================
# Dashboard UI
# ================================
st.title("Retail Analytics Dashboard")
st.markdown("**Analisis performa bisnis retail: revenue, pelanggan, retention, churn, dan CLV.**")

# KPI Cards
with st.container(border=True):
    st.markdown("### Key Metrics")
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Total Revenue", f"${total_revenue:,.0f}")
    kpi2.metric("Total Orders", f"{total_orders:,}")
    kpi3.metric("Total Customers", f"{total_customers:,}")

    st.markdown("### Top Product")
    st.markdown(f"<div style='font-size:20px; font-weight:bold; color:#2E86C1'>{top_product}</div>", unsafe_allow_html=True)

    kpi4, kpi5 = st.columns(2)
    kpi4.metric("Average Order Value (AOV)", f"${aov:,.2f}")
    kpi5.metric("Customer Lifetime Value (CLV)", f"${clv:,.2f}")

# Revenue Trend
with st.container(border=True):
    st.subheader("Revenue Trend Over Time")
    revenue_trend = df.groupby("YearMonth")["Revenue"].sum().reset_index()
    fig_rev = px.bar(revenue_trend, x="YearMonth", y="Revenue", title="Monthly Revenue")
    st.plotly_chart(fig_rev, use_container_width=True)

# Retention & Churn
with st.container(border=True):
    st.subheader("Retention & Churn Rate per Month")
    if not retention_df.empty:
        fig_ret = px.line(retention_df, x="Month", y=["RetentionRate", "ChurnRate"], markers=True,
                          labels={"value": "Rate", "variable": "Metric"})
        st.plotly_chart(fig_ret, use_container_width=True)
    else:
        st.warning("⚠️ Data hanya 1 bulan, Retention/Churn tidak bisa dihitung.")

# Detail Data
with st.container(border=True):
    st.subheader("Detail Data Sample")
    st.dataframe(df.head(20))

st.markdown("---")
st.caption("© 2025 Retail Analytics Dashboard | Dibuat dengan ❤️ menggunakan Streamlit & Plotly")

# ================================
# (Opsional) Tambahan CSS untuk versi lama Streamlit (jika border=True tidak support)
# ================================
st.markdown("""
<style>
div[data-testid="stContainer"] {
    border: 2px solid #2E86C1;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)
