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

if "article_text" not in st.session_state:
    st.session_state.article_text = ""

if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

# Trigger variables for navigation buttons
if "step2_back_trigger" not in st.session_state:
    st.session_state.step2_back_trigger = False
if "step2_next_trigger" not in st.session_state:
    st.session_state.step2_next_trigger = False


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
# STEP 2 INPUT CONTENT AREA
# -----------------------------

# Information box

st.info(
    "Repurposing Existing Content"
)

with st.container(border= True):
    st.markdown("🗒️**PROVIDE YOUR CONTENT**", width="stretch")

    # Text area for pasting article or text
    with st.container(border=True):
        st.session_state.article_text = st.text_area(" ", placeholder = "Paste your articles or any written content here...", max_chars = 18000, height=200, value=st.session_state.article_text)
       
    # File uploader for document/image
    upload_file = st.file_uploader(
        "Or upload image or document file:",
        type=["jpg", "png", "pdf", "docx"], max_upload_size= 10 ,  # 10 MB limit
    )
    if upload_file:
        st.session_state.uploaded_file = upload_file
    


# -----------------------------
# NAVIGATION BUTTONS
# -----------------------------

col1, col2, col3 = st.columns([1, 16, 1])

with col1:
    if st.button("← Back"):
            st.session_state.step2_back_trigger = True

with col3:
    if st.button("Next →"):
            st.session_state.step2_next_trigger = True

if st.session_state.step2_back_trigger:
    st.session_state.current_step = 1
    st.session_state.step2_back_trigger = False
    

if st.session_state.step2_next_trigger:
    st.session_state.current_step = 3
    st.session_state.step2_next_trigger = False
     
# -----------------------------
# PROCESS SELECTION AND STORE IN DICTIONARY
# -----------------------------
if st.session_state.step2_next_trigger:
    
    # --- Update dictionary with latest  values - Repurpose ---
    st.session_state.llm_prompt_inputs["content_path"]= "preferences"  # Set content path for next step
    st.session_state.llm_prompt_inputs["step2_context"]["article_text"] = st.session_state.article_text
    st.session_state.llm_prompt_inputs["step2_context"]["uploaded_file"] = st.session_state.uploaded_file

    

   