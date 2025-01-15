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
    "house": "HOU",
    "housing": "HOU",
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
st.title("SFDC Opportunity Secret Name Generator")

# Input fields
lob = st.text_input("Enter LoB (i.e. Airside/Chiller/Control/Fire/Security/Digital Solution):").strip().lower()
owner = st.text_input("Enter 4 digits abbreviation of building owner (i.e., PTBA, BBRI, UNVR, TLKM, etc.):").strip()
building = st.text_input("Enter Building Type (i.e., Office, Mall, Data Center, etc.):").strip().lower()
area = st.text_input("Enter Project Area (i.e., Cimanggis):").strip()

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
        facility_code = FACILITY_CODES[building]
        reversed_owner = reverse_string(owner).title()
        reversed_facility = reverse_string(facility_code).title()
        reversed_area = reverse_string(area[:4].upper()).title()

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

        original_lob = LOB_CODES_REVERSE.get(lob_code, "Unknown LoB").title()
        original_facility = FACILITY_CODES_REVERSE.get(reverse_string(facility), "Unknown Facility").title()
        original_owner = reverse_string(owner).title()
        original_area = decipher_location(area).title()

        if "Unknown" in (original_lob, original_facility):
            st.error("Invalid Cipher Code. Please check your entry.")
        else:
            st.success("Deciphered Details:")
            st.write(f"LoB: {original_lob}")
            st.write(f"Owner: {original_owner}")
            st.write(f"Facility: {original_facility}")
            st.write(f"Area: {original_area}")
    except Exception as e:
        st.error("Invalid Cipher Code. Please check your entry.")
