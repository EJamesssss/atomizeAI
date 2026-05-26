import streamlit as st
import time

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="AtomizeAI", page_icon="🤖", layout="wide")

# -----------------------------
# SESSION STATE INIT
# -----------------------------
if "current_step" not in st.session_state:
    st.session_state.current_step = 4
if "llm_prompt_inputs" not in st.session_state:
    st.session_state.llm_prompt_inputs = {}

# Triggers
for trigger in ["generate_trigger", "revise_trigger", "image_trigger", "new_content_trigger"]:
    if trigger not in st.session_state:
        st.session_state[trigger] = False

# -----------------------------
# HEADER & STEP INDICATOR
# -----------------------------
col1, col2 = st.columns([3,1])
with col1:
    st.header(" ⚛️ AtomizeAI")
with col2:
    st.caption("MVP v1.0", text_alignment='right')
st.divider()

# Stepper - 4 steps only
steps = ["Start", "Source/Context", "Preferences", "Generate"]
step_cols = st.columns(len(steps)*2-1)
for i, step in enumerate(steps):
    if i == 3:  # Highlight current step
        step_cols[i*2].markdown(
            f"<div style='text-align:center'><span style='font-size:24px; background-color:#000; color:#fff; border-radius:50%; width:32px; height:32px; display:inline-block; line-height:32px'>{i+1}</span><br>{step}</div>",
            unsafe_allow_html=True
        )
    else:
        step_cols[i*2].markdown(
            f"<div style='text-align:center; color:#ccc'>{i+1}<br>{step}</div>",
            unsafe_allow_html=True
        )
    if i < len(steps)-1:
        step_cols[i*2+1].markdown("<div style='height:2px; background-color:#ccc; margin-top:16px;'></div>", unsafe_allow_html=True)
st.divider()

# -----------------------------
# STEP 4: PREVIEW STEP 2 + STEP 3
# -----------------------------
st.info("Preview all your inputs from Step 2 (context) and Step 3 (preferences). You can edit before generating content.")

inputs = st.session_state.llm_prompt_inputs

# ---- Step 2 inputs (No Idea) ----
inputs["main_topic"] = st.text_input("Main Topic / Idea:", value=inputs.get("main_topic",""))
inputs["keywords"] = st.text_input("Keywords / Key Phrases:", value=inputs.get("keywords",""))
inputs["background"] = st.text_area("Background / Description:", value=inputs.get("background",""), height=100)
inputs["key_message"] = st.text_input("Key Message / CTA:", value=inputs.get("key_message",""))

# ---- Step 3 inputs (Preferences) ----
inputs["platform"] = st.selectbox("Platform:", ["Facebook","Instagram","TikTok","LinkedIn","Blog"], index=["Facebook","Instagram","TikTok","LinkedIn","Blog"].index(inputs.get("platform","Facebook")))
inputs["output_type"] = st.selectbox("Output Type:", ["Caption","Script","Article","Carousel copy","Thread"], index=["Caption","Script","Article","Carousel copy","Thread"].index(inputs.get("output_type","Caption")))
inputs["target_audience"] = st.text_input("Target Audience:", value=inputs.get("target_audience",""))
inputs["tone"] = st.radio("Tone:", ["Friendly","Professional","Casual","Persuasive","Educational"], index=["Friendly","Professional","Casual","Persuasive","Educational"].index(inputs.get("tone","Friendly")))
inputs["length"] = st.radio("Length:", ["Short","Medium","Long"], index=["Short","Medium","Long"].index(inputs.get("length","Medium")))
inputs["language"] = st.radio("Language:", ["English","Tagalog","Taglish"], index=["English","Tagalog","Taglish"].index(inputs.get("language","English")))

st.session_state.llm_prompt_inputs = inputs

# -----------------------------
# GENERATE CONTENT BUTTON (bottom full-width)
# -----------------------------
if not st.session_state.generate_trigger:
    if st.button("Generate Content", use_container_width=True):
        st.session_state.generate_trigger = True
        with st.spinner("Generating content..."):
            time.sleep(2)
        st.success("Content generated! Dictionary sent to backend:")
        st.code(st.session_state.llm_prompt_inputs)

# -----------------------------
# POST-GENERATION BUTTONS
# -----------------------------
if st.session_state.generate_trigger:
    if st.button("Revise Content", use_container_width=True):
        st.session_state.revise_trigger = True
    if st.button("Generate Image", use_container_width=True):
        st.session_state.image_trigger = True
    if st.button("Start a New Content", use_container_width=True):
        st.session_state.new_content_trigger = True

# -----------------------------
# REVISION CHATBOT
# -----------------------------
if st.session_state.revise_trigger:
    st.info("Atomize Chatbot - Customize your content")
    revision_text = st.text_area("Enter your revision instructions here", "")
    if st.button("Apply Revision", use_container_width=True):
        st.session_state.llm_prompt_inputs["revision"] = revision_text
        st.success("Revision applied!")
        st.text_area("Revised Content Preview:", value=revision_text or "Original content preview")

# -----------------------------
# IMAGE GENERATION PLACEHOLDER
# -----------------------------
if st.session_state.image_trigger:
    st.info("AI Image generated (placeholder)")
    st.image("https://via.placeholder.com/400x300.png?text=Generated+Image", use_column_width=True)

# -----------------------------
# START NEW CONTENT
# -----------------------------
if st.session_state.new_content_trigger:
    for key in ["current_step","content_path","generate_trigger","revise_trigger","image_trigger","new_content_trigger"]:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.llm_prompt_inputs = {}
    st.experimental_rerun()