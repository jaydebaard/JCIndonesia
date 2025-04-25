import streamlit as st
import pandas as pd
from io import BytesIO

# Set Page
st.set_page_config(page_title="Kalkulator Final Cost & Selling Price", layout="centered")
st.title("🧮 Kalkulator Final Cost, Selling Price, dan Margin")

# =================================
# 1. Biaya Teknisi
st.header("1. Biaya Teknisi")
technician_rate = st.number_input("Biaya per Jam Teknisi (Rp)", value=267040.0, step=1000.0, format="%.0f")
total_hours_technician = st.number_input("Total Jam Kerja Teknisi", value=147.0, step=0.5, format="%.1f")
total_cost_technician = technician_rate * total_hours_technician

# =================================
# 2. Subcontractor Works
st.header("2. Subcontractor Works")
default_rates = {"Helper": 97222.0, "Condenser Cleaning": 500000.0, "Other": 0.0}

subcon_data = []
num_subcons = st.number_input("Jumlah Kategori Subkontraktor", min_value=1, max_value=10, value=2, step=1)

for i in range(num_subcons):
    st.subheader(f"Subcontractor #{i+1}")
    category = st.selectbox(f"Kategori Subkon #{i+1}", ["Helper", "Condenser Cleaning", "Other"], key=f"category_{i}")
    default_rate = default_rates.get(category, 0.0)
    days = st.number_input(f"Hari Kerja - {category}", min_value=0.0, step=0.5, format="%.1f", key=f"days_{i}")
    hours_per_day = st.number_input(f"Jam/Hari - {category}", min_value=0.0, step=0.5, format="%.1f", key=f"hours_{i}")
    rate = st.number_input(f"Rate per Jam - {category} (Rp)", value=default_rate, step=1000.0, format="%.0f", key=f"rate_{i}")
    total_hours = days * hours_per_day
    total_cost = total_hours * rate

    subcon_data.append({
        "Kategori": category,
        "Hari": days,
        "Jam per Hari": hours_per_day,
        "Jam Total": total_hours,
        "Rate per Jam (Rp)": rate,
        "Total Cost (Rp)": total_cost
    })

subcon_total_cost = sum(item["Total Cost (Rp)"] for item in subcon_data)

# =================================
# 3. Other Costs
st.header("3. Other Costs (Manual Input)")
local_transport = st.number_input("Local Transport (Rp)", value=0.0, step=10000.0, format="%.0f")
hotels = st.number_input("Hotels (Rp)", value=0.0, step=10000.0, format="%.0f")
meals = st.number_input("Meals (Rp)", value=0.0, step=10000.0, format="%.0f")
outbound_freight = st.number_input("Outbound Freight (Rp)", value=0.0, step=10000.0, format="%.0f")
product_warranty = st.number_input("Product Warranty (Rp)", value=0.0, step=10000.0, format="%.0f")
if_applicable = st.number_input("If Applicable (Rp)", value=0.0, step=10000.0, format="%.0f")

other_manual_total = local_transport + hotels + meals + outbound_freight + product_warranty + if_applicable

# =================================
# 4. Cost dari Persentase
st.header("4. Biaya Tambahan Persentase (Auto)")
base_cost_for_percentage = total_cost_technician + subcon_total_cost + other_manual_total

road_reward = 0.01 * base_cost_for_percentage
incentive_provision = 0.02 * base_cost_for_percentage
ehs = 0.005 * base_cost_for_percentage
contingency = 0.04 * base_cost_for_percentage

# =================================
# 5. Final Cost Calculation
st.header("5. Final Cost Calculation")
final_cost_price = base_cost_for_percentage + road_reward + incentive_provision + ehs + contingency

st.write(f"Total Cost Technician: Rp {total_cost_technician:,.0f}")
st.write(f"Total Cost Subcontractors: Rp {subcon_total_cost:,.0f}")
st.write(f"Total Manual Other Costs: Rp {other_manual_total:,.0f}")
st.write(f"Road Reward (1%): Rp {road_reward:,.0f}")
st.write(f"Incentive Provision (2%): Rp {incentive_provision:,.0f}")
st.write(f"EHS (0.5%): Rp {ehs:,.0f}")
st.write(f"Cost Contingency (4%): Rp {contingency:,.0f}")

st.success(f"**Final Total Cost Price: Rp {final_cost_price:,.0f}**")

# =================================
# 6. Selling Price & Margin
st.header("6. Selling Price & Margin")
selling_price = st.number_input("Input Selling Price (Rp)", min_value=0.0, step=10000.0, format="%.0f")

final_margin = (selling_price - final_cost_price) / selling_price * 100 if selling_price != 0 else 0

if final_margin < 40:
    st.error(f"⚠️ Margin Akhir: {final_margin:.2f}% (Kurang dari 40%)")
else:
    st.success(f"✅ Margin Akhir: {final_margin:.2f}%")

# =================================
# 7. Perhitungan Tambahan Subcontractor Detail
st.header("7. Perhitungan Subcontractor Tambahan (Helper, Condenser Cleaning, Other)")
unit_rate_helper = 62500.0
unit_rate_condenser = 62500.0

st.subheader("Helper")
helper_days = st.number_input("Jumlah Hari Helper", min_value=0.0, step=0.5, format="%.1f")
helper_quantity = st.number_input("Jumlah Helper", min_value=0, step=1)
total_helper_cost = helper_days * 8 * helper_quantity * unit_rate_helper
st.write(f"Total Biaya Helper: Rp {total_helper_cost:,.0f}")

st.subheader("Condenser Cleaning")
condenser_days = st.number_input("Jumlah Hari Condenser Cleaning", min_value=0.0, step=0.5, format="%.1f")
condenser_quantity = st.number_input("Jumlah Condenser Cleaning", min_value=0, step=1)
total_condenser_cost = condenser_days * 8 * condenser_quantity * unit_rate_condenser
st.write(f"Total Biaya Condenser Cleaning: Rp {total_condenser_cost:,.0f}")

st.subheader("Other")
other_days = st.number_input("Jumlah Hari Other", min_value=0.0, step=0.5, format="%.1f")
other_quantity = st.number_input("Jumlah Other", min_value=0, step=1)
total_other_cost = other_days * 8 * other_quantity * unit_rate_helper
st.write(f"Total Biaya Other: Rp {total_other_cost:,.0f}")

# =================================
# Download Data Excel
st.header("8. Download Data")
data = {
    "Item": [
        "Total Hours Technician",
        "Technician Rate (Rp)",
        "Total Cost Technician (Rp)",
        "Total Cost Subcontractors (Rp)",
        "Other Manual Costs (Rp)",
        "Road Reward (Rp)",
        "Incentive Provision (Rp)",
        "EHS (Rp)",
        "Contingency (Rp)",
        "Final Cost Price (Rp)",
        "Selling Price (Rp)",
        "Margin Akhir (%)",
        "Total Biaya Helper (Rp)",
        "Total Biaya Condenser Cleaning (Rp)",
        "Total Biaya Other (Rp)"
    ],
    "Value": [
        total_hours_technician,
        technician_rate,
        total_cost_technician,
        subcon_total_cost,
        other_manual_total,
        road_reward,
        incentive_provision,
        ehs,
        contingency,
        final_cost_price,
        selling_price,
        final_margin,
        total_helper_cost,
        total_condenser_cost,
        total_other_cost
    ]
}

df_summary = pd.DataFrame(data)


def to_excel_file(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Summary')
    return output.getvalue()

st.download_button(
    label="📥 Download Summary ke Excel",
    data=to_excel_file(df_summary),
    file_name="kalkulator_final_cost_summary.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
) 
