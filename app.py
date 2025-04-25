import streamlit as st
import pandas as pd
from io import BytesIO

# Set page config
st.set_page_config(page_title="Kalkulator Biaya PM, ASD, EC Chiller", layout="centered")
st.title("🧮 Kalkulator Biaya PM, ASD, dan EC Chiller")

st.header("1. Currency & Setting")
usd_to_idr = st.number_input("Kurs USD ke IDR", value=16000.0)

technician_unit_cost_per_hour = st.number_input("Cost per Hour Technician ($)", value=16.6)
ec_unit_cost_per_hour = st.number_input("Cost per Hour EC ($)", value=78.125)

st.header("2. Jumlah Chiller")
col1, col2 = st.columns(2)
with col1:
    no_air_cooled = st.number_input("Jumlah Air Cooled Chiller", min_value=0, step=1)
with col2:
    no_water_cooled = st.number_input("Jumlah Water Cooled Chiller", min_value=0, step=1)

st.header("3. Preventive Maintenance (PM)")
hours_per_day_pm = st.number_input("Jam kerja per hari untuk PM", value=8.0)
manpower_pm = st.number_input("Jumlah Teknisi untuk PM", min_value=1, step=1)

# --- Update Total PM Days berdasarkan Jumlah Chiller
total_pm_base_days = (no_air_cooled * 1) + (no_water_cooled / 2)  # 1 hari = 1 air cooled, 1 hari = 2 water cooled
total_pm_days = total_pm_base_days * manpower_pm

st.write(f"Total Hari PM berdasarkan chiller dan manpower: {total_pm_days:.2f} hari")

st.header("4. Annual Shutdown (ASD)")
asd_visits = st.number_input("Jumlah Kunjungan ASD (times)", min_value=0, step=1)
days_per_visit_asd = st.number_input("Jumlah Hari per Kunjungan ASD (bilangan bulat)", min_value=1, step=1, format="%d")
hours_per_day_asd = st.number_input("Jam kerja per hari untuk ASD", value=8.0)
total_asd_days = asd_visits * days_per_visit_asd

st.header("5. Emergency Call (EC)")
ec_visits = st.number_input("Jumlah Kunjungan EC (times)", min_value=0, step=1)
hours_per_day_ec = st.number_input("Jam kerja per hari untuk EC", value=6.0)
total_ec_days = ec_visits * 1

# Perhitungan Total Days
total_days = total_pm_days + total_asd_days + total_ec_days

# Breakdown Cost
cost_pm = total_pm_days * hours_per_day_pm * technician_unit_cost_per_hour
cost_asd = total_asd_days * hours_per_day_asd * technician_unit_cost_per_hour
cost_ec = total_ec_days * hours_per_day_ec * ec_unit_cost_per_hour

total_cost = cost_pm + cost_asd + cost_ec

st.header("6. Pricing")
customer_type = st.selectbox("Tipe Customer", options=["Private", "Government"])
unit_price = 160.0 if customer_type == "Private" else 112.5
ec_price_per_day = 468.75

# Breakdown Price
price_pm_asd = (total_pm_days + total_asd_days) * unit_price
price_ec = total_ec_days * ec_price_per_day

total_price = price_pm_asd + price_ec

# Margin
margin = (total_price - total_cost) / total_price * 100 if total_price != 0 else 0

st.header("📋 Hasil Perhitungan")
st.write(f"Total PM Days: {total_pm_days:.2f} hari")
st.write(f"Total ASD Days: {total_asd_days:.2f} hari")
st.write(f"Total EC Days: {total_ec_days:.2f} hari")
st.write(f"Total Days: {total_days:.2f} hari")
st.write("---")
st.subheader("Breakdown Cost:")
st.write(f"Cost PM: ${cost_pm:,.2f}")
st.write(f"Cost ASD: ${cost_asd:,.2f}")
st.write(f"Cost EC: ${cost_ec:,.2f}")
st.write(f"Total Cost: ${total_cost:,.2f}")
st.write("---")
st.subheader("Breakdown Price:")
st.write(f"Price PM + ASD: ${price_pm_asd:,.2f}")
st.write(f"Price EC: ${price_ec:,.2f}")
st.write(f"Total Price: ${total_price:,.2f}")
st.write("---")
st.subheader("Margin:")
st.write(f"{margin:.2f}%")

# Optional Tampilkan IDR
show_idr = st.checkbox("Tampilkan juga dalam IDR?")
if show_idr:
    st.write(f"Total Biaya (IDR): Rp {total_cost * usd_to_idr:,.0f}")
    st.write(f"Total Harga (IDR): Rp {total_price * usd_to_idr:,.0f}")

# Prepare data untuk download Excel
data = {
    "Item": [
        "Total PM Days",
        "Total ASD Days",
        "Total EC Days",
        "Total Days",
        "Cost PM ($)",
        "Cost ASD ($)",
        "Cost EC ($)",
        "Total Cost ($)",
        "Price PM+ASD ($)",
        "Price EC ($)",
        "Total Price ($)",
        "Margin (%)",
    ],
    "Value": [
        total_pm_days,
        total_asd_days,
        total_ec_days,
        total_days,
        cost_pm,
        cost_asd,
        cost_ec,
        total_cost,
        price_pm_asd,
        price_ec,
        total_price,
        margin,
    ],
}

df_result = pd.DataFrame(data)

# Button untuk download Excel
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Summary')
    processed_data = output.getvalue()
    return processed_data

st.download_button(
    label="📥 Download Hasil Breakdown ke Excel",
    data=to_excel(df_result),
    file_name="kalkulator_biaya_breakdown_pm_asd_ec.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)
