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
    st.session_state.current_step = 3

# Step 3 preference defaults
if "platform" not in st.session_state:
    st.session_state.platform = ""
if "output_type" not in st.session_state:
    st.session_state.output_type = ""
if "tone" not in st.session_state:
    st.session_state.tone =   ""  
if "length" not in st.session_state:
    st.session_state.length = ""
if "language" not in st.session_state:
    st.session_state.language = ""
if "target_audience_preferences" not in st.session_state:
    st.session_state.target_audience_preferences = ""



#Step 3 Requirements:
# if st.session_state.content_path == "preferences" and st.session_state.current_step == 3:


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
# STEP 3 PREFERENCES INPUTS
# -----------------------------

st.info(
    "Select your platform, output type, tone, length, language, and target audience to customize your generated content."
)

# Platform selection
st.session_state.platform = st.multiselect(
    "Platform", max_selections=1, placeholder="Select your platform...",
    options=["Facebook", "Instagram", "TikTok", "LinkedIn", "Blog"],
    default=st.session_state.platform
)

# Output type
st.session_state.output_type = st.multiselect(
    "Output Type", max_selections=1, placeholder="Select your output type...",
    options=["Caption", "Script", "Article", "Carousel copy", "Thread"],
    default=st.session_state.output_type
)

# Target audience
st.session_state.target_audience_preferences = st.text_input(
    "Target Audience", max_chars= 100, placeholder="e.g., “Online sellers, boutique agencies, young moms” ",
    value=st.session_state.target_audience_preferences
)

# Tone
st.session_state.tone = st.radio(
    "Tone",
    options=["Friendly", "Professional", "Casual", "Persuasive", "Educational"],
    index=["Friendly", "Professional", "Casual", "Persuasive", "Educational"].index(st.session_state.tone)
)

# Length
st.session_state.length = st.radio(
    "Length",
    options=["Short", "Medium", "Long"],
    index=["Short", "Medium", "Long"].index(st.session_state.length)
)

# Language
st.session_state.language = st.radio(
    "Language",
    options=["English", "Tagalog", "Taglish"],
    index=["English", "Tagalog", "Taglish"].index(st.session_state.language)
)

# -----------------------------
# NAVIGATION BUTTONS
# -----------------------------

col1, col2, col3 = st.columns([1, 10, 1])

with col1:
    if st.button("← Back"):
            st.session_state.current_step = 3 # Return to Step 3

with col3:
    if st.button("Next →"):
            st.session_state.current_step = 4  # Advance to Step 4
            st.session_state.content_path  =  "generate"  # Set content path to generate for next step

