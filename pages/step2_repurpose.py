import streamlit as st
import hashlib

from services.models.repurpose_analyzer import analyze_repurpose_input
from utils.session import get_payload, update_payload

## DEBUGGER

import time

DEBUG_ANALYZER = True


def debug_time(label, start_time):
    if DEBUG_ANALYZER:
        elapsed = time.perf_counter() - start_time
        st.write(f"⏱️ {label}: {elapsed:.2f} seconds")

### Debugger ends here

st.session_state.current_step = 2

def build_repurpose_hash(article_text, uploaded_file):
    file_name = ""
    file_bytes = b""

    if uploaded_file is not None:
        file_name = uploaded_file.name
        file_bytes = uploaded_file.getvalue()

    hash_source = article_text.encode("utf-8") + file_name.encode("utf-8") + file_bytes

    return hashlib.sha256(hash_source).hexdigest()

if "repurpose_input_hash" not in st.session_state:
    st.session_state.repurpose_input_hash = None

if "repurpose_analyzed_payload" not in st.session_state:
    st.session_state.repurpose_analyzed_payload = None

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
    type=["jpg", "jpeg", "png", "pdf", "docx", "txt"]
)

if uploaded_file is not None:
    st.session_state.uploaded_file = uploaded_file

# -----------------------------
# NAVIGATION BUTTONS
# -----------------------------
col1, col2, col3 = st.columns([2, 8, 2])

with col1:
    if st.button("← Back", use_container_width=True):
        st.session_state.step2_back_trigger = True

with col3:
    if st.button("Next →", use_container_width=True):
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
    st.session_state.step2_next_trigger = False

    total_start = time.perf_counter()

    article_text = st.session_state.article_text.strip()
    uploaded_file = st.session_state.uploaded_file

    debug_time("Loaded article text and uploaded file", total_start)

    if not article_text and uploaded_file is None:
        st.warning("Please paste content or upload a file before proceeding.")
        st.stop()

    try:
        with st.spinner("Analyzing your content..."):
            analyzer_start = time.perf_counter()

            analyzed_payload = analyze_repurpose_input(
                article_text=article_text,
                uploaded_file=uploaded_file,
                router_state=get_payload()
            )

            debug_time("Analyzer completed", analyzer_start)

        payload_start = time.perf_counter()

        update_payload(analyzed_payload)

        debug_time("Payload updated", payload_start)
        debug_time("Total Step 2 Next process", total_start)

        st.session_state.current_step = 3
        st.switch_page("pages/step3_preferences.py")

    except Exception as error:
        debug_time("Failed process duration", total_start)
        st.error(f"Failed to analyze content: {error}")


st.json(get_payload(), expanded=True)