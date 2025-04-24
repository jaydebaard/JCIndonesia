import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Kalkulator Biaya Kunjungan", layout="centered")
st.title("🧮 Kalkulator Biaya & Margin Kunjungan Teknisi")

# Input dari pengguna
kurs_usd_to_idr = st.number_input("Kurs USD ke IDR", min_value=0.0, value=16000.0)
no_asd = st.number_input("Jumlah Kunjungan ASD", min_value=0, value=2)
no_pm = st.number_input("Jumlah Kunjungan PM", min_value=0, value=2)
no_ec = st.number_input("Jumlah EC", min_value=0, value=1)
no_chiller = st.number_input("Jumlah Chiller", min_value=1, value=2)
hours_per_day = st.slider("Jam kerja per hari", min_value=6.0, max_value=8.0, value=8.0, step=0.5)
no_technician = st.number_input("Jumlah Teknisi", min_value=1, value=2)
unit_cost_usd = st.number_input("Biaya Teknisi per Jam (USD)", min_value=0.0, value=16.6)
ec_unit_cost_usd = 132.8

# Hitung total visit dan jam kerja
total_visits = (no_asd + no_pm) * no_chiller / 2  # 1 teknisi bisa servis 2 chiller per visit
total_hours = no_technician * total_visits * hours_per_day
total_cost_usd = total_hours * unit_cost_usd + (no_ec * ec_unit_cost_usd)
total_cost_idr = total_cost_usd * kurs_usd_to_idr

# Harga jual tetap
customer_type = st.radio("Jenis Customer", ["Private", "Government"])
unit_price_idr = 2560000 if customer_type == "Private" else 1800000
ec_price_idr = 8000000
total_price_idr = (total_hours * unit_price_idr) + (no_ec * ec_price_idr)

# Margin
margin_percent = ((total_price_idr - total_cost_idr) / total_cost_idr * 100) if total_cost_idr else 0

# Tampilkan hasil
st.subheader("📊 Hasil Perhitungan")
st.write(f"Total Kunjungan: **{total_visits:.2f} kali**")
st.write(f"Total Jam Kerja: **{total_hours:.2f} jam**")
st.write(f"Total Biaya (USD): **${total_cost_usd:,.2f}**")
st.write(f"Total Biaya (IDR): **Rp {total_cost_idr:,.0f}**")
st.write(f"Total Harga Jual (IDR): **Rp {total_price_idr:,.0f}**")
st.write(f"Margin Kotor: **{margin_percent:.2f}%**")

# Fungsi export Excel
def generate_excel():
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    workbook = writer.book
    worksheet = workbook.add_worksheet('Perhitungan')
    writer.sheets['Perhitungan'] = worksheet

    worksheet.write('A1', 'Deskripsi')
    worksheet.write('B1', 'Nilai')

    worksheet.write('A2', 'Jumlah ASD')
    worksheet.write('B2', no_asd)
    worksheet.write('A3', 'Jumlah PM')
    worksheet.write('B3', no_pm)
    worksheet.write('A4', 'Jumlah EC')
    worksheet.write('B4', no_ec)
    worksheet.write('A5', 'Jumlah Chiller')
    worksheet.write('B5', no_chiller)
    worksheet.write('A6', 'Jam per Hari')
    worksheet.write('B6', hours_per_day)
    worksheet.write('A7', 'Jumlah Teknisi')
    worksheet.write('B7', no_technician)
    worksheet.write('A8', 'Total Kunjungan')
    worksheet.write('B8', total_visits)
    worksheet.write('A9', 'Total Jam')
    worksheet.write('B9', total_hours)
    worksheet.write('A10', 'Biaya Teknisi/jam (USD)')
    worksheet.write('B10', unit_cost_usd)
    worksheet.write('A11', 'Biaya EC/unit (USD)')
    worksheet.write('B11', ec_unit_cost_usd)
    worksheet.write('A12', 'Total Cost (USD)')
    worksheet.write('B12', total_cost_usd)
    worksheet.write('A13', 'Kurs USD ke IDR')
    worksheet.write('B13', kurs_usd_to_idr)
    worksheet.write('A14', 'Total Cost (IDR)')
    worksheet.write('B14', total_cost_idr)
    worksheet.write('A15', 'Unit Price (IDR)')
    worksheet.write('B15', unit_price_idr)
    worksheet.write('A16', 'EC Price (IDR)')
    worksheet.write('B16', ec_price_idr)
    worksheet.write('A17', 'Total Price (IDR)')
    worksheet.write('B17', total_price_idr)
    worksheet.write('A18', 'Gross Margin (%)')
    worksheet.write('B18', margin_percent)

    rupiah_fmt = workbook.add_format({'num_format': '#,##0'})
    percent_fmt = workbook.add_format({'num_format': '0.00%'})
    worksheet.set_column('A:A', 30)
    worksheet.set_column('B:B', 20, rupiah_fmt)
    worksheet.set_row(17, None, percent_fmt)

    writer.close()
    output.seek(0)
    return output

# Tombol export
st.markdown("---")
st.subheader("📄 Export ke Excel")
st.download_button(
    label="📄 Download Excel",
    data=generate_excel().getvalue(),
    file_name="kalkulasi_kunjungan.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
