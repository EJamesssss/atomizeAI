import streamlit as st
from utils.session import get_payload, update_payload


st.session_state.current_step = 3

# -----------------------------
# HEADER
# -----------------------------
col1, col2 = st.columns([3, 1], width="stretch")

with col1:
    st.header(" ⚛️ AtomizeAI")

with col2:
    st.caption("MVP v1.0", text_alignment="right")

st.divider()


# -----------------------------
# SESSION STATE INITIALIZATION
# -----------------------------
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


# -----------------------------
# STEP INDICATOR
# -----------------------------
steps = ["Start", "Source/Context", "Preferences", "Generate"]
step_cols = st.columns(len(steps) * 2 - 1)

for i, step in enumerate(steps):
    if i == st.session_state.current_step - 1:
        step_cols[i * 2].markdown(
            f"<div style='text-align:center'><span style='font-size:24px; background-color:#000; color:#fff; "
            f"border-radius:50%; width:32px; height:32px; display:inline-block; line-height:32px'>{i + 1}</span><br>{step}</div>",
            unsafe_allow_html=True
        )
    else:
        step_cols[i * 2].markdown(
            f"<div style='text-align:center; color:#ccc'>{i + 1}<br>{step}</div>",
            unsafe_allow_html=True
        )

    if i < len(steps) - 1:
        step_cols[i * 2 + 1].markdown(
            "<div style='height:2px; background-color:#ccc; margin-top:16px;'></div>",
            unsafe_allow_html=True
        )

st.divider()


# -----------------------------
# STEP 3 PREFERENCES INPUTS
# -----------------------------
st.info(
    "Select your platform, output type, tone, length, language, and target audience to customize your generated content."
)

st.session_state.platform = st.selectbox(
    "Platform *",
    options=["Facebook", "Instagram", "TikTok", "LinkedIn", "Blog"],
    index=["Facebook", "Instagram", "TikTok", "LinkedIn", "Blog"].index(st.session_state.platform)
)

st.session_state.output_type = st.selectbox(
    "Output Type *",
    options=["Caption", "Script", "Article", "Carousel copy", "Thread"],
    index=["Caption", "Script", "Article", "Carousel copy", "Thread"].index(st.session_state.output_type)
)

st.session_state.target_audience = st.text_input(
    "Target Audience *",
    max_chars=100,
    placeholder="e.g., Online sellers, boutique agencies, young moms",
    value=st.session_state.target_audience
)

st.session_state.tone = st.radio(
    "Tone *",
    options=["Friendly", "Professional", "Casual", "Persuasive", "Educational"],
    index=["Friendly", "Professional", "Casual", "Persuasive", "Educational"].index(st.session_state.tone)
)

st.session_state.length = st.radio(
    "Length *",
    options=["Short", "Medium", "Long"],
    index=["Short", "Medium", "Long"].index(st.session_state.length)
)

st.session_state.language = st.radio(
    "Language *",
    options=["English", "Tagalog", "Taglish"],
    index=["English", "Tagalog", "Taglish"].index(st.session_state.language)
)


# -----------------------------
# VALIDATION MESSAGE AREA
# -----------------------------
error_placeholder = st.empty()


# -----------------------------
# NAVIGATION BUTTONS
# -----------------------------
col1, col2, col3 = st.columns([1, 10, 1])

with col1:
    if st.button("← Back"):
        st.session_state.current_step = 2

        payload = get_payload()

        if payload.get("content_path") == "repurpose":
            st.switch_page("pages/step2_repurpose.py")
        elif payload.get("content_path") == "no_idea":
            st.switch_page("pages/step2_no_idea.py")
        else:
            st.switch_page("pages/step1_home.py")

with col3:
    if st.button("Next →"):
        required_errors = []

        if not st.session_state.platform:
            required_errors.append("Platform is required.")

        if not st.session_state.output_type:
            required_errors.append("Output Type is required.")

        if not st.session_state.target_audience.strip():
            required_errors.append("Target Audience is required.")

        if not st.session_state.tone:
            required_errors.append("Tone is required.")

        if not st.session_state.length:
            required_errors.append("Length is required.")

        if not st.session_state.language:
            required_errors.append("Language is required.")

        if required_errors:
            with error_placeholder.container():
                for error in required_errors:
                    st.error(error)
            st.stop()

        update_payload({
            "platform": st.session_state.platform,
            "output_type": st.session_state.output_type,
            "target_audience": st.session_state.target_audience.strip(),
            "tone": st.session_state.tone,
            "length": st.session_state.length,
            "language": st.session_state.language
        })

        st.session_state.current_step = 4
        st.switch_page("pages/step4_generate.py")


# -----------------------------
# DEBUG PAYLOAD
# -----------------------------
with st.expander("Debug payload"):
    st.json(get_payload(), expanded=True)