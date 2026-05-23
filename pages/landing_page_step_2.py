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
    st.session_state.article_text = None

if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None


#Step 2 Requirements:
# if st.session_state.content_path == "repurpose" and st.session_state.current_step == 2:

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
    "Repurposing Existing Content"
)

with st.container(border= True):
    st.markdown("🗒️**PROVIDE YOUR CONTENT**", width="stretch")

    # Text area for pasting article or text
    with st.container(border=True):
        st.session_state.article_text = st.text_area( placeholder = "Paste your articles or any written content here...", max_chars = 18000, height=200, value=st.session_state.article_text)
       
    # File uploader for document/image
    st.session_state.uploaded_file = st.file_uploader(
        "Or upload image or document file:",
        type=["jpg", "png", "pdf", "docx"], max_upload_size= 10 ,  # 10 MB limit
    )
    


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