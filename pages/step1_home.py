import streamlit as st
from utils.session import init_payload, update_payload

init_payload()  # This function ensures that the payload is initialized in session state if it doesn't already exist.

# -----------------------------
# SESSION STATE INIT
# -----------------------------
if "current_step" not in st.session_state:
    st.session_state.current_step = 1
if "content_path" not in st.session_state:
    st.session_state.content_path = None
if "llm_prompt_inputs" not in st.session_state:
    st.session_state.llm_prompt_inputs = {}

# -----------------------------
# HEADER
# -----------------------------
col1, col2 = st.columns([3, 1], width='stretch')
with col1:
    st.header(" ⚛️ AtomizeAI")
with col2:
    st.caption("MVP v1.0", text_alignment='right')
st.divider()

# -----------------------------
# STEP INDICATOR
# -----------------------------

steps = ["Start", "Source/Context", "Preferences", "Generate"]
step_cols = st.columns(len(steps)*2-1)
for i, step in enumerate(steps):
    if i == st.session_state.current_step -1:
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
# MAIN QUESTION
# -----------------------------
st.markdown("**WHAT DO YOU WANT TO DO TODAY?**", width="stretch")
st.info("Both paths lead to the same AI engine. Choose based on whether you already have content or not.")

# -----------------------------
# OPTION CARDS - "repurpose or no_idea"
# -----------------------------

col1, col2 = st.columns(2)


with col1:
    with st.container(border = True):
        st.markdown("## 🔄", text_alignment='center')
        st.markdown("#### Repurpose Existing Content", text_alignment='center')
        st.markdown("Transform contents you already have.", text_alignment='center', width="stretch")
        if st.button("Choose Repurpose", use_container_width=True):
            update_payload({"action": "repurpose"})
            st.switch_page("pages/step2_repurpose.py")  # Navigate to Step 2 Repurpose page

with col2:
    with st.container(border = True):
        st.markdown("## 💡", text_alignment='center')
        st.markdown("#### No Idea", text_alignment='center')
        st.markdown("Answer a few questions and we’ll build your content from scratch.", text_alignment='center', width="stretch")
        if st.button("Choose No Idea Yet", use_container_width=True):
            update_payload({"action": "no_idea"})
            st.switch_page("pages/step2_no_idea.py")  # Navigate to Step 2 No Idea page