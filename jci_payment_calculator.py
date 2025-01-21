import streamlit as st
import json
import os

# File to store visitor count
VISITOR_FILE = "visitor_count.json"

# Function to load visitor count
def load_visitor_count():
    if os.path.exists(VISITOR_FILE):
        with open(VISITOR_FILE, "r") as file:
            data = json.load(file)
            return data.get("count", 0)
    return 0

# Function to save visitor count
def save_visitor_count(count):
    with open(VISITOR_FILE, "w") as file:
        json.dump({"count": count}, file)

# Track unique visitors in session state
if "is_visited" not in st.session_state:
    st.session_state.is_visited = False

# Load visitor count
visitor_count = load_visitor_count()

# Increment count for a new visitor
if not st.session_state.is_visited:
    visitor_count += 1
    st.session_state.is_visited = True
    save_visitor_count(visitor_count)

# Display visitor count
st.sidebar.title("Visitor Analytics")
st.sidebar.write(f"Total Visitors: {visitor_count}")

# Main app logic
st.title("📊 PT JCI SoV DoA Calculator")
st.markdown("---")
st.subheader("Enter Payment Details 📝")

# Input Fields
col1, col2 = st.columns(2)
with col1:
    down_payment = st.number_input(
        "🔽 Down Payment Before Shipment (%)",
        min_value=0,
        max_value=100,
        step=1,
        value=0,
        format="%d",
    )
with col2:
    after_payment_days = st.number_input(
        "📅 Payment After Delivery (Days)", min_value=0, step=1, value=0
    )

# Calculate Button
if st.button("🚀 Calculate Average Payment Days"):
    try:
        after_payment_percentage = 100 - down_payment
        weighted_days = (down_payment * 0 + after_payment_percentage * after_payment_days) / 100
        difference = weighted_days - 30
        payment_type = "Standard Payment ✅" if weighted_days <= 30 else "Non-Standard Payment ⚠️"
        difference_message = f"{abs(difference):.2f} days {'less' if difference < 0 else 'more'} than the 30-day JCI standard."
        st.markdown("### 🏁 Calculation Results")
        st.success(f"**Average Payment Days:** {weighted_days:.2f} days")
        st.write(f"**Payment Category:** {payment_type}")
        st.write(f"**Remarks:** This is {difference_message}")
    except Exception as e:
        st.error("❌ An error occurred during the calculation. Please check your inputs.")
