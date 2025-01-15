import difflib
import streamlit as st

# Data mappings based on the provided rules
LOB_CODES = {
    "chiller": "Alpha",
    "airside": "Beta",
    "control": "Gamma",
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
FACILITY_CODES_REVERSE = {v: k.lower() for k, v in FACILITY_CODES.items()}


# Function to reverse a string
def reverse_string(s):
    return s[::-1]


# Function to decipher the location
def decipher_location(location):
    return reverse_string(location).capitalize()


# Function to find the closest match for a string
def get_closest_match(input_str, valid_options):
    matches = difflib.get_close_matches(input_str, valid_options, n=1, cutoff=0.6)
    return matches[0] if matches else None


# Streamlit app title
st.title("SFDC Opportunity Secret Name Generator")

# Input fields
lob = st.text_input(
    "Enter LoB (e.g., Airside, Chiller, Control, Fire, Security, Digital Solution):",
    placeholder="Enter LoB (e.g., Chiller)",
).strip().lower()

owner = st.text_input(
    "Enter 4 abbreviation letters of the building owner name (e.g., CPTR, SMRC, PTBA, BBRI):",
    placeholder="Must be exactly 4 letters",
    max_chars=4,  # Limit input to 4 characters
).strip()

building = st.text_input(
    "Enter Building Type (e.g., Office, Mall, Data Center):",
    placeholder="Enter building type (e.g., Office)",
).strip().lower()
area = st.text_input(
    "Enter Project Area (e.g., Slipi, Cimanggis):",
    placeholder="Enter project area (e.g., Slipi)",
).strip()

# Real-time validation for owner field
if owner and len(owner) != 4:
    st.error("Owner abbreviation must be exactly 4 characters.")

# Button to generate opportunity name
if st.button("Generate Code"):
    if not lob or not owner or len(owner) != 4 or not building or not area:
        st.error("All fields are required, and the owner abbreviation must be exactly 4 characters.")
    elif lob not in LOB_CODES:
        st.error("Invalid LoB. Valid options are:")
        st.write(", ".join(LOB_CODES.keys()))
    else:
        closest_building = get_closest_match(building, FACILITY_CODES.keys())
        if not closest_building:
            st.error("Invalid Building Type. Valid options are:")
            st.write(", ".join(FACILITY_CODES.keys()))
        else:
            lob_code = LOB_CODES[lob]
            facility_code = FACILITY_CODES[closest_building]
            reversed_owner = reverse_string(owner).title()
            reversed_facility = reverse_string(facility_code).title()
            reversed_area = reverse_string(area[:4].upper()).title()

            opportunity_name = f"#{lob_code}#{reversed_owner}-{reversed_facility}#{reversed_area}"
            st.success("Generated Opportunity Name:")
            st.code(opportunity_name)
            st.info("Copy this code to your SFDC Opportunity Name field.")  # Notification added here

# Input to decipher code
cipher = st.text_input(
    "Enter Cipher Code to Decipher:",
    placeholder="Enter generated code (e.g., #Alpha#Sbtp-Efo#Cima)",
)

if st.button("Decipher Code"):
    try:
        lob_code, owner_facility, area = cipher.strip("#").split("#")
        owner, facility = owner_facility.split("-")

        original_lob = LOB_CODES_REVERSE.get(lob_code, "Unknown LoB").title()
        original_facility_key = reverse_string(facility).lower()
        original_facility = next(
            (k.capitalize() for k, v in FACILITY_CODES.items() if v.lower() == original_facility_key),
            "Unknown Facility",
        )
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
