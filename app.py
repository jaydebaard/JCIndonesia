import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Kalkulator Biaya Proyek", layout="centered")

st.title("🧮 Kalkulator Total Biaya Proyek + Akomodasi")

# Input user dasar
total_days = st.number_input("Total Hari Kerja", min_value=0.0, value=10.0)
cost_per_hour = st.number_input("Biaya per Jam (USD)", min_value=0.0, value=16.69)
hours_per_day = st.number_input("Jam Kerja per Hari", min_value=0.0, value=8.0)
kurs_usd_to_idr = st.number_input("Kurs USD ke IDR", min_value=0.0, value=16000.0)
currency = st.radio("Tampilkan Mata Uang", ["IDR (Rupiah)", "USD (Dollar)"]) 

# Optional: Biaya akomodasi
include_accommodation = st.checkbox("Include Akomodasi?")
if include_accommodation:
    flight_cost = st.number_input("Biaya Tiket Pesawat (IDR)", min_value=0.0, value=0.0)
    round_trip = st.checkbox("Round Trip?", value=True)
    if round_trip:
        flight_cost *= 2
    hotel_cost_per_night = st.number_input("Harga Hotel per Malam (IDR)", min_value=0.0, value=0.0)
    stay_nights = st.number_input("Jumlah Malam Menginap", min_value=0, value=int(total_days))
    hotel_cost = hotel_cost_per_night * stay_nights
    meal_cost = st.number_input("Biaya Makan (Total, IDR)", min_value=0.0, value=0.0)
else:
    flight_cost = hotel_cost = meal_cost = 0.0

margin_percent = st.number_input("Margin (%)", min_value=0.0, value=15.0)

# Perhitungan
total_hours = total_days * hours_per_day
total_cost_usd = total_hours * cost_per_hour
total_cost_idr = total_cost_usd * kurs_usd_to_idr
total_cost_with_extras = total_cost_idr + flight_cost + hotel_cost + meal_cost
final_price_idr = total_cost_with_extras * (1 + margin_percent / 100)
gross_margin_percent = ((final_price_idr - total_cost_with_extras) / final_price_idr * 100) if final_price_idr else 0

# Format tampilan mata uang
def format_currency(val):
    if currency == "USD (Dollar)":
        return f"${val / kurs_usd_to_idr:,.2f}"
    return f"Rp {val:,.0f}"

# Output hasil
st.subheader("💰 Hasil Perhitungan")
st.write(f"Total Jam Kerja: **{total_hours:,.2f} jam**")
st.write(f"Total Biaya Kerja: {format_currency(total_cost_idr)}")
if include_accommodation:
    st.write(f"Total Biaya Tiket: {format_currency(flight_cost)}")
    st.write(f"Total Biaya Hotel: {format_currency(hotel_cost)}")
    st.write(f"Total Biaya Makan: {format_currency(meal_cost)}")
st.write(f"Total Biaya (incl. extras): {format_currency(total_cost_with_extras)}")
st.write(f"Final Price (incl. margin): {format_currency(final_price_idr)}")
st.write(f"Gross Margin: **{gross_margin_percent:.2f}%**")

# Export Excel

def generate_excel():
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    workbook = writer.book
    worksheet = workbook.add_worksheet('Perhitungan')
    writer.sheets['Perhitungan'] = worksheet

    worksheet.write('A1', 'Deskripsi')
    worksheet.write('B1', 'Nilai')

    worksheet.write('A2', 'Total Hari Kerja')
    worksheet.write('B2', total_days)
    worksheet.write('A3', 'Jam Kerja per Hari')
    worksheet.write('B3', hours_per_day)
    worksheet.write_formula('B4', '=B2*B3')
    worksheet.write('A4', 'Total Jam Kerja')
    worksheet.write('A5', 'Biaya per Jam (USD)')
    worksheet.write('B5', cost_per_hour)
    worksheet.write_formula('B6', '=B4*B5')
    worksheet.write('A6', 'Total Biaya Kerja (USD)')
    worksheet.write('A7', 'Kurs ke IDR')
    worksheet.write('B7', kurs_usd_to_idr)
    worksheet.write_formula('B8', '=B6*B7')
    worksheet.write('A8', 'Total Biaya Kerja (IDR)')
    worksheet.write('A9', 'Tiket Pesawat (IDR)')
    worksheet.write('B9', flight_cost)
    worksheet.write('A10', 'Hotel (IDR)')
    worksheet.write('B10', hotel_cost)
    worksheet.write('A11', 'Meal (IDR)')
    worksheet.write('B11', meal_cost)
    worksheet.write_formula('B12', '=B8+B9+B10+B11')
    worksheet.write('A12', 'Total Biaya (IDR)')
    worksheet.write('A13', 'Margin (%)')
    worksheet.write('B13', margin_percent / 100)
    worksheet.write_formula('B14', '=B12*(1+B13)')
    worksheet.write('A14', 'Final Price (IDR)')
    worksheet.write_formula('B15', '=(B14-B12)/B14')
    worksheet.write('A15', 'Gross Margin (%)')

    rupiah_fmt = workbook.add_format({'num_format': '#,##0'})
    percent_fmt = workbook.add_format({'num_format': '0.00%'})
    worksheet.set_column('A:A', 30)
    worksheet.set_column('B:B', 20, rupiah_fmt)
    worksheet.set_row(14, None, percent_fmt)
    worksheet.set_row(15, None, percent_fmt)

    writer.close()
    output.seek(0)
    return output

st.markdown("---")
st.subheader("📄 Export ke Excel")
st.download_button(
    label="📄 Download Excel",
    data=generate_excel().getvalue(),
    file_name="kalkulasi_biaya.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
