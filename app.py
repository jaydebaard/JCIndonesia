import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Kalkulator Biaya Proyek", layout="centered")

st.title("🧮 Kalkulator Total Biaya Proyek + Akomodasi")

# Input data dasar
total_days = st.number_input("Total Hari Kerja", min_value=0.0, value=10.0)
cost_per_hour = st.number_input("Biaya per Jam (USD)", min_value=0.0, value=16.69)
hours_per_day = st.number_input("Jam Kerja per Hari", min_value=0.0, value=8.0)
kurs_usd_to_idr = st.number_input("Kurs USD ke IDR", min_value=0.0, value=16000.0)

# Optional: Akomodasi
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

# Margin
margin_percent = st.number_input("Margin (%)", min_value=0.0, value=15.0)

# Perhitungan
total_hours = total_days * hours_per_day
total_cost_usd = total_hours * cost_per_hour
total_cost_idr = total_cost_usd * kurs_usd_to_idr

# Biaya tambahan
total_cost_with_extras = total_cost_idr + flight_cost + hotel_cost + meal_cost
final_price_idr = total_cost_with_extras * (1 + margin_percent / 100)

# Gross Margin
gross_margin_percent = 0.0
if final_price_idr != 0:
    gross_margin_percent = ((final_price_idr - total_cost_with_extras) / final_price_idr) * 100

# Tampilkan hasil
st.subheader("💰 Hasil Perhitungan")
st.write(f"Total Jam Kerja: **{total_hours:.2f} jam**")
st.write(f"Total Biaya Kerja: **${total_cost_usd:.2f}** / **Rp {total_cost_idr:,.0f}**")
if include_accommodation:
    st.write(f"Total Biaya Tiket: Rp {flight_cost:,.0f}")
    st.write(f"Total Biaya Hotel: Rp {hotel_cost:,.0f}")
    st.write(f"Total Biaya Makan: Rp {meal_cost:,.0f}")
st.write(f"Total Biaya (incl. extras): **Rp {total_cost_with_extras:,.0f}**")
st.write(f"Final Price (incl. margin): **Rp {final_price_idr:,.0f}**")
st.write(f"Gross Margin: **{gross_margin_percent:.2f}%**")

# Fungsi export Excel
def generate_excel():
    df = pd.DataFrame({
        "Deskripsi": [
            "Total Hari Kerja",
            "Jam Kerja per Hari",
            "Total Jam Kerja",
            "Biaya per Jam (USD)",
            "Total Biaya Kerja (USD)",
            "Kurs ke IDR",
            "Total Biaya Kerja (IDR)",
            "Tiket Pesawat (IDR)",
            "Hotel (IDR)",
            "Meal (IDR)",
            "Total Biaya (IDR)",
            "Margin (%)",
            "Final Price (IDR)",
            "Gross Margin (%)"
        ],
        "Nilai": [
            total_days,
            hours_per_day,
            total_hours,
            cost_per_hour,
            total_cost_usd,
            kurs_usd_to_idr,
            total_cost_idr,
            flight_cost,
            hotel_cost,
            meal_cost,
            total_cost_with_extras,
            margin_percent,
            final_price_idr,
            gross_margin_percent
        ]
    })

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Perhitungan')
    output.seek(0)
    return output.getvalue()

# Tombol download
st.markdown("---")
st.subheader("📤 Export Hasil ke Excel")
excel_data = generate_excel()
st.download_button(
    label="📄 Download Excel",
    data=excel_data,
    file_name="biaya_pekerjaan_dan_akomodasi.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
