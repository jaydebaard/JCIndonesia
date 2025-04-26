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
        st.session_state.technician_unit_cost_usd = technician_unit_cost_usd
    with col_kurs:
        usd_to_idr_rate = st.number_input("Kurs USD ke IDR", value=st.session_state.usd_to_idr_rate, step=100.0, format="%.0f", key="input_kurs")
        st.session_state.usd_to_idr_rate = usd_to_idr_rate

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

    asd_visits = st.number_input("Jumlah Kunjungan ASD", min_value=0, step=1)
    days_per_visit_asd = st.number_input("Jumlah Hari per Kunjungan ASD", min_value=0.0, step=0.5)
    hours_per_day_asd = st.number_input("Jam kerja per hari ASD", value=8.0, step=0.5)
    total_asd_days = asd_visits * days_per_visit_asd

    ec_visits = st.number_input("Jumlah Kunjungan EC", min_value=0, step=1)
    hours_per_day_ec = st.number_input("Jam kerja per Hari EC", value=6.0, step=0.5)
    total_ec_days = ec_visits

    # Travel Time
    travel_days = st.number_input("Jumlah Hari Travel Time", min_value=0.0, step=0.5)
    hours_per_day_travel = st.number_input("Jam kerja per hari Travel Time", value=8.0, step=0.5)

    # Total Labour
    total_days = total_pm_days + total_asd_days + total_ec_days + travel_days
    total_hours = (total_pm_days * hours_per_day_pm) + (total_asd_days * hours_per_day_asd) + (total_ec_days * hours_per_day_ec) + (travel_days * hours_per_day_travel)
    total_cost_technician = total_hours * technician_unit_cost_per_hour_idr

    st.subheader("📊 Labour Cost Summary")
    st.write(f"🔹 Total Hari Kerja Labour (PM + ASD + EC + Travel): {total_days:.1f} hari")
    st.write(f"🔹 Total Jam Kerja Labour: {total_hours:.1f} jam")
    st.write(f"🔹 Biaya per Jam Teknisi: Rp {technician_unit_cost_per_hour_idr:,.0f}")
    st.write(f"🔹 Total Labour Cost: Rp {total_cost_technician:,.0f}")
    st.caption(f"💡 Perhitungan: (Total Jam × Biaya per Jam) = Total Labour Cost")

    offered_price_idr = st.number_input("💵 Harga Ditawarkan (Rp)", min_value=0.0, step=1000.0, format="%.0f")

    margin_labour = (offered_price_idr - total_cost_technician) / offered_price_idr * 100 if offered_price_idr != 0 else 0
    st.write(f"🔹 Margin Labour Costing: {margin_labour:.2f}%")

# (sambung subcontractor, other cost, final summary, export excel di lanjutannya)

# SUBCONTRACTOR WORKS
st.header("👷 SUBCONTRACTOR WORKS (Optional)")
with st.expander("➕ Tambahkan Subcontractor Works"):
    add_subcon = st.checkbox("Centang untuk input biaya Subcontractor", value=False)
    if add_subcon:
        work_types = ["Helper", "Cooling Tower", "Pump", "Controls", "AHU", "Other HVAC Work"]
        subcontractor_details = []
        default_cost_per_day = 700000  # Default Harga per Hari

        for work in work_types:
            st.subheader(f"🔹 {work}")

            if work == "Helper":
                default_days_helper = total_pm_days + total_asd_days + total_ec_days + travel_days
                days = st.number_input(
                    f"Jumlah Hari {work} (default: {default_days_helper:.1f})", 
                    min_value=0.0, 
                    value=float(default_days_helper), 
                    step=0.5, 
                    key=f"days_{work}"
                )
            else:
                days = st.number_input(f"Jumlah Hari {work}", min_value=0.0, step=0.5, key=f"days_{work}")

            jumlah = st.number_input(f"Jumlah Pekerja {work}", min_value=0, step=1, key=f"qty_{work}")
            cost_per_day = st.number_input(
                f"Harga Satuan per Hari {work} (Rp)", 
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
st.write(f"💵 Harga Ditawarkan: Rp {offered_price_idr:,.0f}")
st.write(f"💰 Total Cost (Labour + Subcon + Other): Rp {total_all_cost:,.0f}")
st.write(f"📈 Margin Final: {final_margin_percentage:.2f}%")

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

        # Define formats
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D9E1F2', 'border': 1})
        currency_format = workbook.add_format({'num_format': '#,##0', 'border': 1})
        percent_format = workbook.add_format({'num_format': '0.00%', 'border': 1})
        normal_format = workbook.add_format({'border': 1})

        ## Summary
        summary_sheet = workbook.add_worksheet('Summary')
        summary_sheet.write('A1', 'Nama Proyek', header_format)
        summary_sheet.write('B1', project_name, normal_format)

        summary_sheet.write('A3', 'Komponen', header_format)
        summary_sheet.write('B3', 'Nilai (Rp)', header_format)
        summary_sheet.write('A4', 'Harga Ditawarkan', normal_format)
        summary_sheet.write_number('B4', offered_price_idr, currency_format)
        summary_sheet.write('A5', 'Total Labour Cost', normal_format)
        summary_sheet.write_number('B5', total_cost_technician, currency_format)
        summary_sheet.write('A6', 'Total Subcontractor Cost', normal_format)
        summary_sheet.write_number('B6', total_subcontractor_cost, currency_format)
        summary_sheet.write('A7', 'Total Other Cost', normal_format)
        summary_sheet.write_number('B7', total_other_cost, currency_format)
        summary_sheet.write('A8', 'Total Keseluruhan Cost', header_format)
        summary_sheet.write_formula('B8', '=SUM(B5:B7)', currency_format)
        summary_sheet.write('A9', 'Margin Final (%)', header_format)
        summary_sheet.write_formula('B9', '=(B4-B8)/B4', percent_format)
        summary_sheet.set_column('A:B', 25)

        ## Labour Detail
        labour_sheet = workbook.add_worksheet('Labour Detail')
        labour_sheet.write_row('A1', ['Kategori', 'Jumlah Hari', 'Jam per Hari', 'Total Jam', 'Biaya per Jam', 'Total Cost'], header_format)

        labour_rows = [
            ['PM', total_pm_days, hours_per_day_pm],
            ['ASD', total_asd_days, hours_per_day_asd],
            ['EC', total_ec_days, hours_per_day_ec],
            ['Travel Time', travel_days, hours_per_day_travel]
        ]

        for idx, (kategori, hari, jam) in enumerate(labour_rows, start=2):
            labour_sheet.write(f'A{idx}', kategori, normal_format)
            labour_sheet.write_number(f'B{idx}', hari, normal_format)
            labour_sheet.write_number(f'C{idx}', jam, normal_format)
            labour_sheet.write_formula(f'D{idx}', f'=B{idx}*C{idx}', normal_format)
            labour_sheet.write_number(f'E{idx}', technician_unit_cost_per_hour_idr, currency_format)
            labour_sheet.write_formula(f'F{idx}', f'=D{idx}*E{idx}', currency_format)

        labour_sheet.set_column('A:F', 20)

        ## Subcontractor Detail
        if not df_subcontractor.empty:
            subcon_sheet = workbook.add_worksheet('Subcontractor Detail')
            subcon_sheet.write_row('A1', ['Pekerjaan', 'Jumlah Hari', 'Jumlah Pekerja', 'Harga per Hari', 'Total Cost'], header_format)

            for idx, row in enumerate(df_subcontractor.itertuples(index=False), start=2):
                subcon_sheet.write(f'A{idx}', row[0], normal_format)
                subcon_sheet.write_number(f'B{idx}', row[1], normal_format)
                subcon_sheet.write_number(f'C{idx}', row[2], normal_format)
                subcon_sheet.write_number(f'D{idx}', row[3], currency_format)
                subcon_sheet.write_formula(f'E{idx}', f'=B{idx}*C{idx}*D{idx}', currency_format)

            subcon_sheet.set_column('A:E', 22)

    output.seek(0)
    return output

# Button Export Excel
excel_data = generate_excel()

st.download_button(
    label="📥 Download Hasil ke Excel",
    data=excel_data,
    file_name="Kalkulasi_Full_PSA_Detail.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
