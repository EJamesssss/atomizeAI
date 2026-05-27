import streamlit as st
from utils.session import init_payload, update_payload, get_payload


# -----------------------------
# SESSION STATE INITIALIZATION
# -----------------------------
init_payload()

st.session_state.current_step = 2

if "main_topic" not in st.session_state:
    st.session_state.main_topic = ""

if "keywords" not in st.session_state:
    st.session_state.keywords = ""

if "background" not in st.session_state:
    st.session_state.background = ""

if "key_message" not in st.session_state:
    st.session_state.key_message = ""

if "step2_noidea_back" not in st.session_state:
    st.session_state.step2_noidea_back = False

if "step2_noidea_next" not in st.session_state:
    st.session_state.step2_noidea_next = False


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
# STEPPER
# -----------------------------
steps = ["Start", "Source/Context", "Preferences", "Generate"]
step_cols = st.columns(len(steps) * 2 - 1)

for i, step in enumerate(steps):
    if i == st.session_state.current_step - 1:
        step_cols[i * 2].markdown(
            f"""
            <div style='text-align:center'>
                <span style='font-size:24px; background-color:#000; color:#fff;
                border-radius:50%; width:32px; height:32px; display:inline-block;
                line-height:32px'>{i + 1}</span><br>{step}
            </div>
            """,
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
# STEP 2 INPUT CONTENT AREA - NO IDEA
# -----------------------------
st.info(
    "Generate your ideas by providing context and details about your content. "
    "The more specific you are, the better AtomizeAI can assist you in creating tailored content."
)

st.session_state.main_topic = st.text_input(
    "Main Topic / Idea *",
    placeholder="e.g., Skincare product launch",
    max_chars=150,
    value=st.session_state.main_topic
)

st.session_state.keywords = st.text_input(
    "Keywords / Key Phrases *",
    placeholder="e.g., affordable, glowing skin, Filipino seller",
    max_chars=250,
    value=st.session_state.keywords
)

st.session_state.background = st.text_area(
    "Background / Description *",
    placeholder="e.g., This is a new skincare product targeting online sellers in the Philippines.",
    max_chars=2000,
    height=120,
    value=st.session_state.background
)

st.session_state.key_message = st.text_input(
    "Key Message / Call-to-Action *",
    placeholder="e.g., Promote a new skincare product for Filipino online sellers",
    max_chars=500,
    value=st.session_state.key_message
)

st.divider()


# -----------------------------
# VALIDATION MESSAGE AREA
# -----------------------------
error_placeholder = st.empty()


# -----------------------------
# NAVIGATION BUTTONS
# -----------------------------
col1, col2, col3 = st.columns([2, 8, 2])

with col1:
    if st.button("← Back", use_container_width=True):
        st.session_state.step2_noidea_back = True

with col3:
    if st.button("Next →", use_container_width=True):
        st.session_state.step2_noidea_next = True


# -----------------------------
# PROCESS TRIGGERS
# -----------------------------
if st.session_state.step2_noidea_back:
    st.session_state.current_step = 1
    st.session_state.step2_noidea_back = False
    st.switch_page("pages/step1_home.py")


if st.session_state.step2_noidea_next:
    st.session_state.step2_noidea_next = False

    required_errors = []

    if not st.session_state.main_topic.strip():
        required_errors.append("Main Topic / Idea is required.")

    if not st.session_state.keywords.strip():
        required_errors.append("Keywords / Key Phrases is required.")

    if not st.session_state.background.strip():
        required_errors.append("Background / Description is required.")

    if not st.session_state.key_message.strip():
        required_errors.append("Key Message / Call-to-Action is required.")

    if required_errors:
        with error_placeholder.container():
            for error in required_errors:
                st.error(error)
        st.stop()

    main_topic = st.session_state.main_topic.strip()
    keywords = st.session_state.keywords.strip()
    background = st.session_state.background.strip()
    key_message = st.session_state.key_message.strip()

    content_brief = f"""
Content summary:
The user wants to create new content from scratch based on their provided idea.

Main topic:
{main_topic}

Key message or purpose:
{key_message}

Important details:
{background}

Keywords or key phrases:
{keywords}

Facts, offers, products, or names mentioned:
Use only the details provided by the user. Do not invent unsupported claims.

Missing or unclear information:
Additional details may be guided by the user's Step 3 preferences.
""".strip()

    update_payload({
        "content_path": "no_idea",
        "source_type": "user_idea",
        "main_topic": main_topic,
        "keywords": keywords,
        "background": background,
        "key_message": key_message,
        "content_brief": content_brief
    })

    st.session_state.current_step = 3
    st.switch_page("pages/step3_preferences.py")


# -----------------------------
# DEBUG PAYLOAD
# -----------------------------
with st.expander("Debug payload"):
    st.json(get_payload(), expanded=False)