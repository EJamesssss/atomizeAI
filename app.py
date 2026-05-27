import streamlit as st
import time


# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================
if "current_step" not in st.session_state:
    st.session_state.current_step = 1
if "content_path" not in st.session_state:
    st.session_state.content_path = None

# Master dictionary — single source of truth sent to LLM backend
if "llm_prompt_inputs" not in st.session_state:
    st.session_state.llm_prompt_inputs = {
        # Set in Step 1
        "content_path": None,           # "repurpose" | "no_idea"

        # Set in Step 2A (repurpose path)
        "article_text": "",
        "uploaded_file": None,

        # Set in Step 2B (no_idea path)
        "main_topic": "",
        "keywords": "",
        "background": "",
        "key_message": "",

        # Set in Step 3 (preferences) — shared by both paths
        "platform": "Facebook",
        "output_type": "Caption",
        "target_audience": "",
        "tone": "Friendly",
        "length": "Medium",
        "language": "English",

        # Set in Step 4 (post-generation)
        "revision": "",
    }

# Generation / UI triggers (separate from prompt data)
for trigger in ["generate_trigger", "revise_trigger", "image_trigger", "new_content_trigger"]:
    if trigger not in st.session_state:
        st.session_state[trigger] = False


# ============================================================
# SHORTHAND — cleaner reads/writes to llm_prompt_inputs
# ============================================================
def get(key):
    return st.session_state.llm_prompt_inputs.get(key, "")

def set_input(key, value):
    st.session_state.llm_prompt_inputs[key] = value


# ============================================================
# SHARED: PAGE CONFIG + HEADER + STEPPER
# ============================================================
def render_header_and_stepper():

    # -----------------------------
    # PAGE CONFIG
    # -----------------------------
    st.set_page_config(page_title="AtomizeAI", page_icon="🤖", layout="wide")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.header(" ⚛️ AtomizeAI")
    with col2:
        st.caption("MVP v1.0", text_alignment="right")
    st.divider()

    steps = ["Start", "Source/Context", "Preferences", "Generate"]
    step_cols = st.columns(len(steps) * 2 - 1)
    for i, step in enumerate(steps):
        if i == st.session_state.current_step - 1:
            step_cols[i * 2].markdown(
                f"<div style='text-align:center'>"
                f"<span style='font-size:24px; background-color:#000; color:#fff; "
                f"border-radius:50%; width:32px; height:32px; display:inline-block; line-height:32px'>"
                f"{i+1}</span><br>{step}</div>",
                unsafe_allow_html=True,
            )
        else:
            step_cols[i * 2].markdown(
                f"<div style='text-align:center; color:#ccc'>{i+1}<br>{step}</div>",
                unsafe_allow_html=True,
            )
        if i < len(steps) - 1:
            step_cols[i * 2 + 1].markdown(
                "<div style='height:2px; background-color:#ccc; margin-top:16px;'></div>",
                unsafe_allow_html=True,
            )
    st.divider()


# ============================================================
# STEP 1 — PATH SELECTION
# ============================================================
def render_step1():
    render_header_and_stepper()

    st.markdown("**WHAT DO YOU WANT TO DO TODAY?**")
    st.info(" Choose based on whether you already have content or not.")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("## 🔄", text_alignment="center")
            st.markdown("#### Repurpose Existing Content" , text_alignment="center")
            st.markdown("Transform content you already have.", text_alignment="center")
            if st.button("Choose Repurpose", use_container_width=True):
                set_input("content_path", "repurpose")
                st.session_state.content_path = "repurpose"
                st.session_state.current_step = 2
                st.rerun()

    with col2:
        with st.container(border=True):
            st.markdown("## 💡", text_alignment="center")
            st.markdown("#### No Idea Yet",text_alignment="center")
            st.markdown("Answer a few questions and we'll build your content from scratch.", text_alignment="center")
            if st.button("Choose No Idea Yet", use_container_width=True):
                set_input("content_path", "no_idea")
                st.session_state.content_path = "no_idea"
                st.session_state.current_step = 2
                st.rerun()


# ============================================================
# STEP 2A — REPURPOSE
# ============================================================
def render_step2_repurpose():
    render_header_and_stepper()

    st.info("Repurposing Existing Content")

    # Read from & write directly into llm_prompt_inputs
    updated_text = st.text_area("", 
        placeholder="Paste your article or content here...",
        value=get("article_text"),
        height=200,
        key="input_article_text",
        max_chars=18000
    )
    set_input("article_text", updated_text)

    uploaded_file = st.file_uploader(
        "Or upload an image/document file:",
        type=["jpg", "png", "pdf"],
        key="input_uploaded_file",
        max_upload_size=10
    )
    if uploaded_file:
        set_input("uploaded_file", uploaded_file)

    st.divider()
    col1, col2, col3 = st.columns([1, 16, 1])
    with col1:
        if st.button("← Back", key="step2r_back"):
            st.session_state.current_step = 1
            st.session_state.content_path = None
            set_input("content_path", None)
            st.rerun()
    with col3:
        if st.button("Next →", key="step2r_next"):
            st.session_state.current_step = 3
            st.rerun()


# ============================================================
# STEP 2B — NO IDEA
# ============================================================
def render_step2_noidea():
    render_header_and_stepper()

    st.info(
        "Generate your ideas by providing context and details about your content. "
        "The more specific you are, the better AtomizeAI can assist you."
    )

    # Each widget reads from & writes directly into llm_prompt_inputs
    set_input("main_topic", st.text_input(
        "Main Topic / Idea:",
        placeholder="e.g., Skincare product launch",
        max_chars=150,
        value=get("main_topic"),
        key="input_main_topic"
    ))
    set_input("keywords", st.text_input(
        "Keywords / Key Phrases:",
        placeholder="e.g., affordable, glowing skin, Filipino seller",
        max_chars=250,
        value=get("keywords"),
        key="input_keywords"
    ))
    set_input("background", st.text_area(
        "Background / Description:",
        placeholder="e.g., This is a new skincare product targeting online sellers in the Philippines.",
        max_chars=2000,
        height=100,
        value=get("background"),
        key="input_background"
    ))
    set_input("key_message", st.text_input(
        "Key Message / Call-to-Action:",
        placeholder="e.g., Promote a new skincare product for Filipino online sellers",
        max_chars=500,
        value=get("key_message"),
        key="input_key_message"
    ))

    st.divider()
    col1, col2, col3 = st.columns([1, 16, 1])
    with col1:
        if st.button("← Back", key="step2n_back"):
            st.session_state.current_step = 1
            st.session_state.content_path = None
            set_input("content_path", None)
            st.rerun()
    with col3:
        if st.button("Next →", key="step2n_next"):
            st.session_state.current_step = 3
            st.rerun()


# ============================================================
# STEP 3 — PREFERENCES
# ============================================================
def render_step3():
    render_header_and_stepper()

    st.info(
        "Select your platform, output type, tone, length, language, and target audience "
        "to customize your generated content."
    )

    PLATFORMS     = ["Facebook", "Instagram", "TikTok", "LinkedIn", "Blog"]
    OUTPUT_TYPES  = ["Caption", "Script", "Article", "Carousel copy", "Thread"]
    TONES         = ["Friendly", "Professional", "Casual", "Persuasive", "Educational"]
    LENGTHS       = ["Short", "Medium", "Long"]
    LANGUAGES     = ["English", "Tagalog", "Taglish"]

    set_input("platform", st.selectbox(
        "Platform",
        options=PLATFORMS,
        index=PLATFORMS.index(get("platform") or "Facebook"),
        key="input_platform"
    ))
    set_input("output_type", st.selectbox(
        "Output Type",
        options=OUTPUT_TYPES,
        index=OUTPUT_TYPES.index(get("output_type") or "Caption"),
        key="input_output_type"
    ))
    set_input("target_audience", st.text_input(
        "Target Audience",
        max_chars=100,
        placeholder="e.g., Online sellers, boutique agencies, young moms",
        value=get("target_audience"),
        key="input_target_audience"
    ))
    set_input("tone", st.radio(
        "Tone",
        options=TONES,
        index=TONES.index(get("tone") or "Friendly"),
        key="input_tone"
    ))
    set_input("length", st.radio(
        "Length",
        options=LENGTHS,
        index=LENGTHS.index(get("length") or "Medium"),
        key="input_length"
    ))
    set_input("language", st.radio(
        "Language",
        options=LANGUAGES,
        index=LANGUAGES.index(get("language") or "English"),
        key="input_language"
    ))

    st.divider()
    col1, col2, col3 = st.columns([1, 10, 1])
    with col1:
        if st.button("← Back", key="step3_back"):
            st.session_state.current_step = 2
            st.rerun()
    with col3:
        if st.button("Next →", key="step3_next"):
            st.session_state.current_step = 4
            st.rerun()


# ============================================================
# STEP 4 — PREVIEW & GENERATE
# ============================================================
def render_step4():
    render_header_and_stepper()

    st.info("Review all your inputs below. You can still edit before generating.")

    # ---- Step 2 editable preview ----
    if st.session_state.content_path == "repurpose":
        st.subheader("📋 Step 2: Repurpose Content")
        set_input("article_text", st.text_area(
            "Article / Content:",
            value=get("article_text"),
            height=200,
            key="step4_article_text"
        ))

        new_file = st.file_uploader(
            "Replace uploaded file (optional):",
            type=["jpg", "png", "pdf", "docx"],
            key="step4_file"
        )
        if new_file:
            set_input("uploaded_file", new_file)

        # ---- File preview ----
        file = new_file or st.session_state.llm_prompt_inputs.get("uploaded_file")
        if file is not None:
            st.markdown("**Preview:**")
            file_type = file.type  # e.g. "image/png", "application/pdf", etc.

            if file_type in ["image/png", "image/jpeg", "image/jpg"]:
                # Images — display directly
                st.image(file, use_container_width=True)

            elif file_type == "application/pdf":
                # PDF — embed via base64 iframe
                import base64
                file.seek(0)
                pdf_bytes = file.read()
                b64 = base64.b64encode(pdf_bytes).decode("utf-8")
                pdf_html = f"""
                    <iframe
                        src="data:application/pdf;base64,{b64}"
                        width="100%" height="500px"
                        style="border: 1px solid #ccc; border-radius: 6px;">
                    </iframe>
                """
                st.markdown(pdf_html, unsafe_allow_html=True)

           
            else:
                st.info(f"No preview available for file type: `{file_type}`")

    elif st.session_state.content_path == "no_idea":
        st.subheader("📋 Step 2: Context Inputs")
        set_input("main_topic",  st.text_input("Main Topic / Idea:",       value=get("main_topic"),  key="step4_main_topic"))
        set_input("keywords",    st.text_input("Keywords / Key Phrases:",   value=get("keywords"),    key="step4_keywords"))
        set_input("background",  st.text_area( "Background / Description:", value=get("background"),  height=100, key="step4_background"))
        set_input("key_message", st.text_input("Key Message / CTA:",        value=get("key_message"), key="step4_key_message"))

    # ---- Step 3 editable preview ----
    st.subheader("⚙️ Step 3: Preferences")

    PLATFORMS     = ["Facebook", "Instagram", "TikTok", "LinkedIn", "Blog"]
    OUTPUT_TYPES  = ["Caption", "Script", "Article", "Carousel copy", "Thread"]
    TONES         = ["Friendly", "Professional", "Casual", "Persuasive", "Educational"]
    LENGTHS       = ["Short", "Medium", "Long"]
    LANGUAGES     = ["English", "Tagalog", "Taglish"]

    set_input("platform",       st.selectbox("Platform:",     PLATFORMS,    index=PLATFORMS.index(get("platform") or "Facebook"),       key="step4_platform"))
    set_input("output_type",    st.selectbox("Output Type:",  OUTPUT_TYPES, index=OUTPUT_TYPES.index(get("output_type") or "Caption"),   key="step4_output_type"))
    set_input("target_audience",st.text_input("Target Audience:", value=get("target_audience"), key="step4_target_audience"))
    set_input("tone",           st.radio("Tone:",     TONES,    index=TONES.index(get("tone") or "Friendly"),   key="step4_tone"))
    set_input("length",         st.radio("Length:",   LENGTHS,  index=LENGTHS.index(get("length") or "Medium"), key="step4_length"))
    set_input("language",       st.radio("Language:", LANGUAGES,index=LANGUAGES.index(get("language") or "English"), key="step4_language"))

    st.divider()

    # ---- Generate button (only shown before generation) ----
    if not st.session_state.generate_trigger:
       if st.button("⚡ Generate Content", use_container_width=True):
            with st.spinner("Generating content... ⌛"):
                time.sleep(2)
                # ✅ This is the final payload sent to your LLM backend:
                # st.session_state.llm_prompt_inputs  ← fully populated here
                # TODO: replace time.sleep with your actual API call, e.g.:
                # response = call_llm_api(st.session_state.llm_prompt_inputs)
                # set_input("generated_output", response)
                st.session_state.generate_trigger = True
                st.rerun()

    # ---- Post-generation ----
    if st.session_state.generate_trigger:
        st.success("✅ Content generated!")
        # TODO: replace the line below with actual generated content
        st.subheader("📦 Payload sent to LLM backend:")
        # Show only relevant keys depending on path (exclude unused Step 2 fields)
        display_payload = {
            k: v for k, v in st.session_state.llm_prompt_inputs.items()
            if not (
                (st.session_state.content_path == "repurpose" and k in ["main_topic","keywords","background","key_message"])
                or
                (st.session_state.content_path == "no_idea"   and k in ["article_text","uploaded_file"])
            )
        }
        st.json(display_payload)

        st.divider()
        if not st.session_state.revise_trigger:
            if st.button("✏️ Revise Content", use_container_width=True):
                st.session_state.revise_trigger = True
                st.rerun()

        if not st.session_state.image_trigger:
            if st.button("🖼️ Generate Image", use_container_width=True):
                st.session_state.image_trigger = True
                st.rerun()

        if st.button("🆕 Start New Content", use_container_width=True):
            st.session_state.new_content_trigger = True
            st.rerun()

    # ---- Revision chatbot ----
    if st.session_state.revise_trigger:
        st.divider()
        st.info("Hi, I'm Atomize — your content assistant! Tell me how you'd like to revise your content.")
        revision_text = st.text_area(
            "Revision instructions:",
            placeholder="Type your revision instructions here...",
            key="revision_input"
        )
        if st.button("Apply Revision", use_container_width=True):
            set_input("revision", revision_text)
            # TODO: send updated llm_prompt_inputs (with "revision" key) to backend
            st.success("Revision applied!")
            st.text_area("Revised Content Preview:", value=revision_text or "Original content preview")

    # ---- Image generation placeholder ----
    if st.session_state.image_trigger:
        st.divider()
        st.info("AI Image generated (placeholder).") #TODO: replace with actual image from LLM API
        st.image("https://via.placeholder.com/400x300.png?text=Generated+Image", use_container_width=True)

    # ---- Reset / Start new ----
    if st.session_state.new_content_trigger:
        st.session_state.current_step = 1
        st.session_state.content_path = None
        st.session_state.generate_trigger = False
        st.session_state.revise_trigger   = False
        st.session_state.image_trigger    = False
        st.session_state.new_content_trigger = False
        st.session_state.llm_prompt_inputs = {
            "content_path": None,
            "article_text": "", "uploaded_file": None,
            "main_topic": "", "keywords": "", "background": "", "key_message": "",
            "platform": "Facebook", "output_type": "Caption", "target_audience": "",
            "tone": "Friendly", "length": "Medium", "language": "English",
            "revision": "",
        }
        st.rerun()


# ============================================================
# ROUTER
# ============================================================
step = st.session_state.current_step
path = st.session_state.content_path

if step == 1:
    render_step1()
elif step == 2:
    if path == "repurpose":
        render_step2_repurpose()
    elif path == "no_idea":
        render_step2_noidea()
    else:
        st.session_state.current_step = 1
        st.rerun()
elif step == 3:
    render_step3()
elif step == 4:
    render_step4()
