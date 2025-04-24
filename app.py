import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Kalkulator Biaya Pekerjaan", layout="centered")

st.title("🛠️ Kalkulator Biaya Pekerjaan + Akomodasi")

# Bagian kerja
total_days = st.number_input("Total hari kerja", min_value=0.0, value=0.0, step=1.0)
cost_per_hour = st.number_input("Biaya per jam (USD)", min_value=0.0, value=16.69, step=0.1)
hours_per_day = st.number_input("Jam kerja per hari", min_value=0.0, value=8.0, step=0.5)

# Include Akomodasi
include_accommodation = st.checkbox("🧳 Sertakan Biaya Akomodasi & Perjalanan")

# Default biaya tambahan
flight_cost = 0
hotel_cost = 0
meal_cost = 0

if include_accommodation:
    st.subheader("✈️ Biaya Perjalanan dan Akomodasi")

    is_round_trip = st.radio("Tiket Pesawat", ["Sekali jalan", "Pulang-Pergi"], index=1)
    one_way_flight_price = st.number_input("Harga tiket sekali jalan (IDR)", min_value=0.0, value=800000.0, step=50000.0)
    flight_cost = one_way_flight_price * (2 if is_round_trip == "Pulang-Pergi" else 1)

    nightly_hotel_price = st.number_input("Harga hotel per malam (IDR)", min_value=0.0, value=750000.0, step=50000.0)
    stay_nights = st.number_input("Jumlah malam menginap", min_value=0, value=int(total_days), step=1)
    hotel_cost = nightly_hotel_price * stay_nights

    meal_cost = st.number_input("Total biaya makan (IDR)", min_value=0.0, value=1000000.0, step=50000.0)

# Kurs dan margin
kurs_usd_to_idr = st.number_input("Kurs USD ke IDR", min_value=0.0, value=16000.0, step=100.0)
margin_percent = st.number_input("Margin keuntungan (%)", min_value=0.0, value=20.0, step=1.0)

# Kalkulasi
total_hours = total_days * hours_per_day
total_cost_usd = total_hours * cost_per_hour
total_cost_idr = total_cost_usd * kurs_usd_to_idr
total_extras = flight_cost + hotel_cost + meal_cost
total_cost_with_extras = total_cost_idr + total_extras
final_price_idr = total_cost_with_extras * (1 + margin_percent / 100)
gross_margin_percent = ((final_price_idr - total_cost_with_extras) / final_price_idr * 100) if final_price_idr else 0

# Output
st.subheader("💰 Hasil Perhitungan:")
st.success(f"Total Jam Kerja: **{total_hours:.2f} jam**")
st.info(f"Biaya kerja (USD): **${total_cost_usd:,.2f}**")
st.info(f"Biaya kerja (IDR): **Rp {total_cost_idr:,.0f}**")

if include_accommodation:
    st.info(f"✈️ Biaya Pesawat: **Rp {flight_cost:,.0f}**")
    st.info(f"🏨 Biaya Hotel: **Rp {hotel_cost:,.0f}** ({stay_nights} malam)")
    st.info(f"🍽️ Biaya Makan: **Rp {meal_cost:,.0f}**")

st.warning(f"Total biaya: **Rp {total_cost_with_extras:,.0f}**")
st.success(f"Final Price: **Rp {final_price_idr:,.0f}**")
st.info(f"📈 Gross Margin: **{gross_margin_percent:.2f}%**")

# Export ke Excel
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
        writer.save()
    return output.getvalue()

st.markdown("### 📥 Export:")
if st.button("Download Hasil ke Excel"):
    excel_data = generate_excel()
    st.download_button(
        label="📄 Download Excel",
        data=excel_data,
        file_name="biaya_pekerjaan_dan_akomodasi.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
