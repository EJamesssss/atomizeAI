import streamlit as st

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------

# Set the browser tab title, icon, and layout style
st.set_page_config(
    page_title="AtomizeAI",
    page_icon="🤖",
    layout="wide"
)

# Header
col1, col2 = st.columns([3, 1], width= 'stretch')

with col1:
    st.header(" ⚛️ AtomizeAI")

with col2:
    st.caption("MVP v1.0", text_alignment= 'right')

st.divider()


# -----------------------------
# SESSION STATE INITIALIZING
# -----------------------------

if "content_path" not in st.session_state:
    st.session_state.content_path = None

if "current_step" not in st.session_state:
    st.session_state.current_step = 2

#Step 2 Requirements:
# if st.session_state.content_path == "no_idea" and st.session_state.current_step == 2:

# Define steps
steps = ["Start", "Source/Context", "Preferences", "Generate", "Revise", "Export"]

# Step indicator
step_cols = st.columns(len(steps) * 2 - 1)  # Add space 

# Define steps
steps = ["Start", "Source/Context", "Preferences", "Generate", "Revise", "Export"]

# Step indicator
step_cols = st.columns(len(steps) * 2 - 1)  # Add space 
    
for i, step in enumerate(steps):
# Current step: filled circle using CSS for styling
    if i == st.session_state.current_step - 1:
        step_cols[i*2].markdown(f"<div style='text-align:center'><span style='font-size:24px; background-color:#000; color:#fff; border-radius:50%; width:32px; height:32px; display:inline-block; line-height:32px'>{i+1}</span><br>{step}</div>", unsafe_allow_html=True)
    else:
        # Other steps: outlined circle
        step_cols[i*2].markdown(f"<div style='text-align:center'><span style='font-size:24px; border:2px solid #ccc; border-radius:50%; width:32px; height:32px; display:inline-block; line-height:32px'>{i+1}</span><br>{step}</div>", unsafe_allow_html=True)
        
    # Add connecting line between steps
    if i < len(steps) -1:
        step_cols[i*2 +1].markdown("<div style='height:2px; background-color:#ccc; margin-top:16px;'></div>", unsafe_allow_html=True)

st.divider()

# -----------------------------
# STEP 2 INPUT CONTENT AREA
# -----------------------------

# Information box

st.info(
    "Generate your Ideas by providing context and details about your content. The more specific you are, the better AtomizeAI can assist you in creating tailored content."
)


# Input fields for context
st.session_state.main_topic = st.text_input(
    "Main Topic /Idea:", placeholder="e.g., “Skincare product launch” ", max_chars =  150,
    value=st.session_state.get("main_topic", "")
)
st.session_state.content_type = st.text_input(
    "Content Type /Goal:", placeholder="e.g., “Product description”, “Social media caption” ", max_chars =  150,
    value=st.session_state.get("content_type", "")
)
st.session_state.keywords = st.text_input(
    "Keywords /Key Phrases: ", placeholder=" e.g., “affordable, glowing skin, Filipino seller” ", max_chars =  250,
    value=st.session_state.get("keywords", "")
)
st.session_state.background = st.text_area(
    "Background /Description: ", placeholder=" e.g., “This is a new skincare product targeting online sellers in the Philippines.” ", max_chars =  2000,
    value=st.session_state.get("background", ""), 
    height=100
)
st.session_state.target_audience = st.text_input(
    "Target Audience", placeholder=" e.g., “Online sellers, boutique agencies, young moms” ",  max_chars =  250,
    value=st.session_state.get("target_audience", "")
)
st.session_state.key_message = st.text_input(
    "Key Message / Call-to-Action", placeholder=" e.g., “affordable, glowing skin, Filipino seller” ", max_chars =  500,
    value=st.session_state.get("key_message", "")
)
st.session_state.word_count = st.text_input(
    "Approximate Word Count (optional)", placeholder=" e.g., “around 100 words” ", max_chars =  100, 
    value=st.session_state.get("word_count", "")
)

st.divider()

# -----------------------------
# NAVIGATION BUTTONS
# -----------------------------

col1, col2, col3 = st.columns([1, 16, 1])

with col1:
    if st.button("← Back"):
            st.session_state.current_step = 1  # Return to Step 1

with col3:
    if st.button("Next →"):
            st.session_state.current_step = 3  # Advance to Step 3
            st.session_state.content_path  =  "preferences"  # Set content path to preferences for next step