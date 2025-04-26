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
    parent_margin = None

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

# Hitung Labour Cost
total_days = total_pm_days + total_asd_days + total_ec_days
total_hours = (total_pm_days * hours_per_day_pm) + (total_asd_days * hours_per_day_asd) + (total_ec_days * hours_per_day_ec)
total_cost_technician = total_hours * technician_unit_cost_per_hour_idr

# ===============================================
# Margin Labour
margin_labour = (offered_price_idr - total_cost_technician) / offered_price_idr * 100 if offered_price_idr != 0 else 0

st.subheader("📊 Labour Costing Margin Analysis")
st.write(f"🔹 Margin berdasarkan Labour Costing: {margin_labour:.2f}%")

if psa_type == "Renewal PSA" and parent_margin is not None:
    if margin_labour >= parent_margin:
        st.success(f"✅ Margin Labour ({margin_labour:.2f}%) memenuhi atau lebih besar dari Parent Margin ({parent_margin:.2f}%).")
    else:
        st.error(f"⚠️ Margin Labour ({margin_labour:.2f}%) LEBIH KECIL dari Parent Margin ({parent_margin:.2f}%). Harus diperbaiki!")

# ===============================================
# SUBCONTRACTOR WORKS (Dynamic)
st.header("👷 SUBCONTRACTOR WORKS (Optional)")

with st.expander("➕ Tambahkan Subcontractor Works"):
    add_subcon = st.checkbox("Centang untuk input biaya Subcontractor", value=False)

    if add_subcon:
        st.markdown("### 📋 List Pekerjaan Subcontractor")
        work_types = ["Helper", "Cooling Tower", "Pump", "Controls", "AHU", "Other HVAC Work"]
        subcontractor_details = []

        for work in work_types:
            st.subheader(f"🔹 {work}")
            days = st.number_input(f"Jumlah Hari {work}", min_value=0.0, step=0.5, format="%.1f", key=f"days_{work}")
            quantity = st.number_input(f"Quantity untuk {work}", min_value=0, step=1, format="%d", key=f"qty_{work}")
            cost_per_day = st.number_input(f"Biaya per Hari per Quantity {work} (Rp)", min_value=0.0, step=1000.0, format="%.0f", key=f"cost_{work}")

            total_cost = days * quantity * cost_per_day
            subcontractor_details.append({
                "Pekerjaan": work,
                "Jumlah Hari": days,
                "Quantity": quantity,
                "Harga per Hari per Quantity (Rp)": cost_per_day,
                "Total Cost (Rp)": total_cost
            })

        df_subcontractor = pd.DataFrame(subcontractor_details)

        st.dataframe(df_subcontractor.style.format({
            "Jumlah Hari": "{:.1f}",
            "Quantity": "{:d}",
            "Harga per Hari per Quantity (Rp)": "Rp {:,.0f}",
            "Total Cost (Rp)": "Rp {:,.0f}"
        }), use_container_width=True)

        total_subcontractor_cost = df_subcontractor["Total Cost (Rp)"].sum()

        st.success(f"💰 Total Subcontractor Cost: Rp {total_subcontractor_cost:,.0f}")

    else:
        total_subcontractor_cost = 0.0
        df_subcontractor = pd.DataFrame()

# (Bagian lanjut Other Cost, Spare Part, Final Summary, dan Export akan gue lanjutkan setelah ini karena panjang)

