import streamlit as st
import pandas as pd
from io import BytesIO

# Set page config
st.set_page_config(page_title="Kalkulator Biaya PM, ASD, EC Chiller (Rupiah)", layout="centered")
st.title("🧮 Kalkulator Biaya PM, ASD, dan EC Chiller (Rupiah)")

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

# Hitung otomatis Total Hari PM
base_pm_days = (no_air_cooled * 1) + (no_water_cooled / 2)
auto_total_pm_days = base_pm_days * pm_visits * manpower_pm

# Input Total Hari PM (editable manual)
total_pm_days = st.number_input(
    "Total Hari PM (hasil hitung otomatis dari chiller × visit × manpower, bisa diedit manual)",
    min_value=0.0,
    value=float(auto_total_pm_days),
    step=0.5,
    format="%.1f"
)

st.success(f"Total Hari PM: {total_pm_days:,.1f} hari")

# ===============================================
st.header("4. Annual Shutdown (ASD)")
asd_visits = st.number_input("Jumlah Kunjungan ASD", min_value=0, step=1, format="%d")

default_days_per_visit_asd = asd_visits if asd_visits > 0 else 0.0
days_per_visit_asd = st.number_input("Jumlah Hari per Kunjungan ASD", min_value=0.0, value=float(default_days_per_visit_asd), step=0.5, format="%.1f")

hours_per_day_asd = st.number_input("Jam kerja per hari untuk ASD", value=8.0, step=0.5, format="%.1f")
total_asd_days = asd_visits * days_per_visit_asd

# ===============================================
st.header("5. Emergency Call (EC)")
ec_visits = st.number_input("Jumlah Kunjungan EC", min_value=0, step=1, format="%d")
hours_per_day_ec = st.number_input("Jam kerja per hari untuk EC", value=6.0, step=0.5, format="%.1f")
total_ec_days = ec_visits * 1

# ===============================================
# Perhitungan Total Days & Total Hours
total_days = total_pm_days + total_asd_days + total_ec_days
total_hours_pm_asd = (total_pm_days * hours_per_day_pm) + (total_asd_days * hours_per_day_asd)
total_hours_ec = (total_ec_days * hours_per_day_ec)
total_hours = total_hours_pm_asd + total_hours_ec

# ===============================================
# Cost HANYA dari total hours x biaya teknisi
total_cost = total_hours * technician_unit_cost_per_hour_idr

# ===============================================
st.header("6. Harga Yang Ditawarkan")
offered_price_idr = st.number_input("Harga yang Ditawarkan (Rp)", min_value=0.0, step=1000.0, format="%.0f")

# Margin berdasarkan harga yang ditawarkan
margin = (offered_price_idr - total_cost) / offered_price_idr * 100 if offered_price_idr != 0 else 0

# ===============================================
# OUTPUT
st.header("📋 Hasil Perhitungan Akhir (Rupiah)")
st.write(f"Total PM Days: {total_pm_days:,.1f} hari")
st.write(f"Total ASD Days: {total_asd_days:,.1f} hari")
st.write(f"Total EC Days: {total_ec_days:,.1f} hari")
st.write(f"Total Hours: {total_hours:,.1f} jam")
st.write(f"Total Days: {total_days:,.1f} hari")

st.write("---")

st.subheader("💵 Price vs Cost")
st.write(f"**Harga yang Ditawarkan (Price): Rp {offered_price_idr:,.0f}**")
st.write(f"**Total Cost (semua jam x biaya teknisi): Rp {total_cost:,.0f}**")
st.caption(f"Perhitungan: {total_hours:,.1f} jam x Rp {technician_unit_cost_per_hour_idr:,.0f} per jam = Rp {total_cost:,.0f}")

# Warning margin merah kalau <40%
if margin < 40:
    st.error(f"⚠️ Margin: {margin:.2f}% (Kurang dari 40%)")
else:
    st.success(f"✅ Margin: {margin:.2f}%")

# ===============================================
# Prepare Data untuk Download Excel
data = {
    "Item": [
        "Total PM Days",
        "Total ASD Days",
        "Total EC Days",
        "Total Hours",
        "Total Days",
        "Total Cost (Rp)",
        "Harga Ditawarkan (Rp)",
        "Margin (%)",
    ],
    "Value": [
        total_pm_days,
        total_asd_days,
        total_ec_days,
        total_hours,
        total_days,
        total_cost,
        offered_price_idr,
        margin,
    ],
}

df_result = pd.DataFrame(data)

# Function download Excel
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Summary')
    processed_data = output.getvalue()
    return processed_data

st.download_button(
    label="📥 Download Hasil Breakdown ke Excel (Rupiah)",
    data=to_excel(df_result),
    file_name="kalkulator_biaya_pm_asd_ec_idr.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)
