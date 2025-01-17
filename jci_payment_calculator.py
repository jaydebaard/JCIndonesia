import streamlit as st

# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #f4f4f4;
    }
    .stApp {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    h1, h2 {
        color: #007BFF;
        text-align: center;
    }
    .stButton button {
        background-color: #007BFF;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stButton button:hover {
        background-color: #0056b3;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Streamlit App Title
st.title("📊 PT JCI SoV DoA Calculator")

# Decorative Section Divider
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
        # Calculate After Shipment Payment
        after_payment_percentage = 100 - down_payment

        # Calculate Weighted Average Payment Days
        weighted_days = (down_payment * 0 + after_payment_percentage * after_payment_days) / 100
        difference = weighted_days - 30  # Compare with JCI standard of 30 days

        # Determine if payment is standard or non-standard
        if weighted_days > 30:
            payment_type = "Non-Standard Payment ⚠️"
            difference_message = f"{abs(difference):.2f} days more than the 30-day JCI standard."
        elif weighted_days < 30:
            payment_type = "Standard Payment ✅"
            difference_message = f"{abs(difference):.2f} days less than the 30-day JCI standard."
        else:
            payment_type = "Standard Payment ✅"
            difference_message = "exactly matches the 30-day JCI standard."

        # Determine Approvers
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
        st.info("📌 Please align with Morina Normalita (finance controller-L20 Finance). The data is based on DOA Approval Report Jan 2025.")

    except Exception as e:
        st.error("❌ An error occurred during the calculation. Please check your inputs.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center;'>
        Developed for PT JCI SoV DoA. <br>
        🚀 Powered by Streamlit.
    </div>
    """,
    unsafe_allow_html=True,
)
