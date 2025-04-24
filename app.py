import streamlit as st

st.set_page_config(page_title="Kalkulator Biaya Kunjungan", layout="centered")
st.title("🧮 Kalkulator Biaya & Margin Kunjungan Teknisi")

kurs = st.number_input("Kurs USD ke IDR", value=16000.0)
no_asd = st.number_input("Jumlah Kunjungan ASD", value=2, step=1, format="%d")
no_pm = st.number_input("Jumlah Kunjungan PM", value=2, step=1, format="%d")
no_ec = st.number_input("Jumlah EC", value=1, step=1, format="%d")
no_chiller = st.number_input("Jumlah Chiller", value=2, step=1, format="%d")
hours_per_day = st.slider("Jam kerja per hari", min_value=6.0, max_value=8.0, value=8.0, step=0.5)
no_technician = st.number_input("Jumlah Teknisi", value=2, step=1, format="%d")
unit_cost_usd = st.number_input("Biaya Teknisi per Jam (USD)", value=16.6)
customer_type = st.radio("Jenis Customer", ["Private", "Government"])

if st.button("Hitung Total Biaya"):
    try:
        ec_unit_cost_usd = 132.8
        total_visits = (no_asd + no_pm) * no_chiller / 2
        total_hours = no_technician * total_visits * hours_per_day
        total_cost_usd = total_hours * unit_cost_usd + (no_ec * ec_unit_cost_usd)
        total_cost_idr = total_cost_usd * kurs

        unit_price_idr = 2560000 if customer_type.lower() == "private" else 1800000
        ec_price_idr = 8000000
        total_price_idr = (total_hours * unit_price_idr) + (no_ec * ec_price_idr)

        margin = ((total_price_idr - total_cost_idr) / total_cost_idr * 100) if total_cost_idr else 0

        st.success("Hasil Perhitungan:")
        st.write(f"**Total Visit**: {total_visits:.2f}")
        st.write(f"**Total Hours**: {total_hours:.2f}")
        st.write(f"**Total Cost (IDR)**: Rp {total_cost_idr:,.0f}")
        st.write(f"**Total Price (IDR)**: Rp {total_price_idr:,.0f}")
        st.write(f"**Margin**: {margin:.2f}%")

    except Exception as e:
        st.error(f"Terjadi kesalahan: {str(e)}")
