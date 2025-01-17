import streamlit as st

# Display Johnson Controls Logo
st.image(
    "https://upload.wikimedia.org/wikipedia/en/thumb/3/39/Johnson_Controls_logo.svg/1200px-Johnson_Controls_logo.svg.png",
    width=150,
    use_container_width=False,
    caption="Johnson Controls",
)

# Streamlit App Title
st.title("JCI Payment Days Calculator")

# Input Fields
st.header("Enter Payment Details")
down_payment = st.number_input("Down Payment Before Shipment (%)", min_value=0.0, max_value=100.0, step=1.0, value=30.0)
after_payment_days = st.number_input("Payment Days After Delivery (Days)", min_value=0, step=1, value=60)

# Calculate Button
if st.button("Calculate Average Payment Days"):
    try:
        # Calculate After Shipment Payment
        after_payment_percentage = 100 - down_payment

        # Calculate Weighted Average Payment Days
        weighted_days = (down_payment * 0 + after_payment_percentage * after_payment_days) / 100
        difference = weighted_days - 30  # Compare with JCI standard of 30 days

        # Determine if payment is standard or non-standard
        if weighted_days > 30:
            payment_type = "Non-Standard Payment"
            difference_message = f"{abs(difference):.2f} days more than the 30-day JCI standard."
        elif weighted_days < 30:
            payment_type = "Standard Payment"
            difference_message = f"{abs(difference):.2f} days less than the 30-day JCI standard."
        else:
            payment_type = "Standard Payment"
            difference_message = "exactly matches the 30-day JCI standard."

        # Determine Approvers
        if weighted_days <= 30:
            approvers = "No approver needed."
        elif 31 <= weighted_days <= 45:
            approvers = (
                "L50 Operations/Departmental: Peter Ferguson\n"
                "L60 Finance: Alessandro Vacca"
            )
        elif weighted_days > 45:
            approvers = (
                "L60 BU President: Anu Rathninde\n"
                "L70 Corporate Management: Marc Vandiepenbeeck\n"
                "L40 Credit Department: Mark Harcek/Laura McAleavey"
            )
        else:
            approvers = "Unknown - Invalid range."

        # Display Results
        st.success("Calculation Results:")
        st.write(f"**Average Payment Days:** {weighted_days:.2f} days")
        st.write(f"**Payment Type:** {payment_type}")
        st.write(f"**Comparison:** This is {difference_message}")
        st.write("**Approvers:**")
        st.text(approvers)
        st.info("Please align with Bu Morina. The data is based on DOA Approval Report Jan 2025.")

    except Exception as e:
        st.error("An error occurred during the calculation. Please check your inputs.")

# Footer
st.write("---")
st.write("Developed for JCI Payment Days Analysis.")
