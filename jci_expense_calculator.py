import streamlit as st
import pandas as pd
from datetime import date
import io

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

    amount = st.number_input(
        "💵 Amount (in Rupiah)", min_value=0.0, step=1000.0, format="%.2f"
    )

    note = ""
    if category == "Others (with note)":
        note = st.text_input("📝 Note (optional)")

    submitted = st.form_submit_button("➕ Add Expense")

    if submitted:
        # Format the date to day, month, year
        formatted_date = transaction_date.strftime("%d-%m-%Y")

        # Append the new expense to the session state
        st.session_state.expenses.append({
            "Date": formatted_date,
            "Category": category,
            "Amount (Rp)": amount,
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
    total_expenses = df["Amount (Rp)"].sum()
    st.write(f"### 💰 Total Expenses: Rp {total_expenses:,.2f}")

    # Add separator
    st.markdown("---")

    # Download option for the expenses as CSV
    csv = df.to_csv(index=False)
    st.download_button(
        label="⬇️ Download Expenses as CSV",
        data=csv,
        file_name="expenses.csv",
        mime="text/csv",
    )

    # Download option for the expenses as Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Expenses")
        writer.save()
    st.download_button(
        label="⬇️ Download Expenses as Excel",
        data=output.getvalue(),
        file_name="expenses.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
else:
    st.info("No expenses recorded yet. Start by adding your first expense above!")
