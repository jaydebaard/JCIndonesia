import streamlit as st
import pandas as pd
from io import BytesIO

# PAGE SETUP
st.set_page_config(page_title="Kalkulator Biaya Full PSA", layout="centered")
st.title("🧮 Kalkulator Biaya PSA: Labour, Subkontraktor, Other Cost, Spare Parts")

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

    technician_unit_cost_per_hour_idr = st.number_input("Biaya per Jam Teknisi (Rp)", value=265600.0, step=1000.0, format="%.0f")

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

    asd_visits = st.number_input("Jumlah Kunjungan ASD", min_value=0, step=1)
    days_per_visit_asd = st.number_input("Jumlah Hari per Kunjungan ASD", min_value=0.0, value=float(asd_visits), step=0.5)
    hours_per_day_asd = st.number_input("Jam kerja per hari ASD", value=8.0, step=0.5)
    total_asd_days = asd_visits * days_per_visit_asd

    ec_visits = st.number_input("Jumlah Kunjungan EC", min_value=0, step=1)
    hours_per_day_ec = st.number_input("Jam kerja per Hari EC", value=6.0, step=0.5)
    total_ec_days = ec_visits

    total_days = total_pm_days + total_asd_days + total_ec_days
    total_hours = (total_pm_days * hours_per_day_pm) + (total_asd_days * hours_per_day_asd) + (total_ec_days * hours_per_day_ec)
    total_cost_technician = total_hours * technician_unit_cost_per_hour_idr

    st.subheader("📊 Labour Cost Summary")
    st.write(f"🔹 Total Labour Cost: Rp {total_cost_technician:,.0f}")

    offered_price_idr = st.number_input("💵 Harga Ditawarkan (Rp)", min_value=0.0, step=1000.0, format="%.0f")

    margin_labour = (offered_price_idr - total_cost_technician) / offered_price_idr * 100 if offered_price_idr != 0 else 0
    st.write(f"🔹 Margin Labour Costing: {margin_labour:.2f}%")

    if psa_type == "Renewal PSA" and parent_margin is not None:
        if margin_labour >= parent_margin:
            st.success(f"✅ Margin Labour ({margin_labour:.2f}%) memenuhi atau lebih besar dari Parent Margin ({parent_margin:.2f}%).")
        else:
            st.error(f"⚠️ Margin Labour ({margin_labour:.2f}%) lebih kecil dari Parent Margin ({parent_margin:.2f}%). Harus diperbaiki!")
    elif psa_type == "New PSA":
        if margin_labour > 20:
            st.success(f"✅ Margin Labour ({margin_labour:.2f}%) bagus (lebih dari 20%).")
        else:
            st.error(f"⚠️ Margin Labour ({margin_labour:.2f}%) kurang dari 20%. Harus dinaikkan!")

# SUBCONTRACTOR WORKS
st.header("👷 SUBCONTRACTOR WORKS (Optional)")
with st.expander("➕ Tambahkan Subcontractor Works"):
    add_subcon = st.checkbox("Centang untuk input biaya Subcontractor", value=False)
    if add_subcon:
        work_types = ["Helper", "Cooling Tower", "Pump", "Controls", "AHU", "Other HVAC Work"]
        subcontractor_details = []
        for work in work_types:
            st.subheader(f"🔹 {work}")
            days = st.number_input(f"Jumlah Hari {work}", min_value=0.0, step=0.5, key=f"days_{work}")
            quantity = st.number_input(f"Quantity untuk {work}", min_value=0, step=1, key=f"qty_{work}")
            cost_per_day = st.number_input(f"Biaya per Hari per Quantity {work} (Rp)", min_value=0.0, step=1000.0, key=f"cost_{work}")
            total_cost = days * quantity * cost_per_day
            subcontractor_details.append({
                "Pekerjaan": work,
                "Jumlah Hari": days,
                "Quantity": quantity,
                "Harga per Hari per Quantity (Rp)": cost_per_day,
                "Total Cost (Rp)": total_cost
            })
        df_subcontractor = pd.DataFrame(subcontractor_details)
        st.dataframe(df_subcontractor)
        total_subcontractor_cost = df_subcontractor["Total Cost (Rp)"].sum()
        st.success(f"💰 Total Subcontractor Cost: Rp {total_subcontractor_cost:,.0f}")
    else:
        total_subcontractor_cost = 0.0
        df_subcontractor = pd.DataFrame()

# OTHER COSTS
st.header("💵 OTHER COSTS (Optional)")
with st.expander("➕ Tambahkan Other Costs"):
    add_other_cost = st.checkbox("Centang untuk input biaya lainnya", value=False)
    if add_other_cost:
        transportation_cost = st.number_input("Biaya Transportasi (Rp)", min_value=0.0, step=10000.0)
        meal_cost = st.number_input("Biaya Konsumsi (Rp)", min_value=0.0, step=10000.0)
        other_cost = st.number_input("Biaya Lain-lain (Rp)", min_value=0.0, step=10000.0)
        ehs_cost = 0.005 * (total_cost_technician + total_subcontractor_cost)
        subtotal_for_contingency = total_cost_technician + total_subcontractor_cost + transportation_cost + meal_cost + other_cost
        contingency_cost = 0.04 * subtotal_for_contingency
        total_other_cost = transportation_cost + meal_cost + other_cost + ehs_cost + contingency_cost
        st.success(f"Total Other Costs (Include EHS & Contingency): Rp {total_other_cost:,.0f}")
    else:
        transportation_cost = 0.0
        meal_cost = 0.0
        other_cost = 0.0
        ehs_cost = 0.0
        contingency_cost = 0.0
        total_other_cost = 0.0

# SPARE PARTS
st.header("🔧 SPARE PARTS (Optional)")
with st.expander("➕ Tambahkan Spare Parts"):
    add_spare_parts = st.checkbox("Centang untuk input biaya spare parts", value=False)
    if add_spare_parts:
        spare_parts_cost = st.number_input("Total Biaya Spare Parts (Rp)", min_value=0.0, step=10000.0)
    else:
        spare_parts_cost = 0.0

# FINAL CALCULATION
total_final_cost = total_cost_technician + total_subcontractor_cost + total_other_cost + spare_parts_cost
margin_final = (offered_price_idr - total_final_cost) / offered_price_idr * 100 if offered_price_idr != 0 else 0

st.header("🧾 FINAL SUMMARY")
st.metric(label="Total Final Cost (Rp)", value=f"Rp {total_final_cost:,.0f}")
if psa_type == "Renewal PSA":
    if margin_final < 40:
        st.error(f"⚠️ Margin Final: {margin_final:.2f}% (Di bawah 40%)")
    else:
        st.success(f"✅ Margin Final: {margin_final:.2f}% (Bagus)")
elif psa_type == "New PSA":
    if margin_final > 20:
        st.success(f"✅ Margin Final: {margin_final:.2f}% (Bagus, > 20%)")
    else:
        st.error(f"⚠️ Margin Final: {margin_final:.2f}% (Kurang dari 20%)")

# EXPORT EXCEL
def to_excel_multi(df_summary, df_subcontractor):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_summary.to_excel(writer, index=False, sheet_name='PSA Summary')
        if not df_subcontractor.empty:
            df_subcontractor.to_excel(writer, index=False, sheet_name='Subcontractor Details')
    return output.getvalue()

df_summary = pd.DataFrame({
    "Keterangan": [
        "PSA Type", "Parent Margin (%)", "Margin Labour (%)", "Labour Cost (Rp)",
        "Subcontractor Cost (Rp)", "Transportation Cost (Rp)", "Meal Cost (Rp)",
        "Other Manual Cost (Rp)", "EHS Cost (Rp)", "Contingency Cost (Rp)",
        "Spare Parts Cost (Rp)", "Total Final Cost (Rp)", "Offered Price (Rp)", "Margin Final (%)"
    ],
    "Hasil": [
        psa_type,
        parent_margin if parent_margin is not None else "-",
        f"{margin_labour:.2f}",
        f"Rp {total_cost_technician:,.0f}",
        f"Rp {total_subcontractor_cost:,.0f}",
        f"Rp {transportation_cost:,.0f}",
        f"Rp {meal_cost:,.0f}",
        f"Rp {other_cost:,.0f}",
        f"Rp {ehs_cost:,.0f}",
        f"Rp {contingency_cost:,.0f}",
        f"Rp {spare_parts_cost:,.0f}",
        f"Rp {total_final_cost:,.0f}",
        f"Rp {offered_price_idr:,.0f}",
        f"{margin_final:.2f}"
    ]
})

st.download_button(
    label="📥 Download Hasil ke Excel (Multi-Sheet)",
    data=to_excel_multi(df_summary, df_subcontractor),
    file_name="psa_full_costing_summary.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
