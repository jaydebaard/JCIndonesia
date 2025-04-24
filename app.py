import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Kalkulator Proyek + Margin", layout="centered")
st.title("🧮 Kalkulator Proyek + Biaya + Gross Margin")

st.header("1. Input Biaya Kerja")
total_days = st.number_input("Total Hari Kerja", min_value=0.0, value=10.0)
hours_per_day = st.number_input("Jam Kerja per Hari", min_value=0.0, value=8.0)
cost_per_hour = st.number_input("Biaya per Jam (USD)", min_value=0.0, value=16.69)
kurs_usd_to_idr = st.number_input("Kurs USD ke IDR", min_value=0.0, value=16000.0)

# Akomodasi
st.header("2. Akomodasi")
include_accommodation = st.checkbox("Include Akomodasi?", value=True)
if include_accommodation:
    flight_cost = st.number_input("Biaya Tiket (IDR)", value=1_600_000.0)
    if st.checkbox("Round Trip?", value=True):
        flight_cost *= 2
    hotel_cost = st.number_input("Biaya Hotel per Malam (IDR)", value=700_000.0)
    stay_nights = st.number_input("Jumlah Malam Menginap", value=int(total_days))
    meal_cost = st.number_input("Biaya Makan (IDR)", value=1_000_000.0)
else:
    flight_cost = hotel_cost = meal_cost = stay_nights = 0.0

# Perhitungan total biaya kerja
total_hours = total_days * hours_per_day
total_cost_usd = total_hours * cost_per_hour
total_cost_idr = total_cost_usd * kurs_usd_to_idr
akomodasi_total = (hotel_cost * stay_nights) + flight_cost + meal_cost
total_biaya_kerja = total_cost_idr + akomodasi_total

# Input margin
margin_percent = st.number_input("Markup (%)", value=20.0)
harga_final = total_biaya_kerja * (1 + margin_percent / 100)
gross_margin = (harga_final - total_biaya_kerja) / harga_final * 100

# COST BREAKDOWN dari gambar
st.header("3. Input Biaya Proyek")
labour = st.number_input("Labour (IDR)", value=30_780_000.0)
sub_contractor = st.number_input("Sub-kontraktor (IDR)", value=14_000_000.0)
other_expenses = st.number_input("Other Expenses (IDR)", value=3_600_000.0)
freight = st.number_input("Freight (IDR)", value=2_600_000.0)
escalation = st.number_input("Eskalasi (IDR)", value=2_039_200.0)
contingency_percent = st.number_input("Contingency (%)", value=0.4)
contract_value = st.number_input("Nilai Kontrak (IDR)", value=130_000_000.0)

# Kalkulasi biaya proyek
subtotal = labour + sub_contractor + other_expenses
contingency = subtotal * (contingency_percent / 100)
total_estimate_cost = subtotal + freight + escalation + contingency
gross_profit = contract_value - total_estimate_cost
markup_contract = (gross_profit / total_estimate_cost * 100)
gross_margin_contract = (gross_profit / contract_value * 100)

# Output Hasil
st.subheader("💰 Hasil Perhitungan")
st.markdown(f"""
- **Total Jam Kerja:** {total_hours:,.2f} jam  
- **Total Biaya Kerja + Akomodasi:** Rp {total_biaya_kerja:,.0f}  
- **Harga Jual dengan Markup {margin_percent:.1f}%:** Rp {harga_final:,.0f}  
- **Gross Margin (Biaya Kerja):** {gross_margin:.2f}%  

---  
**Breakdown Proyek (CIS Style):**  
- Subtotal Biaya Langsung: Rp {subtotal:,.0f}  
- Contingency ({contingency_percent}%): Rp {contingency:,.0f}  
- Total Estimasi Biaya: Rp {total_estimate_cost:,.0f}  
- Gross Profit: Rp {gross_profit:,.0f}  
- Markup: {markup_contract:.1f}%  
- Gross Margin: {gross_margin_contract:.1f}%  
""")

# Fungsi export
def generate_excel():
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df = pd.DataFrame({
        "Deskripsi": [
            "Total Jam Kerja", "Biaya Kerja (IDR)", "Akomodasi", "Harga Final (Jual)",
            "Gross Margin Kerja", "", "Subtotal Proyek", "Contingency", "Total Estimate Cost",
            "Contract Value", "Gross Profit", "Markup (%)", "Gross Margin (%)"
        ],
        "Nilai": [
            total_hours, total_cost_idr, akomodasi_total, harga_final,
            gross_margin, "", subtotal, contingency, total_estimate_cost,
            contract_value, gross_profit, markup_contract, gross_margin_contract
        ]
    })
    df.to_excel(writer, index=False, sheet_name="Kalkulasi")

    workbook = writer.book
    worksheet = writer.sheets["Kalkulasi"]
    worksheet.set_column('A:A', 30)
    worksheet.set_column('B:B', 20, workbook.add_format({'num_format': '#,##0'}))
    writer.close()
    output.seek(0)
    return output

st.subheader("⬇️ Export Excel")
st.download_button(
    label="Download Excel",
    data=generate_excel().getvalue(),
    file_name="kalkulator_proyek.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
