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
        technician_unit_cost_usd = st.number_input(
            "Harga per Jam Teknisi (USD)", 
            value=st.session_state.technician_unit_cost_usd, step=0.01, format="%.2f", key="input_usd")
        st.session_state.technician_unit_cost_usd = technician_unit_cost_usd
    with col_kurs:
        usd_to_idr_rate = st.number_input(
            "Kurs USD ke IDR", 
            value=st.session_state.usd_to_idr_rate, step=100.0, format="%.0f", key="input_kurs")
        st.session_state.usd_to_idr_rate = usd_to_idr_rate

    default_technician_unit_cost_per_hour_idr = technician_unit_cost_usd * usd_to_idr_rate

    technician_unit_cost_per_hour_idr = st.number_input(
        "Biaya per Jam Teknisi (Rp)",
        min_value=0.0,
        value=default_technician_unit_cost_per_hour_idr,
        step=1000.0,
        format="%.0f",
        key="input_cost_idr"
    )

    st.caption(f"💡 Biaya default dihitung dari: ${technician_unit_cost_usd:.2f} × {usd_to_idr_rate:.0f} = Rp {default_technician_unit_cost_per_hour_idr:,.0f}")

    # Labour Planning
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
    st.write(f"🔹 Total Hari Kerja Labour (PM + ASD + EC): {total_days:.1f} hari")
    st.write(f"🔹 Total Jam Kerja Labour: {total_hours:.1f} jam")
    st.write(f"🔹 Biaya per Jam Teknisi: Rp {technician_unit_cost_per_hour_idr:,.0f}")
    st.write(f"🔹 Total Labour Cost: Rp {total_cost_technician:,.0f}")
    st.caption(f"💡 Perhitungan: Total Jam Kerja ({total_hours:.1f} jam) × Biaya per Jam (Rp {technician_unit_cost_per_hour_idr:,.0f}) = Rp {total_cost_technician:,.0f}")

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
        default_cost_per_day = 700000  # Harga fix Rp 700.000

        for work in work_types:
            st.subheader(f"🔹 {work}")
            
            if work == "Helper":
                default_days_helper = total_pm_days + total_asd_days + total_ec_days
                days = st.number_input(
                    f"Jumlah Hari pekerjaan {work} (default: {default_days_helper:.1f} hari)", 
                    min_value=0.0, 
                    value=float(default_days_helper), 
                    step=0.5, 
                    key=f"days_{work}"
                )
            else:
                days = st.number_input(f"Jumlah Hari pekerjaan {work}", min_value=0.0, step=0.5, key=f"days_{work}")

            jumlah = st.number_input(f"Jumlah Pekerja {work}", min_value=0, step=1, key=f"qty_{work}")
            cost_per_day = st.number_input(
                f"Harga Satuan per Hari untuk {work} (Rp)", 
                min_value=0.0, 
                value=float(default_cost_per_day), 
                step=1000.0, 
                key=f"cost_{work}"
            )

            total_cost = days * jumlah * cost_per_day

            subcontractor_details.append({
                "Pekerjaan": work,
                "Jumlah Hari": days,
                "Jumlah Pekerja": jumlah,
                "Harga per Hari per Pekerja (Rp)": cost_per_day,
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
        st.info(f"🔹 EHS (0.5% dari Labour+Subcon): Rp {ehs_cost:,.0f}")
        st.info(f"🔹 Contingency (4% dari Subtotal Manual): Rp {contingency_cost:,.0f}")
    else:
        transportation_cost = 0.0
        meal_cost = 0.0
        other_cost = 0.0
        ehs_cost = 0.0
        contingency_cost = 0.0
        total_other_cost = 0.0

# FINAL SUMMARY
st.header("📈 FINAL SUMMARY")

total_all_cost = total_cost_technician + total_subcontractor_cost + total_other_cost

if offered_price_idr > 0:
    final_margin_percentage = ((offered_price_idr - total_all_cost) / offered_price_idr) * 100
else:
    final_margin_percentage = 0

st.subheader("📊 Ringkasan Akhir")
st.write(f"💵 Harga Ditawarkan (Propose Price): Rp {offered_price_idr:,.0f}")
st.write(f"💰 Total Cost (Labour + Subcon + Other): Rp {total_all_cost:,.0f}")
st.write(f"📈 Margin Final: {final_margin_percentage:.2f}%")

# FINAL PRESENTATION TABLE
st.header("📋 Ringkasan Semua Komponen Cost & Margin")

final_summary_table = pd.DataFrame({
    "Komponen": [
        "Harga Ditawarkan (Propose Price)",
        "Total Labour Cost",
        "Total Subcontractor Cost",
        "Total Other Cost",
        "Total Keseluruhan Cost",
        "Margin Final (%)"
    ],
    "Nilai": [
        offered_price_idr,
        total_cost_technician,
        total_subcontractor_cost,
        total_other_cost,
        total_all_cost,
        f"{final_margin_percentage:.2f}%"
    ]
})

st.dataframe(final_summary_table)

# EXPORT TO EXCEL
st.header("📤 Export Data ke Excel")

def generate_excel():
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        workbook = writer.book

        # Summary Sheet
        summary_data = [
            ["Nama Proyek", project_name],
            [],
            ["Komponen", "Nilai (Rp)"],
            ["Harga Ditawarkan (Propose Price)", offered_price_idr],
            ["Total Labour Cost", total_cost_technician],
            ["Total Subcontractor Cost", total_subcontractor_cost],
            ["Total Other Cost", total_other_cost],
            ["Total Keseluruhan Cost", "=SUM(B5:B7)"],
            ["Margin Final (%)", "=(B4-B8)/B4"]
        ]
        df_summary = pd.DataFrame(summary_data)
        df_summary.to_excel(writer, index=False, header=False, sheet_name='Summary')

        # Labour Sheet (Detail)
        labour_detail = [
            ["Kategori", "Jumlah Hari", "Jam per Hari", "Total Jam", "Biaya per Jam", "Total Cost"],
            ["PM", total_pm_days, hours_per_day_pm, total_pm_days * hours_per_day_pm, technician_unit_cost_per_hour_idr, total_pm_days * hours_per_day_pm * technician_unit_cost_per_hour_idr],
            ["ASD", total_asd_days, hours_per_day_asd, total_asd_days * hours_per_day_asd, technician_unit_cost_per_hour_idr, total_asd_days * hours_per_day_asd * technician_unit_cost_per_hour_idr],
            ["EC", total_ec_days, hours_per_day_ec, total_ec_days * hours_per_day_ec, technician_unit_cost_per_hour_idr, total_ec_days * hours_per_day_ec * technician_unit_cost_per_hour_idr]
        ]
        df_labour = pd.DataFrame(labour_detail)
        df_labour.to_excel(writer, index=False, header=False, sheet_name='Labour Detail')

        # Subcontractor Sheet
        if not df_subcontractor.empty:
            df_subcontractor.to_excel(writer, index=False, sheet_name='Subcontractor Detail')

    output.seek(0)
    return output

excel_data = generate_excel()

st.download_button(
    label="📥 Download Hasil ke Excel",
    data=excel_data,
    file_name="Kalkulasi_Full_PSA.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
