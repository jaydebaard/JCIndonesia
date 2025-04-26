import streamlit as st
import pandas as pd
from io import BytesIO

# Set page config
st.set_page_config(page_title="Kalkulator Biaya PM, ASD, EC + Subcontractor", layout="centered")
st.title("🧮 Kalkulator Biaya PM, ASD, EC, Subkontraktor, Spare Parts, dan Other Cost (Rupiah)")

# ===============================================
st.header("1. Cost Setting (Rupiah)")
technician_unit_cost_per_hour_idr = st.number_input("Biaya per Jam Teknisi (Rp)", value=265600.0, step=1000.0, format="%.0f")

# ===============================================
st.header("2. Jumlah Chiller")
col1, col2 = st.columns(2)
with col1:
    no_air_cooled = st.number_input("Jumlah Air Cooled Chiller", min_value=0, step=1, format="%d")
with col2:
    no_water_cooled = st.number_input("Jumlah Water Cooled Chiller", min_value=0, step=1, format="%d")

# ===============================================
st.header("3. Preventive Maintenance (PM)")
hours_per_day_pm = st.number_input("Jam kerja per hari untuk PM", value=8.0, step=0.5, format="%.1f")
manpower_pm = st.number_input("Jumlah Teknisi untuk PM", min_value=1, step=1, format="%d")
pm_visits = st.number_input("Jumlah Kunjungan PM", min_value=0, step=1, format="%d")

base_pm_days = (no_air_cooled * 1) + (no_water_cooled / 2)
auto_total_pm_days = base_pm_days * pm_visits * manpower_pm

total_pm_days = st.number_input(
    "Total Hari PM (hasil hitung otomatis, bisa diedit manual)",
    min_value=0.0,
    value=float(auto_total_pm_days),
    step=0.5,
    format="%.1f"
)
st.success(f"Total Hari PM: {total_pm_days:,.1f} hari")

# ===============================================
st.header("4. Annual Shutdown (ASD)")
asd_visits = st.number_input("Jumlah Kunjungan ASD", min_value=0, step=1, format="%d")
days_per_visit_asd = st.number_input("Jumlah Hari per Kunjungan ASD", min_value=0.0, value=float(asd_visits), step=0.5, format="%.1f")
hours_per_day_asd = st.number_input("Jam kerja per hari untuk ASD", value=8.0, step=0.5, format="%.1f")
total_asd_days = asd_visits * days_per_visit_asd

# ===============================================
st.header("5. Emergency Call (EC)")
ec_visits = st.number_input("Jumlah Kunjungan EC", min_value=0, step=1, format="%d")
hours_per_day_ec = st.number_input("Jam kerja per hari untuk EC", value=6.0, step=0.5, format="%.1f")
total_ec_days = ec_visits

# ===============================================
# Perhitungan Total Days & Total Hours
total_days = total_pm_days + total_asd_days + total_ec_days
total_hours = (total_pm_days * hours_per_day_pm) + (total_asd_days * hours_per_day_asd) + (total_ec_days * hours_per_day_ec)

# ===============================================
# Cost Teknisi
total_cost_technician = total_hours * technician_unit_cost_per_hour_idr

# ===============================================
st.header("6. Harga Yang Ditawarkan")
offered_price_idr = st.number_input("Harga yang Ditawarkan (Rp)", min_value=0.0, step=1000.0, format="%.0f")

# ===============================================
# Subcontractor Work
st.header("7. Subcontractor Works (Optional)")

with st.expander("➕ Tambahkan Subcontractor Works"):
    add_subcon = st.checkbox("Centang untuk input biaya Subcontractor", value=False)
    if add_subcon:
        st.subheader("Helper Work")
        helper_days = st.number_input("Jumlah Hari Helper", min_value=0.0, step=0.5, format="%.1f")
        helper_hours_per_day = st.number_input("Jam kerja per Hari Helper", min_value=0.0, value=8.0, step=0.5, format="%.1f")
        helper_cost_per_hour = st.number_input("Biaya per Jam Helper (Rp)", min_value=0.0, value=62500.0, step=1000.0, format="%.0f")
        helper_total_cost = helper_days * helper_hours_per_day * helper_cost_per_hour

        st.subheader("Condenser Cleaning Work")
        cleaning_days = st.number_input("Jumlah Hari Cleaning", min_value=0.0, step=0.5, format="%.1f")
        cleaning_hours_per_day = st.number_input("Jam kerja per Hari Cleaning", min_value=0.0, value=8.0, step=0.5, format="%.1f")
        cleaning_cost_per_hour = st.number_input("Biaya per Jam Cleaning (Rp)",
