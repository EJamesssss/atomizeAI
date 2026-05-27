import streamlit as st

from utils.session import get_payload, update_payload
from utils.clipboard import copy_to_clipboard_button

from services.models.caption_generator import (
    generate_content_from_payload,
    revise_content_from_payload
)

from services.comfyui.image_service import generate_image_from_payload
from services.comfyui.client import get_image_bytes


st.session_state.current_step = 4


# -----------------------------
# SESSION STATE INIT
# -----------------------------
for trigger in [
    "generate_trigger",
    "revise_trigger",
    "image_trigger",
    "new_content_trigger"
]:
    if trigger not in st.session_state:
        st.session_state[trigger] = False

if "generated_content" not in st.session_state:
    st.session_state.generated_content = ""

if "revision_success_message" not in st.session_state:
    st.session_state.revision_success_message = False

if "generation_success_message" not in st.session_state:
    st.session_state.generation_success_message = False

if "image_success_message" not in st.session_state:
    st.session_state.image_success_message = False


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
# STEP INDICATOR
# -----------------------------
steps = ["Start", "Source/Context", "Preferences", "Generate"]
step_cols = st.columns(len(steps) * 2 - 1)

for i, step in enumerate(steps):
    if i == st.session_state.current_step - 1:
        step_cols[i * 2].markdown(
            f"<div style='text-align:center'>"
            f"<span style='font-size:24px; background-color:#000; color:#fff; "
            f"border-radius:50%; width:32px; height:32px; display:inline-block; "
            f"line-height:32px'>{i + 1}</span><br>{step}</div>",
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
# LOAD PAYLOAD
# -----------------------------
payload = get_payload()

# Always sync generated content from payload if available
if payload.get("generated_content"):
    st.session_state.generated_content = payload.get("generated_content")


# -----------------------------
# PAGE INTRO
# -----------------------------
st.info(
    "Review the content analysis and selected preferences before generating the final content."
)


# -----------------------------
# SOURCE / CONTENT ANALYSIS
# -----------------------------
st.subheader("Content Analysis")

content_path = payload.get("content_path", "Not provided")
source_type = payload.get("source_type", "Not provided")
uploaded_file_name = payload.get("uploaded_file_name")
uploaded_file_type = payload.get("uploaded_file_type")
uploaded_file_size = payload.get("uploaded_file_size")
article_text = payload.get("article_text")
content_brief = payload.get("content_brief")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Content Path:**")
    st.write(content_path)

    st.markdown("**Source Type:**")
    st.write(source_type)

with col2:
    st.markdown("**Uploaded File:**")
    st.write(uploaded_file_name or "No uploaded file")

    if uploaded_file_type:
        st.markdown("**File Type:**")
        st.write(uploaded_file_type)

    if uploaded_file_size:
        st.markdown("**File Size:**")
        st.write(f"{uploaded_file_size:,} bytes")

if article_text:
    with st.expander("View pasted text"):
        st.write(article_text)

if content_brief:
    st.text_area(
        "Analyzed Content Brief",
        value=content_brief,
        height=280,
        disabled=True
    )
else:
    st.warning("No content analysis found. Please go back to Step 2 and analyze your content first.")

st.divider()


# -----------------------------
# SELECTED PREFERENCES
# -----------------------------
st.subheader("Selected Preferences")

preferences = {
    "Platform": payload.get("platform", "Not provided"),
    "Output Type": payload.get("output_type", "Not provided"),
    "Target Audience": payload.get("target_audience", "Not provided"),
    "Tone": payload.get("tone", "Not provided"),
    "Length": payload.get("length", "Not provided"),
    "Language": payload.get("language", "Not provided")
}

for label, value in preferences.items():
    st.markdown(f"**{label}:** {value}")

st.divider()


# -----------------------------
# NAVIGATION AND GENERATE BUTTON
# -----------------------------
col1, col2, col3 = st.columns([1, 8, 3])

with col1:
    if st.button("← Back"):
        st.session_state.current_step = 3
        st.switch_page("pages/step3_preferences.py")

with col3:
    generate_clicked = st.button("Generate Content", use_container_width=True)


# -----------------------------
# GENERATE CONTENT
# -----------------------------
if generate_clicked:
    missing_fields = []

    if not payload.get("content_brief"):
        missing_fields.append("Content analysis is missing.")

    if not payload.get("platform"):
        missing_fields.append("Platform is missing.")

    if not payload.get("output_type"):
        missing_fields.append("Output type is missing.")

    if not payload.get("target_audience"):
        missing_fields.append("Target audience is missing.")

    if not payload.get("tone"):
        missing_fields.append("Tone is missing.")

    if not payload.get("length"):
        missing_fields.append("Length is missing.")

    if not payload.get("language"):
        missing_fields.append("Language is missing.")

    if missing_fields:
        for error in missing_fields:
            st.error(error)
        st.stop()

    try:
        with st.spinner("Generating final content with Qwen..."):
            generated_content = generate_content_from_payload(payload)

        st.session_state.generated_content = generated_content

        update_payload({
            "generated_content": generated_content
        })

        st.session_state.generation_success_message = True
        st.rerun()

    except Exception as error:
        st.error(f"Failed to generate content: {error}")


# -----------------------------
# SUCCESS MESSAGES
# -----------------------------
if st.session_state.generation_success_message:
    st.success("Content generated successfully!")
    st.session_state.generation_success_message = False

if st.session_state.revision_success_message:
    st.success("Content revised successfully!")
    st.session_state.revision_success_message = False

if st.session_state.image_success_message:
    st.success("Image generated successfully!")
    st.session_state.image_success_message = False


# -----------------------------
# GENERATED CONTENT PREVIEW
# -----------------------------
if st.session_state.generated_content:
    st.subheader("Generated Content")

    st.text_area(
        "Output",
        value=st.session_state.generated_content,
        height=300,
        disabled=True
    )

    copy_to_clipboard_button(
        st.session_state.generated_content,
        "Copy Generated Content"
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Revise Content", use_container_width=True):
            st.session_state.revise_trigger = True
            st.session_state.image_trigger = False

    with col2:
        if st.button("Generate Image", use_container_width=True):
            st.session_state.image_trigger = True
            st.session_state.revise_trigger = False

    with col3:
        if st.button("Start New Content", use_container_width=True):
            st.session_state.new_content_trigger = True


# -----------------------------
# REVISION AREA
# -----------------------------
if st.session_state.revise_trigger:
    st.info("Tell AtomizeAI how you want to revise the generated content.")

    revision_text = st.text_area(
        "Revision Instructions *",
        placeholder="e.g., Make it shorter, more persuasive, and use Taglish.",
        key="revision_instruction_input"
    )

    if st.button("Apply Revision", use_container_width=True):
        if not revision_text.strip():
            st.error("Revision instruction is required.")
            st.stop()

        try:
            with st.spinner("Revising content with Qwen..."):
                update_payload({
                    "revision_instruction": revision_text.strip()
                })

                revised_content = revise_content_from_payload(
                    payload=get_payload(),
                    revision_instruction=revision_text.strip()
                )

                st.session_state.generated_content = revised_content

                update_payload({
                    "generated_content": revised_content,
                    "last_revision_instruction": revision_text.strip()
                })

            st.session_state.revision_success_message = True
            st.rerun()

        except Exception as error:
            st.error(f"Failed to revise content: {error}")


# -----------------------------
# IMAGE GENERATION AREA
# -----------------------------
if st.session_state.image_trigger:
    st.info("Generate an image based on the generated content and selected preferences.")

    if st.button("Run Image Generation", use_container_width=True):
        if not get_payload().get("generated_content"):
            st.error("Generated content is required before generating an image.")
            st.stop()

        try:
            with st.spinner("Generating image prompt and sending workflow to ComfyUI..."):
                image_result = generate_image_from_payload(get_payload())

                image_prompt = image_result["image_prompt"]
                workflow_prompt = image_result["workflow_prompt"]

                update_payload({
                    "image_prompt": image_prompt,
                    "workflow_prompt": workflow_prompt,
                    "generated_images": image_result["images"],
                    "comfyui_prompt_id": image_result["prompt_id"]
                })
            st.session_state.image_success_message = True
            st.rerun()

        except Exception as error:
            st.error(f"Failed to generate image: {error}")


# -----------------------------
# PROMPT SENT TO COMFYUI
# -----------------------------
payload = get_payload()

if payload.get("image_prompt"):
    with st.expander("View prompt sent to ComfyUI", expanded=True):
        st.markdown("**Qwen-generated image prompt**")
        st.code(payload.get("image_prompt"), language="text")

        copy_to_clipboard_button(
            payload.get("image_prompt"),
            "Copy Image Prompt"
        )

        if payload.get("workflow_prompt"):
            st.markdown("**Prompt inserted into ComfyUI workflow node**")
            st.code(payload.get("workflow_prompt"), language="text")


payload = get_payload()

if payload.get("image_prompt"):
    with st.expander("View prompt sent to ComfyUI", expanded=True):
        st.markdown("**Qwen-generated image prompt**")
        st.code(payload.get("image_prompt"), language="text")

        if payload.get("workflow_prompt"):
            st.markdown("**Prompt inserted into ComfyUI workflow node**")
            st.code(payload.get("workflow_prompt"), language="text")
# -----------------------------
# GENERATED IMAGE DISPLAY
# -----------------------------
payload = get_payload()
generated_images = payload.get("generated_images", [])

if generated_images:
    st.subheader("Generated Image")

    for image_data in generated_images:
        try:
            image_bytes = get_image_bytes(image_data)

            st.image(
                image_bytes,
                caption=image_data["filename"],
                use_container_width=True
            )

        except Exception as error:
            st.error(f"Failed to load generated image: {error}")
            st.write(image_data)


# -----------------------------
# START NEW CONTENT
# -----------------------------
if st.session_state.new_content_trigger:
    keys_to_clear = [
        "generate_trigger",
        "revise_trigger",
        "image_trigger",
        "new_content_trigger",
        "generated_content",
        "ai_payload",
        "article_text",
        "uploaded_file",
        "main_topic",
        "keywords",
        "background",
        "key_message",
        "target_audience",
        "repurpose_input_hash",
        "repurpose_analyzed_payload",
        "revision_instruction_input",
        "revision_success_message",
        "generation_success_message",
        "image_success_message"
    ]

    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

    st.session_state.current_step = 1
    st.switch_page("pages/step1_home.py")


# -----------------------------
# DEBUG PAYLOAD
# -----------------------------
with st.expander("Debug payload"):
    st.json(get_payload(), expanded=True)