import streamlit as st
import pandas as pd
from datetime import date
import io
import matplotlib.pyplot as plt
import json
import os

# File to store expenses persistently
EXPENSES_FILE = "expenses.json"

# Function to load expenses from file
def load_expenses():
    if os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, "r") as file:
            return json.load(file)
    return []

# Function to save expenses to file
def save_expenses(expenses):
    with open(EXPENSES_FILE, "w") as file:
        json.dump(expenses, file)

# Load existing expenses into session state
if "expenses" not in st.session_state:
    st.session_state.expenses = load_expenses()

# Set the page title with a subtitle
st.markdown("# Expense Calculator")
st.markdown("### Track your daily expenses with ease")

# Add a sidebar for navigation
st.sidebar.title("Navigation")
st.sidebar.info("Use this app to calculate and track your expenses.")
st.sidebar.image("https://via.placeholder.com/150", caption="Expense Tracker", use_container_width=True)

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

# File upload for importing expenses
st.sidebar.subheader("Import Expenses")
uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])
if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            imported_data = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            imported_data = pd.read_excel(uploaded_file)

        # Ensure required columns are present
        required_columns = {"Date", "Category", "Amount (Rp)", "Note"}
        if not required_columns.issubset(imported_data.columns):
            st.sidebar.error("The file must contain the following columns: Date, Category, Amount (Rp), Note")
        else:
            # Append imported data to session state and save
            for _, row in imported_data.iterrows():
                st.session_state.expenses.append({
                    "Date": row["Date"],
                    "Category": row["Category"],
                    "Amount (Rp)": row["Amount (Rp)"],
                    "Note": row["Note"],
                })
            save_expenses(st.session_state.expenses)
            st.sidebar.success("Expenses imported successfully!")
    except Exception as e:
        st.sidebar.error(f"Error processing the file: {e}")

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
            new_expense = {
                "Date": formatted_date,
                "Category": category,
                "Amount (Rp)": clean_amount,
                "Note": note,
            }
            st.session_state.expenses.append(new_expense)
            save_expenses(st.session_state.expenses)  # Save to file
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

    if not category_totals.empty:
        fig, ax = plt.subplots()
        ax.pie(category_totals, labels=category_totals.index, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig)
    else:
        st.info("No data available to generate a pie chart.")
else:
    st.info("No expenses recorded yet. Start by adding your first expense above!")
