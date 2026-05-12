import streamlit as st
import pandas as pd

st.title("📊 Goods Flow Dashboard")

# ===== 上傳資料 =====
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.sidebar.header("Filter")
    date_col = st.sidebar.selectbox("Select Date Column", df.columns)

    # ===== DAILY =====
    st.header("📅 DAILY Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Inventory (pcs)", int(df["inventory_pcs"].sum()))
    col2.metric("Inventory (CBM)", round(df["inventory_cbm"].sum(),2))
    col3.metric("Buffer Fill Rate", f"{df['buffer_fillrate'].mean():.2%}")

    col4, col5, col6 = st.columns(3)
    col4.metric("Storage Utilization", f"{df['storage_util'].mean():.2%}")
    col5.metric("Inbound (Pallet)", int(df["inbound_pallet"].sum()))
    col6.metric("Outbound (Pallet)", int(df["outbound_pallet"].sum()))

    col7, col8, col9 = st.columns(3)
    col7.metric("Deadwood %", f"{df['deadwood'].mean():.2%}")
    col8.metric("SL Working Hours", df["working_hours"].sum())

    # 圖表
    st.subheader("Daily Trend")
    st.line_chart(df.set_index(date_col)[["inbound_pallet", "outbound_pallet"]])


    # ===== WEEKLY =====
    st.header("📆 WEEKLY Dashboard")

    colw1, colw2, colw3 = st.columns(3)
    colw1.metric("Shipping Fee", df["shipping_fee"].sum())
    colw2.metric("Backflow", df["backflow"].sum())
    colw3.metric("Forecast Sold m2", df["forecast_m2"].sum())

    colw4, colw5, colw6 = st.columns(3)
    colw4.metric("Landing Sold m2", df["landing_m2"].sum())
    colw5.metric("Planning Hours", df["plan_hours"].sum())
    colw6.metric("Actual Hours", df["actual_hours"].sum())

    st.metric("Direct Flow", f"{df['direct_flow'].mean():.2%}")

    st.subheader("Weekly Comparison")
    st.bar_chart(df[["forecast_m2", "landing_m2"]])

else:
    st.info("Please upload an Excel file to view dashboard")
