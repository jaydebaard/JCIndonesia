import streamlit as st

# Data mappings based on the provided rules
LOB_CODES = {
    "chiller": "Alpha",
    "airside": "Beta",
    "control (bms)": "Gamma",
    "fire": "Delta",
    "security": "Epsilon",
    "digital solution": "Zeta",
}

FACILITY_CODES = {
    "public facilities": "PUB",
    "university": "UNI",
    "transport": "TRP",
    "hotel": "HOT",
    "commercial": "COM",
    "mall": "MAL",
    "office": "OFC",
    "industrial": "IND",
    "data center": "DCT",
    "residential": "RES",
    "House": "HOU",
    "Housing": "HOU",
    "hospital": "HOS",
    "warehouse": "WRH",
    "retail": "RTL",
    "plant": "EPL",
    "government office": "GOV",
    "government": "GOV",
    "sports": "SPT",
    "sport": "SPT",
    "stadium": "STA",
    "education center": "EDU",
    "entertainment center": "ENT",
    "factory": "FCT",
    "airport": "APT",
    "train station": "STN",
    "train": "STN",
    "logistics hub": "LGH",
}

LOB_CODES_REVERSE = {v: k.capitalize() for k, v in LOB_CODES.items()}
FACILITY_CODES_REVERSE = {v: k.capitalize() for k, v in FACILITY_CODES.items()}


# Function to reverse a string
def reverse_string(s):
    return s[::-1]


# Function to decipher the location
def decipher_location(location):
    return reverse_string(location).capitalize()


# Streamlit app title
st.title("SFDC Opportunity Name Generator")

# Input fields
lob = st.text_input("Enter LoB (Airside/Chiller/Control/Fire/Security/Digital Solution):").strip().lower()
owner = st.text_input("Enter End Customer Name Abbreviation (e.g., PTBS, BBRI, etc.):").strip()
building = st.text_input("Enter Building Type (e.g., Office, Mall, Data Center, etc.):").strip().lower()
area = st.text_input("Enter Project Area (e.g., Cimanggis):").strip()

# Button to generate opportunity name
if st.button("Generate Opportunity Name"):
    error = False

    # Validate inputs
    if lob not in LOB_CODES:
        st.error("Invalid LoB. Try with the correct word.")
        error = True
    if not owner:
        st.error("Invalid End Customer Name. Please provide a valid abbreviation.")
        error = True
    if building not in FACILITY_CODES:
        st.error("Invalid Building Type. Try with the correct word.")
        error = True
    if not area:
        st.error("Invalid Project Area. Please provide a valid area.")
        error = True

    if not error:
        lob_code = LOB_CODES[lob]
        facility_code = FACILITY_CODES[building
