import streamlit as st
import pandas as pd
from io import BytesIO

# Title
st.set_page_config(page_title="Kalkulator Biaya PM, ASD, EC, dan Subkontraktor (Rupiah)", layout="centered")
st.title("🧮 Kalkulator Biaya PM, ASD, EC, dan Subkontraktor (Rupiah)")

# Section: Cost Setting
st.header("1. Biaya Teknisi")
tech_rate = st.number_input("Biaya per Jam Teknisi (Rp)", value=267040.0, step=1000.0, format="%.0f")

# Section: Estimasi Jam Kerja Teknisi
st.header("2. Estimasi Jam Kerja Teknisi")
total_hours = st.number_input("Total Jam Kerja Teknisi", value=147.0, step=0.5, format="%.1f")
total_cost_technician = total_hours * tech_rate

# Section: Harga Penawaran
st.header("3. Harga yang Ditawarkan")
offered_price_idr = st.number_input("Harga yang Ditawarkan (Rp)", min_value=0.0, step=1000.0, format="%.0f")
margin = (offered_price_idr - total_cost_technician) / offered_price_idr * 100 if offered_price_idr != 0 else 0

# Display Summary Harga vs Cost Teknisi
st.subheader("💵 Price vs Cost (Teknisi)")
st.write(f"Harga Ditawarkan: **Rp {offered_price_idr:,.0f}**")
st.write(f"Total Cost Teknisi: **Rp {total_cost_technician:,.0f}**")
st.caption(f"Perhitungan: {total_hours:,.1f} jam x Rp {tech_rate:,.0f} per jam = Rp {total_cost_technician:,.0f}")
if margin < 40:
    st.error(f"⚠️ Margin: {margin:.2f}% (Kurang dari 40%)")
else:
    st.success(f"✅ Margin: {margin:.2f}%")

# Section: Subcontractor Work
st.header("4. Subcontractor Works")

# Subcontractor categories with default rates
default_rates = {
    "Helper": 97222.0,
    "Condenser Cleaning": 500000.0,
    "Other": 0.0
}

subcon_data = []
num_subcons = st.number_input("Berapa banyak jenis pekerjaan Subkontraktor?", min_value=1, max_value=10, value=2, step=1)

for i in range(num_subcons):
    st.markdown(f"### Subcontractor #{i+1}")
    category = st.selectbox(f"Pilih Kategori Pekerjaan Subkontraktor #{i+1}", ["Helper", "Condenser Cleaning", "Other"], key=f"category_{i}")

    default_rate = default_rates.get(category, 0.0)

    days = st.number_input(f"Jumlah Hari - {category}", min_value=0.0, step=0.5, key=f"days_{i}", format="%.1f")
    hours_per_day = st.number_input(f"Jam/Hari - {category}", min_value=0.0, step=0.5, key=f"hours_{i}", format="%.1f")
    rate = st.number_input(f"Biaya per Jam - {category} (Rp)", min_value=0.0, value=default_rate, step=1000.0, key=f"rate_{i}", format="%.0f")

    total_hours_subcon = days * hours_per_day
    total_cost_subcon = total_hours_subcon * rate

    st.success(f"Total Cost {category}: Rp {total_cost_subcon:,.0f}")
    st.caption(f"{total_hours_subcon:,.1f} jam x Rp {rate:,.0f} = Rp {total_cost_subcon:,.0f}")

    subcon_data.append({
        "Kategori": category,
        "Hari": days,
        "Jam per Hari": hours_per_day,
        "Jam Total": total_hours_subcon,
        "Rate per Jam (Rp)": rate,
        "Total Cost (Rp)": total_cost_subcon
    })

# Total Cost Semua Subkontraktor
total_cost_all_subcon = sum(item["Total Cost (Rp)"] for item in subcon_data)
st.subheader("🧾 Total Biaya Semua Subkontraktor")
st.write(f"**Rp {total_cost_all_subcon:,.0f}**")

# Section: Download to Excel
summary_data = {
    "Item": [
        "Total Jam Teknisi",
        "Biaya per Jam Teknisi (Rp)",
        "Total Cost Teknisi (Rp)",
        "Harga Ditawarkan (Rp)",
        "Margin (%)",
        "Total Cost Subkontraktor (Rp)"
    ],
    "Value": [
        total_hours,
        tech_rate,
        total_cost_technician,
        offered_price_idr,
        margin,
        total_cost_all_subcon
    ]
}
df_summary = pd.DataFrame(summary_data)

df_subcon = pd.DataFrame(subcon_data)

def to_excel_file(df1, df2):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df1.to_excel(writer, index=False, sheet_name='Summary')
        df2.to_excel(writer, index=False, sheet_name='Subcontractors')
    return output.getvalue()

st.download_button(
    label="📥 Download Excel (Summary + Subcontractor)",
    data=to_excel_file(df_summary, df_subcon),
    file_name="biaya_subkontraktor_dan_teknisi.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
