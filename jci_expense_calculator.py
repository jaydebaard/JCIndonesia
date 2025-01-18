import streamlit as st
import pandas as pd
from datetime import date
import io
import matplotlib.pyplot as plt

# Set the page title with a subtitle
st.markdown("# Expense Calculator")
st.markdown("### Track your daily expenses with ease")

# Add a sidebar for navigation
st.sidebar.title("Navigation")
st.sidebar.info("Use this app to calculate and track your expenses.")
st.sidebar.image("https://via.placeholder.com/150", caption="Expense Tracker", use_column_width=True)

# Categories for expense inputs
categories = [
    "Fuel",
    "Meal with Customer",
    "Individual Meal",
    "Taxi",
    "Parking",
    "Tolls",
    "Others (with note)",
]

# Initialize session state to store expenses
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# Create a form for expense input
with st.form("expense_form"):
    st.subheader("Add New Expense")

    transaction_date = st.date_input("📅 Date of Transaction", value=date.today())

    category = st.selectbox("📂 Category", categories)

    amount = st.text_input("💵 Amount (in Rupiah, e.g., Rp. 5,000,000)")

    note = ""
    if category == "Others (with note)":
        note = st.text_input("📝 Note (optional)")

    submitted = st.form_submit_button("➕ Add Expense")

    if submitted:
        # Format the date to day, month, year
        formatted_date = transaction_date.strftime("%d-%m-%Y")

        # Clean and convert the amount to a numeric value
        try:
            clean_amount = float(amount.replace("Rp.", "").replace(",", ""))
        except ValueError:
            st.error("Please enter a valid amount in the format 'Rp. 5,000,000'")
            clean_amount = None

        if clean_amount is not None:
            # Append the new expense to the session state
            st.session_state.expenses.append({
                "Date": formatted_date,
                "Category": category,
                "Amount (Rp)": clean_amount,
                "Note": note,
            })
            st.success("✅ Expense added successfully!")

# Display the list of expenses
if st.session_state.expenses:
    st.subheader("Expense Summary")
    
    # Convert to DataFrame for better presentation
    df = pd.DataFrame(st.session_state.expenses)
    st.dataframe(df, use_container_width=True)

    # Display the total expenses
    total_expenses = sum(entry["Amount (Rp)"] for entry in st.session_state.expenses)
    st.write(f"### 💰 Total Expenses: Rp. {total_expenses:,.0f}")

    # Add separator
    st.markdown("---")

    # Download option for the expenses as CSV
    csv = pd.DataFrame(st.session_state.expenses).to_csv(index=False)
    st.download_button(
        label="⬇️ Download Expenses as CSV",
        data=csv,
        file_name="expenses.csv",
        mime="text/csv",
    )

    # Download option for the expenses as Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        pd.DataFrame(st.session_state.expenses).to_excel(writer, index=False, sheet_name="Expenses")
    st.download_button(
        label="⬇️ Download Expenses as Excel",
        data=output.getvalue(),
        file_name="expenses.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    # Create a pie chart of the expenses
    st.subheader("Expense Distribution")
    category_totals = df.groupby("Category")["Amount (Rp)"].sum()
    fig, ax = plt.subplots()
    ax.pie(category_totals, labels=category_totals.index, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig)
else:
    st.info("No expenses recorded yet. Start by adding your first expense above!")
