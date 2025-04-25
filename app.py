import streamlit as st
import pandas as pd
from io import BytesIO

# Set page config
st.set_page_config(page_title="Kalkulator Biaya PM, ASD, EC + Subcontractor (Rupiah)", layout="centered")
st.title("🧮 Kalkulator Biaya PM, ASD, EC, Subkontraktor, dan Other Cost (Rupiah)")

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
# Cost Teknisi
total_cost_technician = total_hours * technician_unit_cost_per_hour_idr

# ===============================================
st.header("6. Harga Yang Ditawarkan")
offered_price_idr = st.number_input("Harga yang Ditawarkan (Rp)", min_value=0.0, step=1000.0, format="%.0f")

# Margin dari harga yang ditawarkan (teknisi saja)
margin = (offered_price_idr - total_cost_technician) / offered_price_idr * 100 if offered_price_idr != 0 else 0

# ===============================================
# OUTPUT Price vs Cost
st.header("📋 Hasil Perhitungan Awal (Teknisi Saja)")
st.write(f"Total PM Days: {total_pm_days:,.1f} hari")
st.write(f"Total ASD Days: {total_asd_days:,.1f} hari")
st.write(f"Total EC Days: {total_ec_days:,.1f} hari")
st.write(f"Total Hours: {total_hours:,.1f} jam")
st.write(f"Total Days: {total_days:,.1f} hari")

st.write("---")

st.subheader("💵 Price vs Cost (Teknisi)")
st.write(f"**Harga yang Ditawarkan (Price): Rp {offered_price_idr:,.0f}**")
st.write(f"**Total Cost Teknisi: Rp {total_cost_technician:,.0f}**")
st.caption(f"Perhitungan: {total_hours:,.1f} jam x Rp {technician_unit_cost_per_hour_idr:,.0f} per jam = Rp {total_cost_technician:,.0f}")

if margin < 40:
    st.error(f"⚠️ Margin (Hanya dari Teknisi): {margin:.2f}% (Kurang dari 40%)")
else:
    st.success(f"✅ Margin (Hanya dari Teknisi): {margin:.2f}%")

# ===============================================
# Bagian Baru - Subcontractor Work
st.header("7. Subcontractor Works")

subcon_categories = ["Helper", "Condenser Cleaning", "Other"]
selected_category = st.selectbox("Pilih Kategori Subcontractor", subcon_categories)

subcon_days = st.number_input(f"Jumlah Hari untuk {selected_category}", min_value=0.0, step=0.5, format="%.1f")
subcon_hours_per_day = st.number_input(f"Jam kerja per Hari untuk {selected_category}", min_value=0.0, step=0.5, format="%.1f")
subcon_cost_per_hour = st.number_input(f"Biaya per Jam untuk {selected_category} (Rp)", min_value=0.0, step=1000.0, format="%.0f")

# Hitung cost subcon
subcon_total_hours = subcon_days * subcon_hours_per_day
subcon_total_cost = subcon_total_hours * subcon_cost_per_hour

st.success(f"Total Subcontractor Cost untuk {selected_category}: Rp {subcon_total_cost:,.0f}")
st.caption(f"Perhitungan: {subcon_total_hours:,.1f} jam x Rp {subcon_cost_per_hour:,.0f} per jam = Rp {subcon_total_cost:,.0f}")

# ===============================================
# Bagian Baru - Other Cost
st.header("8. Other Cost (Rupiah)")

transportation_cost = st.number_input("Biaya Transportasi (Rp)", min_value=0.0, step=10000.0, format="%.0f")
meal_cost = st.number_input("Biaya Konsumsi (Rp)", min_value=0.0, step=10000.0, format="%.0f")
contingency_cost = st.number_input("Contingency Fee (Rp)", min_value=0.0, step=10000.0, format="%.0f")
ehs_cost = st.number_input("Biaya EHS (Rp)", min_value=0.0, step=10000.0, format="%.0f")
other_cost = st.number_input("Biaya Lain-lain (Rp)", min_value=0.0, step=10000.0, format="%.0f")

total_other_cost = transportation_cost + meal_cost + contingency_cost + ehs_cost + other_cost

st.success(f"Total Other Cost: Rp {total_other_cost:,.0f}")

# ===============================================
# Total Final Cost & Margin Revisi
total_final_cost = total_cost_technician + subcon_total_cost + total_other_cost

st.header("🧾 Ringkasan Final Cost & Margin Revisi")
st.write(f"💰 **Total Final Cost: Rp {total_final_cost:,.0f}**")

margin_final = (offered_price_idr - total_final_cost) / offered_price_idr * 100 if offered_price_idr != 0 else 0

if margin_final < 40:
    st.error(f"⚠️ Margin (Revisi, berdasarkan total cost): {margin_final:.2f}% (Kurang dari 40%)")
else:
    st.success(f"✅ Margin (Revisi, berdasarkan total cost): {margin_final:.2f}%")

# ===============================================
# Download Data Excel
data = {
    "Item": [
        "Total PM Days",
        "Total ASD Days",
        "Total EC Days",
        "Total Hours",
        "Total Days",
        "Total Cost Teknisi (Rp)",
        f"Total Cost Subcontractor ({selected_category}) (Rp)",
        "Total Other Cost (Rp)",
        "Total Final Cost (Rp)",
        "Harga Ditawarkan (Rp)",
        "Margin (%) dari Teknisi",
        "Margin (%) dari Total Cost",
    ],
    "Value": [
        total_pm_days,
        total_asd_days,
        total_ec_days,
        total_hours,
        total_days,
        total_cost_technician,
        subcon_total_cost,
        total_other_cost,
        total_final_cost,
        offered_price_idr,
        margin,
        margin_final,
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
    file_name="kalkulator_biaya_pm_asd_ec_subcon_other_idr.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)
