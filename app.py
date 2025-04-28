import streamlit as st
import pandas as pd
from io import BytesIO

# PAGE SETUP
st.set_page_config(page_title="Kalkulator Biaya Full PSA", layout="centered")
st.title("🧮 Kalkulator Biaya PSA: Labour, Subkontraktor, Other Cost, Spare Parts")

# INPUT PROJECT NAME
st.header("📋 Nama Proyek")
project_name = st.text_input("Masukkan Nama Proyek", "")

# PSA Type Selection
st.header("📋 PSA TYPE")
psa_type = st.radio("Apakah ini New PSA atau Renewal PSA?", ("New PSA", "Renewal PSA"))
if psa_type == "Renewal PSA":
    parent_margin = st.number_input("Masukkan Parent Margin (%)", min_value=0.0, max_value=100.0, step=0.1, format="%.1f")
else:
    parent_margin = None

# LABOUR COSTING
st.header("🛠️ LABOUR COSTING")
with st.container():
    st.subheader("📋 Input Dasar Labour Cost")

    default_usd = 16.69
    default_kurs = 16000.0

    if "technician_unit_cost_usd" not in st.session_state:
        st.session_state.technician_unit_cost_usd = default_usd
    if "usd_to_idr_rate" not in st.session_state:
        st.session_state.usd_to_idr_rate = default_kurs

    if st.button("🔄 Reset ke Default USD & Kurs"):
        st.session_state.technician_unit_cost_usd = default_usd
        st.session_state.usd_to_idr_rate = default_kurs

    col_usd, col_kurs = st.columns(2)
    with col_usd:
        technician_unit_cost_usd = st.number_input("Harga per Jam Teknisi (USD)", value=st.session_state.technician_unit_cost_usd, step=0.01, format="%.2f", key="input_usd")
    with col_kurs:
        usd_to_idr_rate = st.number_input("Kurs USD ke IDR", value=st.session_state.usd_to_idr_rate, step=100.0, format="%.0f", key="input_kurs")

    default_technician_unit_cost_per_hour_idr = technician_unit_cost_usd * usd_to_idr_rate
    technician_unit_cost_per_hour_idr = st.number_input("Biaya per Jam Teknisi (Rp)", min_value=0.0, value=default_technician_unit_cost_per_hour_idr, step=1000.0, format="%.0f", key="input_cost_idr")

    st.caption(f"💡 Biaya default dihitung dari: ${technician_unit_cost_usd:.2f} × {usd_to_idr_rate:.0f} = Rp {default_technician_unit_cost_per_hour_idr:,.0f}")

    # Labour Planning
    st.subheader("📋 Perencanaan Labour Cost")
    col1, col2 = st.columns(2)
    with col1:
        no_air_cooled = st.number_input("Jumlah Air Cooled Chiller", min_value=0, step=1)
    with col2:
        no_water_cooled = st.number_input("Jumlah Water Cooled Chiller", min_value=0, step=1)

    hours_per_day_pm = st.number_input("Jam kerja per hari PM", value=8.0, step=0.5)
    manpower_pm = st.number_input("Jumlah Teknisi PM", min_value=1, step=1)
    pm_visits = st.number_input("Jumlah Kunjungan PM", min_value=0, step=1)

    base_pm_days = (no_air_cooled * 1) + (no_water_cooled / 2)
    auto_total_pm_days = base_pm_days * pm_visits * manpower_pm
    total_pm_days = st.number_input("Total Hari PM (auto/mau edit manual)", min_value=0.0, value=float(auto_total_pm_days), step=0.5)

    # Hitung otomatis default ASD Days per Visit
    default_days_per_visit_asd = (no_air_cooled * 2) + (no_water_cooled * 4)

    if "days_per_visit_asd" not in st.session_state:
        st.session_state.days_per_visit_asd = default_days_per_visit_asd

    if default_days_per_visit_asd != st.session_state.days_per_visit_asd:
        st.session_state.days_per_visit_asd = default_days_per_visit_asd

    days_per_visit_asd = st.number_input(
        "Jumlah Hari per Kunjungan ASD",
        min_value=0.0,
        value=st.session_state.days_per_visit_asd,
        step=0.5,
        key="input_days_per_visit_asd"
    )

    asd_visits = st.number_input("Jumlah Kunjungan ASD", min_value=0, step=1)
    total_asd_days = asd_visits * days_per_visit_asd

    ec_visits = st.number_input("Jumlah Kunjungan EC", min_value=0, step=1)
    hours_per_day_ec = st.number_input("Jam kerja per Hari EC", value=6.0, step=0.5)
    total_ec_days = ec_visits

    travel_days = st.number_input("Jumlah Hari Travel Time", min_value=0.0, step=0.5)
    hours_per_day_travel = st.number_input("Jam kerja per hari Travel Time", value=8.0, step=0.5)

    total_days = total_pm_days + total_asd_days + total_ec_days + travel_days
    total_hours = (total_pm_days * hours_per_day_pm) + (total_asd_days * days_per_visit_asd) + (total_ec_days * hours_per_day_ec) + (travel_days * hours_per_day_travel)
    total_cost_technician = total_hours * technician_unit_cost_per_hour_idr

    st.subheader("📊 Labour Cost Summary")
    st.write(f"🔹 Total Hari Kerja Labour (PM + ASD + EC + Travel): {total_days:.1f} hari")
    st.write(f"🔹 Total Jam Kerja Labour: {total_hours:.1f} jam")
    st.write(f"🔹 Biaya per Jam Teknisi: Rp {technician_unit_cost_per_hour_idr:,.0f}")
    st.write(f"🔹 Total Labour Cost: Rp {total_cost_technician:,.0f}")

    offered_price_idr = st.number_input("💵 Harga Ditawarkan (Rp)", min_value=0.0, step=1000.0, format="%.0f")

    margin_labour = (offered_price_idr - total_cost_technician) / offered_price_idr * 100 if offered_price_idr != 0 else 0
    st.write(f"🔹 Margin Labour Costing: {margin_labour:.2f}%")

# Analisa Margin Labour
if psa_type == "New PSA":
    if margin_labour >= 20:
        st.success(f"✅ Margin Labour ({margin_labour:.2f}%) memenuhi syarat New PSA (≥ 20%). OK!")
    else:
        st.error(f"⚠️ Margin Labour ({margin_labour:.2f}%) kurang dari syarat 20%. Harus dinaikkan.")
elif psa_type == "Renewal PSA":
    if parent_margin is not None:
        if margin_labour > parent_margin:
            st.success(f"✅ Margin Labour ({margin_labour:.2f}%) lebih besar dari Parent Margin ({parent_margin:.2f}%). OK!")
        else:
            st.error(f"⚠️ Margin Labour ({margin_labour:.2f}%) lebih kecil dari Parent Margin ({parent_margin:.2f}%). Harus diperbaiki.")

# Next steps: subcontractor, other cost, final summary, export excel...

