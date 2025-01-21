import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

# File to store visitor logs
VISITOR_LOG_FILE = "visitor_logs.json"

# Load visitor logs
def load_visitor_logs():
    if os.path.exists(VISITOR_LOG_FILE):
        with open(VISITOR_LOG_FILE, "r") as file:
            return json.load(file)
    return []

# Save visitor logs
def save_visitor_logs(logs):
    with open(VISITOR_LOG_FILE, "w") as file:
        json.dump(logs, file)

# Log a new visitor
def log_visitor():
    visitor_logs = load_visitor_logs()
    today = datetime.now().strftime("%Y-%m-%d")
    visitor_logs.append({"date": today, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    save_visitor_logs(visitor_logs)

# Track unique visitors per session
if "is_visited" not in st.session_state:
    st.session_state.is_visited = False

# Log visitor if not already logged in this session
if not st.session_state.is_visited:
    st.session_state.is_visited = True
    log_visitor()

# Load logs for analytics
visitor_logs = load_visitor_logs()
visitor_df = pd.DataFrame(visitor_logs)

# Sidebar Analytics
st.sidebar.title("Visitor Analytics")

# Display total visitors
total_visitors = len(visitor_logs)
st.sidebar.metric("Total Visitors", total_visitors)

# Group visitors by date
if not visitor_df.empty:
    visitor_by_date = visitor_df.groupby("date").size().reset_index(name="count")
    st.sidebar.write("### Daily Visitors")
    st.sidebar.bar_chart(visitor_by_date.set_index("date"))

    # Show detailed visitor logs
    if st.sidebar.button("Show Visitor Logs"):
        st.write("### Visitor Logs")
        st.dataframe(visitor_df)
else:
    st.sidebar.write("No visitors yet.")

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

        # Determine payment type
        if weighted_days > 30:
            payment_type = "Non-Standard Payment ⚠️"
            difference_message = f"{abs(difference):.2f} days more than the 30-day JCI standard."
        elif weighted_days < 30:
            payment_type = "Standard Payment ✅"
            difference_message = f"{abs(difference):.2f} days less than the 30-day JCI standard."
        else:
            payment_type = "Standard Payment ✅"
            difference_message = "exactly matches the 30-day JCI standard."

        # Determine approvers
        if weighted_days <= 30:
            approvers = "No approver needed."
        elif 31 <= weighted_days <= 45:
            approvers = (
                "🔹 L50 Operations/Departmental: Peter Ferguson\n"
                "🔹 L60 Finance: Alessandro Vacca"
            )
        elif weighted_days > 45:
            approvers = (
                "🔸 L60 BU President: Anu Rathninde\n"
                "🔸 L70 Corporate Management: Marc Vandiepenbeeck\n"
                "🔸 L40 Credit Department: Mark Harcek"
            )
        else:
            approvers = "Unknown - Invalid range."

        # Display Results
        st.markdown("### 🏁 Calculation Results")
        st.success(f"**Average Payment Days:** {weighted_days:.2f} days")
        st.write(f"**Payment Category:** {payment_type}")
        st.write(f"**Remarks:** This is {difference_message}")
        st.write("**Approvers:**")
        st.text(approvers)
        st.info(
            "📌 Please align with Morina Normalita (finance controller-L20 Finance). "
            "The data is based on DOA Approval Report Jan 2025."
        )
    except Exception as e:
        st.error("❌ An error occurred during the calculation. Please check your inputs.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #222222;'>
        Developed for PT JCI SoV DoA. <br>
        🚀 Powered by Streamlit.
    </div>
    """,
    unsafe_allow_html=True,
)
