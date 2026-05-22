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

# -----------------------------
# SESSION STATE INITIALIZING
# -----------------------------

if "content_path" not in st.session_state:
    st.session_state.content_path = None

if "current_step" not in st.session_state:
    st.session_state.current_step = 1

# Header
col1, col2 = st.columns([3, 1], width= 'stretch')

with col1:
    st.header(" ⚛️ AtomizeAI")

with col2:
    st.caption("MVP v1.0", text_alignment= 'right')

st.divider()

# Define steps
steps = ["Start", "Source", "Preferences", "Generate", "Revise", "Export"]

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

# Main question
st.markdown("**WHAT DO YOU WANT TO DO TODAY?**", width="stretch")

# Information box
st.info(
    "Both paths lead to the same AI engine. Choose based on whether you already have content or not."
)


# Two option cards
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("## 🔄", text_alignment='center')
        st.markdown("#### Repurpose Existing Content" , text_alignment= 'center')
        st.markdown(" Transform contents you already have. ", text_alignment= 'center', width="stretch") 

        if st.button("Choose Repurpose", use_container_width=True):
            st.session_state.content_path = "repurpose"
            st.session_state.current_step = 2  # Move to next step

with col2:
    with st.container(border=True):
        st.markdown("## 💡", text_alignment='center')
        st.markdown("#### No Idea" , text_alignment= 'center')
        st.markdown("Answer a few questions and we’ll build your content from scratch.", text_alignment= 'center', width="stretch") 

        if st.button("Choose No idea Yet", use_container_width=True):
            st.session_state.content_path = "no_idea"
            st.session_state.current_step = 2  # Move to next step


# Show selected option
if st.session_state.content_path == "repurpose":
    st.success("Selected path: Repurpose existing content")

elif st.session_state.content_path == "no_idea":
    st.success("Selected path: No idea yet")


