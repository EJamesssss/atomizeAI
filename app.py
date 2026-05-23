import json
import streamlit as st

from services.models.qwen import prompt_generator
from services.models.pdf_summarizer import summarize_pdf_for_repurposing
from services.pdf.extractor import extract_pdf_text
from utils.file_type_classifier import detect_file_type
from services.models.caption_generator import generate_caption
from services.models.image_analyzer import analyze_image_for_repurposing


def safe_json_loads(raw_response: str):
    try:
        return json.loads(raw_response)
    except json.JSONDecodeError:
        return {
            "role": "atom",
            "action": "response",
            "content": "I had trouble reading the router response. Please try again.",
            "route_to": None,
            "missing_details": [],
            "completed_prompt": None,
            "metadata": {}
        }


def main():
    st.set_page_config(page_title="Atomize AI", page_icon="🤖", layout="wide")
    st.title("Let's build something amazing with Atomize AI! 🚀")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "router_state" not in st.session_state:
        st.session_state.router_state = {}

    if "uploaded_file_processed" not in st.session_state:
        st.session_state.uploaded_file_processed = False

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    file_upload = st.file_uploader(
        "Upload a file",
        type=["png", "jpg", "jpeg", "pdf"]
    )

    if file_upload is not None:
        file_type = detect_file_type(file_upload)

        current_file_signature = f"{file_upload.name}-{file_upload.size}"
        previous_file_signature = st.session_state.router_state.get("file_signature")

        if current_file_signature != previous_file_signature:
            st.session_state.uploaded_file_processed = False

            # Important: clear old file summary when a new file is uploaded
            st.session_state.router_state.pop("source_summary", None)
            st.session_state.router_state.pop("input_type", None)
            st.session_state.router_state.pop("pdf_extract_status", None)
            st.session_state.router_state.pop("image_analysis_status", None)

        st.session_state.router_state["uploaded_file"] = {
            "file_name": file_upload.name,
            "file_type": file_type,
            "file_size": file_upload.size,
        }

        st.session_state.router_state["file_signature"] = current_file_signature

        st.markdown(
            f"Uploaded file: **{file_upload.name}** "
            f"({file_type}, {file_upload.size} bytes)"
        )

        if file_type == "pdf" and not st.session_state.uploaded_file_processed:
            with st.spinner("Reading and summarizing PDF..."):
                pdf_text = extract_pdf_text(file_upload)

                if not pdf_text:
                    st.warning(
                        "I could not extract readable text from this PDF. "
                        "It may be scanned or image-based."
                    )
                    st.session_state.router_state["pdf_extract_status"] = "no_text_found"
                else:
                    st.session_state.router_state["pdf_extract_status"] = "text_extracted"
                    st.session_state.router_state["pdf_text_preview"] = pdf_text[:1000]

                    pdf_summary = summarize_pdf_for_repurposing(
                        pdf_text=pdf_text,
                        router_state=st.session_state.router_state,
                    )

                    st.session_state.router_state["source_summary"] = pdf_summary
                    st.session_state.router_state["input_type"] = "pdf"

                    st.session_state.uploaded_file_processed = True

                    with st.expander("PDF summary preview"):
                        st.markdown(pdf_summary)

        elif file_type == "image" and not st.session_state.uploaded_file_processed:
            st.image(file_upload, caption="Uploaded image", use_container_width=True)

            with st.spinner("Analyzing image..."):
                image_summary = analyze_image_for_repurposing(
                    uploaded_file=file_upload,
                    router_state=st.session_state.router_state
                )

                st.session_state.router_state["source_summary"] = image_summary
                st.session_state.router_state["input_type"] = "photo"
                st.session_state.router_state["image_analysis_status"] = "analyzed"

                st.session_state.uploaded_file_processed = True

                with st.expander("Image analysis preview"):
                    st.markdown(image_summary)

        elif file_type == "image":
            st.image(file_upload, caption="Uploaded image", use_container_width=True)

        

    user_input = st.chat_input("What do you want to do?")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking ..."):
                response = prompt_generator(
                    st.session_state.messages,
                    st.session_state.router_state
                )

                raw_response = response["message"]["content"]
                parsed_response = json.loads(raw_response)

                assistant_message = parsed_response["content"]
                st.markdown(assistant_message)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_message
                })

                metadata = parsed_response.get("metadata", {})

                st.session_state.router_state.update({
                    key: value
                    for key, value in metadata.items()
                    if value is not None
                })

                if parsed_response.get("action") == "route":
                    route_to = parsed_response.get("route_to")
                    completed_prompt = parsed_response.get("completed_prompt")

                    if route_to == "caption_generator":
                        with st.spinner("Generating caption..."):
                            final_caption = generate_caption(completed_prompt)

                        st.markdown("### Generated Caption")
                        st.markdown(final_caption)

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": final_caption
                        })

                st.markdown(st.session_state.router_state)
                st.markdown("---")
                st.markdown(raw_response)


if __name__ == "__main__":
    main()