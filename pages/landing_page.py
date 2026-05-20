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


# Header
col1, col2 = st.columns([3, 1], width= 'stretch')

with col1:
    st.header(" AtomizeAI")

with col2:
    st.caption("MVP v1.0", text_alignment= 'right')

st.divider()

# Step indicator
step_cols = st.columns(6)

steps = ["Start", "Source", "Preferences", "Generate", "Revise", "Export"]

for index, step_name in enumerate(steps):
    with step_cols[index]:
        if index == 0:
            st.markdown("## ①")
        else:
            st.markdown(f"### {index + 1}")

        st.caption(step_name)

st.divider()

# Main question
st.caption("WHAT DO YOU WANT TO DO TODAY?")

# Two option cards
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("## 🔁")
        st.markdown("* 📄Repurpose Existing Content *")
        st.caption("Transform articles or documents you already have")

        if st.button("Choose Repurpose", use_container_width=True):
            st.session_state.content_path = "repurpose"

with col2:
    with st.container(border=True):
        st.markdown("### 💡")
        st.markdown("**No idea yet**")
        st.caption("Answer a few questions and we’ll build your content from scratch")

        if st.button("Choose No Idea Yet", use_container_width=True):
            st.session_state.content_path = "no_idea"

# Show selected option
if st.session_state.content_path == "repurpose":
    st.success("Selected path: Repurpose existing content")

elif st.session_state.content_path == "no_idea":
    st.success("Selected path: No idea yet")

# Information box
st.info(
    "Both paths lead to the same AI engine. Choose based on whether you already have content or not."
)

# Next button placeholder
if st.button("Next →"):
    if st.session_state.content_path is None:
        st.warning("Please choose one option before proceeding.")
    else:
        st.success("Proceeding to Step 2 soon.")