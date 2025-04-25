# ===============================================
# Total Final Cost & Margin Revisi
total_final_cost = total_cost_technician + subcon_total_cost + total_other_cost

st.header("🧾 Ringkasan Final Cost & Margin Revisi")
st.write(f"💰 **Total Final Cost: Rp {total_final_cost:,.0f}**")

margin_final = (offered_price_idr - total_final_cost) / offered_price_idr * 100 if offered_price_idr != 0 else 0

if margin_final < 40:
    st.error(f"⚠️ Margin (Revisi, berdasarkan total cost): {margin_final:.2f}% (Kurang dari 40%)")
else:
    st.success(f"✅ Margin (Revisi, berdasarkan total cost): {margin_final:.2f}%")
