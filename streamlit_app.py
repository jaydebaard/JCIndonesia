import difflib  # For fuzzy matching
import streamlit as st

# ... (existing LOB_CODES and FACILITY_CODES dictionaries)

def get_closest_match(input_str, options):
    """Find the closest match for a string in a list of options."""
    matches = difflib.get_close_matches(input_str, options, n=1, cutoff=0.6)
    return matches[0] if matches else None

# Streamlit app title
st.title("SFDC Opportunity Secret Name Generator")

# Input fields
lob = st.text_input(
    "Enter LoB (e.g., Airside, Chiller, Control, Fire, Security, Digital Solution):",
    placeholder="Enter LoB (e.g., Chiller)",
).strip().lower()
owner = st.text_input(
    "Enter a 4-character abbreviation of the building owner (e.g., PTBA, BBRI):",
    placeholder="Enter owner abbreviation (e.g., PTBA)",
).strip()
building = st.text_input(
    "Enter Building Type (e.g., Office, Mall, Data Center):",
    placeholder="Enter building type (e.g., Office)",
).strip().lower()
area = st.text_input(
    "Enter Project Area (e.g., Cimanggis):",
    placeholder="Enter project area (e.g., Cimanggis)",
).strip()

# Dynamically generate opportunity name when all inputs are valid
if lob and owner and len(owner) == 4 and building and area:
    if lob not in LOB_CODES:
        st.error("Invalid LoB. Please try again with a correct option.")
    else:
        closest_facility = get_closest_match(building, FACILITY_CODES.keys())
        if not closest_facility:
            st.error("Invalid Building Type. Valid options are:")
            st.write(", ".join(FACILITY_CODES.keys()))
        else:
            lob_code = LOB_CODES[lob]
            facility_code = FACILITY_CODES[closest_facility]
            reversed_owner = reverse_string(owner).title()
            reversed_facility = reverse_string(facility_code).title()
            reversed_area = reverse_string(area[:4].upper()).title()

            opportunity_name = f"#{lob_code}#{reversed_owner}-{reversed_facility}#{reversed_area}"
            st.success("Generated Opportunity Name:")
            st.code(opportunity_name)
            st.session_state["last_generated_code"] = opportunity_name
else:
    st.warning("Please fill in all fields with valid inputs.")
