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

# Step 3 default values
defaults = {
    "platform": "Facebook",
    "output_type": "Caption",
    "target_audience": "",
    "tone": "Friendly",
    "length": "Medium",
    "language": "English"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Triggers for navigation buttons
if "step3_back_trigger" not in st.session_state:
    st.session_state.step3_back_trigger = False
if "step3_next_trigger" not in st.session_state:
    st.session_state.step3_next_trigger = False




#Step 3 Requirements:
# if st.session_state.content_path == "preferences" and st.session_state.current_step == 3:


# Define steps
steps = ["Start", "Source/Context", "Preferences", "Generate", "Revise", "Export"]

# Step indicator
step_cols = st.columns(len(steps) * 2 - 1)  # Add space 

    
# Stepper 4 steps
steps = ["Start", "Source/Context", "Preferences", "Generate"]
step_cols = st.columns(len(steps)*2-1)
for i, step in enumerate(steps):
    if i == 3:
        step_cols[i*2].markdown(
            f"<div style='text-align:center'><span style='font-size:24px; background-color:#000; color:#fff; border-radius:50%; width:32px; height:32px; display:inline-block; line-height:32px'>{i+1}</span><br>{step}</div>",
            unsafe_allow_html=True
        )
    else:
        step_cols[i*2].markdown(f"<div style='text-align:center; color:#ccc'>{i+1}<br>{step}</div>", unsafe_allow_html=True)
    if i < len(steps)-1:
        step_cols[i*2+1].markdown("<div style='height:2px; background-color:#ccc; margin-top:16px;'></div>", unsafe_allow_html=True)
st.divider()

# -----------------------------
# STEP 3 PREFERENCES INPUTS
# -----------------------------

st.info(
    "Select your platform, output type, tone, length, language, and target audience to customize your generated content."
)

# Platform selection
st.session_state.platform = st.selectbox(
    "Platform",
    options=["Facebook", "Instagram", "TikTok", "LinkedIn", "Blog"],
    index=["Facebook", "Instagram", "TikTok", "LinkedIn", "Blog"].index(st.session_state.platform)
)

# Output type
st.session_state.output_type = st.selectbox(
    "Output Type",
    options=["Caption", "Script", "Article", "Carousel copy", "Thread"],
    index=["Caption", "Script", "Article", "Carousel copy", "Thread"].index(st.session_state.output_type)
)

# Target audience
st.session_state.target_audience = st.text_input(
    "Target Audience",
    max_chars=100,
    placeholder="e.g., Online sellers, boutique agencies, young moms",
    value=st.session_state.target_audience
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
        st.session_state.step3_back_trigger = True
with col3:
    if st.button("Next →"):
        st.session_state.step3_next_trigger = True

# -----------------------------
# PROCESS TRIGGERS
# -----------------------------
# Go back to Step 2
if st.session_state.step3_back_trigger:
    st.session_state.current_step = 2
    st.session_state.step3_back_trigger = False
    

# Advance to Step 4 and save preferences
if st.session_state.step3_next_trigger:
    st.session_state.current_step = 4
    st.session_state.step3_next_trigger = False
    st.session_state.content_path = "generate"
    # Save all Step 3 preferences to llm_prompt_inputs
    st.session_state.llm_prompt_inputs["step3_preferences"] = {
        "platform": st.session_state.platform,
        "output_type": st.session_state.output_type,
        "target_audience": st.session_state.target_audience,
        "tone": st.session_state.tone,
        "length": st.session_state.length,
        "language": st.session_state.language
    }

