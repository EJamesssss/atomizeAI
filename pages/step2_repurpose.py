import streamlit as st

from utils.session import get_payload

st.session_state.current_step = 2

# -----------------------------
# SESSION STATE INIT
# -----------------------------
if "current_step" not in st.session_state:
    st.session_state.current_step = 2
if "content_path" not in st.session_state:
    st.session_state.content_path = None



if "article_text" not in st.session_state:
    st.session_state.article_text = ""
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
if "step2_back_trigger" not in st.session_state:
    st.session_state.step2_back_trigger = False
if "step2_next_trigger" not in st.session_state:
    st.session_state.step2_next_trigger = False

# -----------------------------
# HEADER
# -----------------------------
col1, col2 = st.columns([3,1])
with col1:
    st.header(" ⚛️ AtomizeAI")
with col2:
    st.caption("MVP v1.0", text_alignment='right')
st.divider()

# -----------------------------
# STEP INDICATOR (dynamic highlight)
# -----------------------------
steps = ["Start", "Source/Context", "Preferences", "Generate"]
step_cols = st.columns(len(steps)*2-1)
for i, step in enumerate(steps):
    if i == st.session_state.current_step - 1:
        step_cols[i*2].markdown(
        f"<div style='text-align:center'><span style='font-size:24px; background-color:#000; color:#fff; "
        f"border-radius:50%; width:32px; height:32px; display:inline-block; line-height:32px'>{i+1}</span><br>{step}</div>",
        unsafe_allow_html=True
        )
    else:
        step_cols[i*2].markdown(
            f"<div style='text-align:center; color:#ccc'>{i+1}<br>{step}</div>",
            unsafe_allow_html=True
        )
    if i < len(steps)-1:
        step_cols[i*2+1].markdown(
            "<div style='height:2px; background-color:#ccc; margin-top:16px;'></div>",
            unsafe_allow_html=True
        )
st.divider()

# -----------------------------
# INPUT AREA
# -----------------------------
st.info("Repurposing Existing Content")

# Text area
st.session_state.article_text = st.text_area(
    "Paste your article or content here:",
    value=st.session_state.article_text,
    height=200
)

# File uploader
uploaded_file = st.file_uploader(
    "Or upload image/document file:",
    type=["jpg","png","pdf","docx"],
    max_upload_size=10
)
if uploaded_file:
    st.session_state.uploaded_file = uploaded_file

# -----------------------------
# NAVIGATION BUTTONS
# -----------------------------
col1, col2, col3 = st.columns([1,16,1])
with col1:
    if st.button("← Back"):
        st.session_state.step2_back_trigger = True
with col3:
    if st.button("Next →"):
        st.session_state.step2_next_trigger = True

# -----------------------------
# TRIGGER PROCESSING
# -----------------------------
# Back to Step 1
if st.session_state.step2_back_trigger:
    st.session_state.current_step = 1
    st.session_state.step2_back_trigger = False
    st.switch_page("pages/step1_home.py")
    

# Next to Step 3
if st.session_state.step2_next_trigger:
    st.session_state.current_step = 3
    st.session_state.step2_next_trigger = False


    st.switch_page("pages/step3_preferences.py")


st.json(get_payload(), expanded=True)