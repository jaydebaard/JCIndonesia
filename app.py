import streamlit as st
import pandas as pd
from io import BytesIO

# PAGE SETUP
st.set_page_config(page_title="Kalkulator Biaya Full PSA", layout="centered")
st.title("🧮 Kalkulator Biaya PSA: Labour, Subkontraktor, Other Cost, Spare Parts")

# PSA Type Selection
st.header("\ud83d\udccb PSA TYPE")
psa_type = st.radio("Apakah ini New PSA atau Renewal PSA?", ("New PSA", "Renewal PSA"))
if psa_type == "Renewal PSA":
    parent_margin = st.number_input("Masukkan Parent Margin (%)", min_value=0.0, max_value=100.0, step=0.1, format="%.1f")
else:
    parent_margin = None

# LABOUR COSTING
st.header("\ud83d\udee0\ufe0f LABOUR COSTING")
with st.container():
    st.subheader("\ud83d\udccb Input Dasar Labour Cost")

    default_usd = 16.69
    default_kurs = 16000.0

    if "technician_unit_cost_usd" not in st.session_state:
        st.session_state.technician_unit_cost_usd = default_usd
    if "usd_to_idr_rate" not in st.session_state:
        st.session_state.usd_to_idr_rate = default_kurs

    if st.button("\ud83d\udd04 Reset ke Default USD & Kurs"):
        st.session_state.technician_unit_cost_usd = default_usd
        st.session_state.usd_to_idr_rate = default_kurs

    col_usd, col_kurs = st.columns(2)
    with col_usd:
        technician_unit_cost_usd = st.number_input(
            "Harga per Jam Teknisi (USD)", value=st.session_state.technician_unit_cost_usd, step=0.01, format="%.2f", key="input_usd")
        st.session_state.technician_unit_cost_usd = technician_unit_cost_usd
    with col_kurs:
        usd_to_idr_rate = st.number_input(
            "Kurs USD ke IDR", value=st.session_state.usd_to_idr_rate, step=100.0, format="%.0f", key="input_kurs")
        st.session_state.usd_to_idr_rate = usd_to_idr_rate

    default_technician_unit_cost_per_hour_idr = technician_unit_cost_usd * usd_to_idr_rate

    technician_unit_cost_per_hour_idr = st.number_input(
        "Biaya per Jam Teknisi (Rp)", min_value=0.0, value=default_technician_unit_cost_per_hour_idr,
        step=1000.0, format="%.0f", key="input_cost_idr")

    st.caption(f"\ud83d\udca1 Biaya default dihitung dari: ${technician_unit_cost_usd:.2f} \u00d7 {usd_to_idr_rate:.0f} = Rp {default_technician_unit_cost_per_hour_idr:,.0f}")

    # Input PM, ASD, EC
    no_air_cooled = st.number_input("Jumlah Air Cooled Chiller", min_value=0, step=1)
    no_water_cooled = st.number_input("Jumlah Water Cooled Chiller", min_value=0, step=1)

    hours_per_day_pm = st.number_input("Jam kerja per hari PM", value=8.0, step=0.5)
    manpower_pm = st.number_input("Jumlah Teknisi PM", min_value=1, step=1)
    pm_visits = st.number_input("Jumlah Kunjungan PM", min_value=0, step=1)

    base_pm_days = (no_air_cooled * 1) + (no_water_cooled / 2)
    auto_total_pm_days = base_pm_days * pm_visits * manpower_pm
    total_pm_days = st.number_input("Total Hari PM", min_value=0.0, value=float(auto_total_pm_days), step=0.5)

    asd_visits = st.number_input("Jumlah Kunjungan ASD", min_value=0, step=1)
    days_per_visit_asd = st.number_input("Hari per Kunjungan ASD", min_value=0.0, value=float(asd_visits), step=0.5)
    hours_per_day_asd = st.number_input("Jam kerja per hari ASD", value=8.0, step=0.5)
    total_asd_days = asd_visits * days_per_visit_asd

    ec_visits = st.number_input("Jumlah Kunjungan EC", min_value=0, step=1)
    hours_per_day_ec = st.number_input("Jam kerja per Hari EC", value=6.0, step=0.5)
    total_ec_days = ec_visits

    total_days = total_pm_days + total_asd_days + total_ec_days
    total_hours = (total_pm_days * hours_per_day_pm) + (total_asd_days * hours_per_day_asd) + (total_ec_days * hours_per_day_ec)
    total_cost_technician = total_hours * technician_unit_cost_per_hour_idr

    st.subheader("\ud83d\udcca Labour Cost Summary")
    st.write(f"\ud83d\udd39 Total Labour Cost: Rp {total_cost_technician:,.0f}")

    offered_price_idr = st.number_input("\ud83d\udcb5 Harga Ditawarkan (Rp)", min_value=0.0, step=1000.0, format="%.0f")

    margin_labour = (offered_price_idr - total_cost_technician) / offered_price_idr * 100 if offered_price_idr != 0 else 0
    st.write(f"\ud83d\udd39 Margin Labour Costing: {margin_labour:.2f}%")

    if psa_type == "Renewal PSA" and parent_margin is not None:
        if margin_labour >= parent_margin:
            st.success(f"\u2705 Margin Labour ({margin_labour:.2f}%) memenuhi atau lebih besar dari Parent Margin ({parent_margin:.2f}%).")
        else:
            st.error(f"\u26a0\ufe0f Margin Labour ({margin_labour:.2f}%) lebih kecil dari Parent Margin ({parent_margin:.2f}%). Harus diperbaiki!")
    elif psa_type == "New PSA":
        if margin_labour > 20:
            st.success(f"\u2705 Margin Labour ({margin_labour:.2f}%) bagus (lebih dari 20%).")
        else:
            st.error(f"\u26a0\ufe0f Margin Labour ({margin_labour:.2f}%) kurang dari 20%. Harus dinaikkan!")

# SUBCONTRACTOR WORKS
st.header("\ud83d\udc77 SUBCONTRACTOR WORKS (Optional)")
subcontractor_details = []
with st.expander("\u2795 Tambahkan Subcontractor Works"):
    add_subcon = st.checkbox("Centang untuk input biaya Subkontraktor", value=False)
    if add_subcon:
        work_types = ["Helper", "Cooling Tower", "Pump", "Controls", "AHU", "Other HVAC Work"]
        for work in work_types:
            st.subheader(f"\ud83d\udd39 {work}")
            days = st.number_input(f"Jumlah Hari {work}", min_value=0.0, step=0.5, key=f"days_{work}")
            quantity = st.number_input(f"Quantity {work}", min_value=0, step=1, key=f"qty_{work}")
            cost_per_day = st.number_input(f"Biaya per Hari per Quantity {work} (Rp)", min_value=0.0, step=1000.0, key=f"cost_{work}")
            total_cost = days * quantity * cost_per_day
            subcontractor_details.append({
                "Pekerjaan": work,
                "Jumlah Hari": days,
                "Quantity": quantity,
                "Harga per Hari (Rp)": cost_per_day,
                "Total Cost (Rp)": total_cost
            })
        df_subcontractor = pd.DataFrame(subcontractor_details)
        st.dataframe(df_subcontractor)
        total_subcontractor_cost = df_subcontractor["Total Cost (Rp)"].sum()
        st.success(f"\ud83d\udcb0 Total Subcontractor Cost: Rp {total_subcontractor_cost:,.0f}")
    else:
        total_subcontractor_cost = 0.0

# OTHER COSTS
st.header("\ud83d\udcb5 OTHER COSTS (Optional)")
with st.expander("\u2795 Tambahkan Other Costs"):
    add_other_cost = st.checkbox("Centang untuk input biaya lainnya", value=False)
    if add_other_cost:
        transportation_cost = st.number_input("Biaya Transportasi (Rp)", min_value=0.0, step=10000.0)
        meal_cost = st.number_input("Biaya Konsumsi (Rp)", min_value=0.0, step=10000.0)
        other_cost = st.number_input("Biaya Lain-lain (Rp)", min_value=0.0, step=10000.0)
        ehs_cost = 0.005 * (total_cost_technician + total_subcontractor_cost)
        subtotal_for_contingency = total_cost_technician + total_subcontractor_cost + transportation_cost + meal_cost + other_cost
        contingency_cost = 0.04 * subtotal_for_contingency
        total_other_cost = transportation_cost + meal_cost + other_cost + ehs_cost + contingency_cost

        st.info(f"\ud83d\udd39 EHS (0.5% dari Labour+Subcon): Rp {ehs_cost:,.0f}")
        st.info(f"\ud83d\udd39 Contingency (4% dari subtotal biaya): Rp {contingency_cost:,.0f}")
        st.success(f"Total Other Costs (include EHS & Contingency): Rp {total_other_cost:,.0f}")
    else:
        transportation_cost = meal_cost = other_cost = ehs_cost = contingency_cost = total_other_cost = 0.0

# SPARE PARTS
st.header("\ud83d\udd27 SPARE PARTS (Optional)")
with st.expander("\u2795 Tambahkan Spare Parts"):
    add_spare_parts = st.checkbox("Centang untuk input biaya Spare Parts", value=False)
    if add_spare_parts:
        spare_parts_cost = st.number_input("Total Biaya Spare Parts (Rp)", min_value=0.0, step=10000.0)
    else:
        spare_parts_cost = 0.0

# FINAL SUMMARY
st.header("\ud83d\udcde FINAL SUMMARY")
total_final_cost = total_cost_technician + total_subcontractor_cost + total_other_cost + spare_parts_cost
margin_final = (offered_price_idr - total_final_cost) / offered_price_idr * 100 if offered_price_idr != 0 else 0

st.metric(label="Total Final Cost (Rp)", value=f"Rp {total_final_cost:,.0f}")
if psa_type == "Renewal PSA":
    if margin_final >= 40:
        st.success(f"✅ Margin Final: {margin_final:.2f}% (Bagus)")
    else:
        st.error(f"⚠️ Margin Final: {margin_final:.2f}% (Di bawah 40%)")
else:
    if margin_final > 20:
        st.success(f"✅ Margin Final: {margin_final:.2f}% (Bagus)")
    else:
        st.error(f"⚠️ Margin Final: {margin_final:.2f}% (Kurang dari 20%)")

# EXPORT EXCEL
def to_excel(df_summary, df_subcontractor):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_summary.to_excel(writer, index=False, sheet_name='Summary')
        if not df_subcontractor.empty:
            df_subcontractor.to_excel(writer, index=False, sheet_name='Subcontractor Details')
    return output.getvalue()

# Summary to export
df_summary = pd.DataFrame({
    "Item": ["Labour Cost", "Subcontractor Cost", "Other Cost", "Spare Parts Cost", "Total Final Cost", "Harga Ditawarkan", "Margin Final"],
    "Nilai": [
        f"Rp {total_cost_technician:,.0f}",
        f"Rp {total_subcontractor_cost:,.0f}",
        f"Rp {total_other_cost:,.0f}",
        f"Rp {spare_parts_cost:,.0f}",
        f"Rp {total_final_cost:,.0f}",
        f"Rp {offered_price_idr:,.0f}",
        f"{margin_final:.2f}%"
    ]
})

st.download_button(
    label="\ud83d\udcc2 Download Hasil ke Excel",
    data=to_excel(df_summary, df_subcontractor),
    file_name="psa_full_costing_summary.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
