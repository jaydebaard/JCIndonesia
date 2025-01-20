import streamlit as st
import pandas as pd
from datetime import date
import io
import matplotlib.pyplot as plt
import json
import os
from PIL import Image
import pytesseract

# File to store expenses persistently
EXPENSES_FILE = "expenses.json"
IMAGES_FOLDER = "receipt_images"

# Ensure the receipt images folder exists
os.makedirs(IMAGES_FOLDER, exist_ok=True)

# Function to check if Tesseract is installed
def is_tesseract_installed():
    from shutil import which
    return which("tesseract") is not None

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

# Function to extract amount from receipt image
def extract_amount_from_image(image):
    if not is_tesseract_installed():
        st.error("Tesseract is not installed or not in your PATH. Please install Tesseract to use this feature.")
        return None

    try:
        text = pytesseract.image_to_string(Image.open(image))
        # Use regex to find patterns of currency in the text
        import re
        matches = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d{2})?\b', text)
        if matches:
            # Convert the first match to a numeric value
            return float(matches[0].replace(",", ""))
    except Exception as e:
        st.error(f"Error extracting amount: {e}")
    return None

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

# Create a form for expense input
with st.form("expense_form"):
    st.subheader("Add New Expense")

    transaction_date = st.date_input("📅 Date of Transaction", value=date.today())

    category = st.selectbox("📂 Category", categories)

    amount = st.text_input("💵 Amount (in Rupiah, e.g., Rp. 5,000,000)")

    note = ""
    if category == "Others (with note)":
        note = st.text_input("📝 Note (optional)")

    receipt_image = st.camera_input("📸 Take a picture of the receipt (optional)")

    extracted_amount = None
    if receipt_image is not None:
        extracted_amount = extract_amount_from_image(receipt_image)
        if extracted_amount:
            st.success(f"Extracted Amount: Rp. {extracted_amount:,.0f}")

    submitted = st.form_submit_button("➕ Add Expense")

    if submitted:
        # Format the date to day, month, year
        formatted_date = transaction_date.strftime("%d-%m-%Y")

        # Clean and convert the amount to a numeric value
        try:
            clean_amount = float(amount.replace("Rp.", "").replace(",", "")) if amount else extracted_amount
        except ValueError:
            st.error("Please enter a valid amount in the format 'Rp. 5,000,000'")
            clean_amount = None

        if clean_amount is not None:
            # Save the receipt image if provided
            receipt_path = None
            if receipt_image is not None:
                receipt_path = os.path.join(IMAGES_FOLDER, f"receipt_{len(st.session_state.expenses) + 1}.png")
                with open(receipt_path, "wb") as f:
                    f.write(receipt_image.getbuffer())

            # Append the new expense to the session state
            new_expense = {
                "Date": formatted_date,
                "Category": category,
                "Amount (Rp)": clean_amount,
                "Note": note,
                "Receipt Path": receipt_path,
            }
            st.session_state.expenses.append(new_expense)
            save_expenses(st.session_state.expenses)  # Save to file
            st.success("✅ Expense added successfully!")

# Display the list of expenses
if st.session_state.expenses:
    st.subheader("Expense Summary")

    # Convert to DataFrame for better presentation
    df = pd.DataFrame(st.session_state.expenses)
    if "Receipt Path" in df.columns:
        st.dataframe(df.drop(columns=["Receipt Path"]), use_container_width=True)
    else:
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

    # Display attached receipt images
    st.subheader("Receipt Images")
    for expense in st.session_state.expenses:
        if "Receipt Path" in expense and expense["Receipt Path"]:
            st.image(expense["Receipt Path"], caption=f"Receipt for {expense['Category']} on {expense['Date']}", use_container_width=True)
else:
    st.info("No expenses recorded yet. Start by adding your first expense above!")
