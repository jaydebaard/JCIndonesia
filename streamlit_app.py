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
    "shopping mall": "MAL",
    "office": "OFC",
    "industrial": "IND",
    "data center": "DCT",
    "residential": "RES",
    "hospital": "HOS",
    "warehouse": "WRH",
    "retail": "RTL",
    "energy plant": "EPL",
    "government office": "GOV",
    "sports facility": "SPT",
    "education center": "EDU",
    "entertainment center": "ENT",
    "factory": "FCT",
    "airport": "APT",
    "train station": "STN",
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


st.title("SFDC Opportunity Name Generator")
st.image("/Users/antonsanjaya/Downloads/johnson-controls.jpg", width=200)

# Input fields
lob = st.text_input("Enter LoB (Airside/Chiller/Control/Fire/Security/Digital Solution):").strip().lower()
owner = st.text_input("Enter End Customer Name Abbreviation (e.g., PTBS, BBRI, etc.):").strip()
building = st.text_input("Enter Building Type (e.g., Office, Mall, Data Center, etc.):").strip().lower()
area = st.text_input("Enter Project Area (e.g., Cimanggis):").strip()

# Button to generate opportunity name
if st.button("Generate Opportunity Name"):
    lob_code = LOB_CODES.get(lob, "Unknown LoB")
    facility_code = FACILITY_CODES.get(building, "Unknown Facility")

    reversed_owner = reverse_string(owner)
    reversed_facility = reverse_string(facility_code)
    reversed_area = reverse_string(area[:4].upper())

    if "Unknown" in (lob_code, facility_code):
        st.error("Invalid input. Please check your entries.")
    else:
        opportunity_name = f"#{lob_code}#{reversed_owner}-{reversed_facility}#{reversed_area}"
        st.success("Generated Opportunity Name:")
        st.code(opportunity_name)
        st.session_state["last_generated_code"] = opportunity_name

# Button to copy the last generated code
if "last_generated_code" in st.session_state and st.button("Copy to Clipboard"):
    st.experimental_set_query_params(opportunity_name=st.session_state["last_generated_code"])
    st.success("Generated code copied to clipboard!")

# Input to decipher code
cipher = st.text_input("Enter Cipher Code to Decipher:")

if st.button("Decipher Code"):
    try:
        lob_code, owner_facility, area = cipher.strip("#").split("#")
        owner, facility = owner_facility.split("-")

        original_lob = LOB_CODES_REVERSE.get(lob_code, "Unknown LoB")
        original_facility = FACILITY_CODES_REVERSE.get(reverse_string(facility), "Unknown Facility")
        original_owner = reverse_string(owner)
        original_area = decipher_location(area)

        st.success("Deciphered Details:")
        st.write(f"LoB: {original_lob}")
        st.write(f"Owner: {original_owner}")
        st.write(f"Facility: {original_facility}")
        st.write(f"Area: {original_area}")
    except Exception as e:
        st.error("Invalid Cipher Code. Please check your entry.")