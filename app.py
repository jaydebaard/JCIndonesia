import streamlit as st
import pandas as pd
from io import BytesIO

# ===============================================
# PAGE SETUP
st.set_page_config(page_title="Kalkulator Biaya Full PSA", layout="centered")
st.title("🧮 Kalkulator Biaya PSA: Labour, Subkontraktor, Other Cost, Spare Parts")

# ===============================================
# PSA Type Selection
st.header("📋 PSA TYPE")

psa_type = st.radio(
    "Apakah ini New PSA atau Renewal PSA?",
    ("New PSA", "Renewal PSA")
)

if psa_type == "Renewal PSA":
    parent_margin = st.number_input("Masukkan Parent Margin (%)", min_value=0.0, max_value=100.0, step=0.1, format="%.1f")
else:
    parent_margin = None  # Tidak relevan untuk New PSA

# ===============================================
# LABOUR COSTING
st.header("🛠️ LABOUR COSTING")

st.subheader("1. Cost Setting (Technician Rate)")
technician_unit_cost_per_hour_idr = st.number_input("Biaya per Jam Teknisi (Rp)", value=265600.0, step=1000.0, format="%.0f")

st.subheader("2. Jumlah Chiller")
col1, col2 = st.columns(2)
with col1:
    no_air_cooled = st.number_input("Jumlah Air Cooled Chiller", min_value=0, step=1, format="%d")
with col2:
    no_water_cooled = st.number_input("Jumlah Water Cooled Chiller", min_value=0, step=1, format="%d")

st.subheader("3. Preventive Maintenance (PM)")
hours_per_day_pm = st.number_input("Jam kerja per hari PM", value=8.0, step=0.5, format="%.1f")
manpower_pm = st.number_input("Jumlah Teknisi PM", min_value=1, step=1, format="%d")
pm_visits = st.number_input("Jumlah Kunjungan PM", min_value=0, step=1, format="%d")

base_pm_days = (no_air_cooled * 1) + (no_water_cooled / 2)
auto_total_pm_days = base_pm_days * pm_visits * manpower_pm
total_pm_days = st.number_input("Total Hari PM (auto/mau edit manual)", min_value=0.0, value=float(auto_total_pm_days), step=0.5, format="%.1f")

st.subheader("4. Annual Shutdown (ASD)")
asd_visits = st.number_input("Jumlah Kunjungan ASD", min_value=0, step=1, format="%d")
days_per_visit_asd = st.number_input("Jumlah Hari per Kunjungan ASD", min_value=0.0, value=float(asd_visits), step=0.5, format="%.1f")
hours_per_day_asd = st.number_input("Jam kerja per hari ASD", value=8.0, step=0.5, format="%.1f")
total_asd_days = asd_visits * days_per_visit_asd

st.subheader("5. Emergency Call (EC)")
ec_visits = st.number_input("Jumlah Kunjungan EC", min_value=0, step=1, format="%d")
hours_per_day_ec = st.number_input("Jam kerja per Hari EC", value=6.0, step=0.5, format="%.1f")
total_ec_days = ec_visits

st.subheader("6. Harga Yang Ditawarkan")
offered_price_idr = st.number_input("Harga Ditawarkan (Rp)", min_value=0.0, step=1000.0, format="%.0f")

# Hitungan Labour Cost
total_days = total_pm_days + total_asd_days + total_ec_days
total_hours = (total_pm_days * hours_per_day_pm) + (total_asd_days * hours_per_day_asd) + (total_ec_days * hours_per_day_ec)
total_cost_technician = total_hours * technician_unit_cost_per_hour_idr

# Margin Labour
margin_labour = (offered_price_idr - total_cost_technician) / offered_price_idr * 100 if offered_price_idr != 0 else 0

# ===============================================
# LABOUR Margin Analysis
st.subheader("📊 Labour Costing Margin Analysis")
st.write(f"🔹 Margin berdasarkan Labour Costing: {margin_labour:.2f}%")

if psa_type == "Renewal PSA" and parent_margin is not None:
    if margin_labour >= parent_margin:
        st.success(f"✅ Margin Labour ({margin_labour:.2f}%) memenuhi atau lebih besar dari Parent Margin ({parent_margin:.2f}%).")
    else:
        st.error(f"⚠️ Margin Labour ({margin_labour:.2f}%) LEBIH KECIL dari Parent Margin ({parent_margin:.2f}%). Harus diperbaiki!")

# ===============================================
# SUBCONTRACTOR WORKS
st.header("👷 SUBCONTRACTOR WORKS (Optional)")
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
        cleaning_cost_per_hour = st.number_input("Biaya per Jam Cleaning (Rp)", min_value=0.0, value=62500.0, step=1000.0, format="%.0f")
        cleaning_total_cost = cleaning_days * cleaning_hours_per_day * cleaning_cost_per_hour

        st.subheader("Other Subcontractor Work")
        other_days = st.number_input("Jumlah Hari Other Subcon", min_value=0.0, step=0.5, format="%.1f")
        other_hours_per_day = st.number_input("Jam kerja per Hari Other Subcon", min_value=0.0, value=8.0, step=0.5, format="%.1f")
        other_cost_per_hour = st.number_input("Biaya per Jam Other Subcon (Rp)", min_value=0.0, step=1000.0, format="%.0f")
        other_total_cost = other_days * other_hours_per_day * other_cost_per_hour

        total_subcontractor_cost = helper_total_cost + cleaning_total_cost + other_total_cost
    else:
        total_subcontractor_cost = 0.0

# ===============================================
# OTHER COSTS
st.header("💵 OTHER COSTS (Optional)")
with st.expander("➕ Tambahkan Other Costs"):
    add_other_cost = st.checkbox("Centang untuk input biaya lainnya", value=False)
    if add_other_cost:
        transportation_cost = st.number_input("Biaya Transportasi (Rp)", min_value=0.0, step=10000.0, format="%.0f")
        meal_cost = st.number_input("Biaya Konsumsi (Rp)", min_value=0.0, step=10000.0, format="%.0f")
        other_cost = st.number_input("Biaya Lain-lain (Rp)", min_value=0.0, step=10000.0, format="%.0f")

        ehs_cost = 0.005 * offered_price_idr
        contingency_cost = 0.04 * offered_price_idr

        st.write(f"🔒 EHS (0.5% dari Harga Ditawarkan): Rp {ehs_cost:,.0f}")
        st.write(f"🔒 Contingency Fee (4% dari Harga Ditawarkan): Rp {contingency_cost:,.0f}")

        total_other_cost = transportation_cost + meal_cost + other_cost + ehs_cost + contingency_cost
    else:
        total_other_cost = 0.0

# ===============================================
# SPARE PARTS
st.header("🔧 SPARE PARTS (Optional)")
with st.expander("➕ Tambahkan Spare Parts"):
    add_spare_parts = st.checkbox("Centang untuk input biaya spare parts", value=False)
    if add_spare_parts:
        spare_parts_cost = st.number_input("Total Biaya Spare Parts (Rp)", min_value=0.0, step=10000.0, format="%.0f")
    else:
        spare_parts_cost = 0.0

# ===============================================
# FINAL COST CALCULATION
total_final_cost = total_cost_technician + total_subcontractor_cost + total_other_cost + spare_parts_cost
margin_final = (offered_price_idr - total_final_cost) / offered_price_idr * 100 if offered_price_idr != 0 else 0

# ===============================================
# FINAL SUMMARY
st.header("🧾 FINAL SUMMARY")

st.metric(label="Total Final Cost (Rp)", value=f"Rp {total_final_cost:,.0f}")
if margin_final < 40:
    st.error(f"⚠️ Margin Final: {margin_final:.2f}% (Kurang dari 40%)")
else:
    st.success(f"✅ Margin Final: {margin_final:.2f}% (Bagus)")

# ===============================================
# PRICE vs COST ANALYSIS
st.header("🧩 Price vs Cost Analysis")
if margin_final >= 40 and offered_price_idr >= total_final_cost:
    st.success("✅ Harga dan Margin sudah BAGUS. Siap lanjut ke offering atau negosiasi.")
elif margin_final < 40 and offered_price_idr >= total_final_cost:
    st.warning("⚠️ Harga cukup, tapi Margin kurang dari 40%. Perlu cek ulang Cost atau Price.")
elif offered_price_idr < total_final_cost:
    st.error("❌ Harga ditawarkan LEBIH KECIL dari Total Cost. HARUS dinaikkan sebelum submit.")
else:
    st.warning("⚠️ Perlu review antara Harga dan Cost.")

