import difflib
import streamlit as st

# Data mappings
LOB_CODES = {
    "chiller": "Chiller",
    "airside": "Airside",
    "control": "Control",
    "fire": "Fire",
    "security": "Security",
    "digital solution": "Digital",
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

# Utility functions
def reverse_string(s):
    return s[::-1]

def decipher_location(location):
    return reverse_string(location).capitalize()

def get_closest_match(input_str, valid_options):
    matches = difflib.get_close_matches(input_str, valid_options, n=1, cutoff=0.6)
    return matches[0] if matches else None

# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #f8f9fa;
    }
    .stApp {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton button {
        background-color: #007BFF;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stButton button:hover {
        background-color: #0056b3;
    }
    h1, h2 {
        text-align: center;
        color: #007BFF;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Streamlit app title
st.title("🔐 SFDC Opportunity Secret Code Generator")

# Input Fields with Icons
st.subheader("✨ Input Details")
lob = st.text_input(
    "🔽 Enter LoB (e.g., Chiller, Airside, Fire):",
    placeholder="Enter LoB (e.g., Chiller)",
).strip().lower()

owner = st.text_input(
    "🏢 Enter Building Owner (4 letters):",
    placeholder="e.g., CPTR, SMRC",
    max_chars=4,
).strip()

building = st.text_input(
    "🏬 Enter Building Type (e.g., Office, Mall):",
    placeholder="Enter building type (e.g., Office)",
).strip().lower()

area = st.text_input(
    "📍 Enter Project Area (e.g., Slipi, Cimanggis):",
    placeholder="Enter project area (e.g., Slipi)",
).strip()

# Real-time validation
if owner and len(owner) != 4:
    st.error("❗ Owner abbreviation must be exactly 4 characters.")

# Generate Opportunity Code
if st.button("🚀 Generate Code"):
    if not lob or not owner or len(owner) != 4 or not building or not area:
        st.error("⚠️ All fields are required, and the owner abbreviation must be exactly 4 characters.")
    elif lob not in LOB_CODES:
        st.error("❌ Invalid LoB. Valid options are:")
        st.write(", ".join(LOB_CODES.keys()))
    else:
        closest_building = get_closest_match(building, FACILITY_CODES.keys())
        if not closest_building:
            st.error("❌ Invalid Building Type. Valid options are:")
            st.write(", ".join(FACILITY_CODES.keys()))
        else:
            lob_code = LOB_CODES[lob]
            facility_code = FACILITY_CODES[closest_building]
            reversed_owner = reverse_string(owner).title()
            reversed_facility = reverse_string(facility_code).title()
            reversed_area = reverse_string(area[:4].upper()).title()

            opportunity_name = f"#{lob_code}#{reversed_owner}-{reversed_facility}#{reversed_area}"
            st.success("🎉 Generated Opportunity Name:")
            st.code(opportunity_name)
            st.info("✅ Copy this code to your SFDC Opportunity Name field.")

            # Display Account Name
            account_name = "PT Johnson Controls Indonesia"
            st.success("🏢 Account Name:")
            st.code(account_name)
            st.info("✅ Copy this to the account name/facility owner in SFDC.")

# Decipher Opportunity Code
st.subheader("🔎 Decipher Opportunity Code")
cipher = st.text_input(
    "🔐 Enter opportunity code name to Decipher:",
    placeholder="Enter generated code (e.g., #Airside#Sbtp-Efo#Cima)",
)

if st.button("🕵️‍♂️ Decipher Code"):
    if not cipher:
        st.error("⚠️ Please enter a cipher code to decipher.")
    else:
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
                st.error("❌ Invalid Cipher Code. Please check your entry.")
            else:
                st.success("🔓 Deciphered Details:")
                st.write(f"**LoB:** {original_lob}")
                st.write(f"**Owner:** {original_owner}")
                st.write(f"**Facility:** {original_facility}")
                st.write(f"**Area:** {original_area}")
        except ValueError:
            st.error("❌ Invalid Cipher Code format. Please use the correct format.")
        except Exception as e:
            st.error("❌ An unexpected error occurred while deciphering the code.")
