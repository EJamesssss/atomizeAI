from services.extractors.file_text_extractor import extract_text_from_uploaded_file
from services.models.content_summarizer import summarize_content_for_repurposing
from services.models.image_analyzer import analyze_image_for_repurposing


IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png"]
DOCUMENT_EXTENSIONS = [".pdf", ".docx", ".txt"]


def is_image_file(uploaded_file):
    file_name = uploaded_file.name.lower()
    return any(file_name.endswith(ext) for ext in IMAGE_EXTENSIONS)


def is_document_file(uploaded_file):
    file_name = uploaded_file.name.lower()
    return any(file_name.endswith(ext) for ext in DOCUMENT_EXTENSIONS)


def analyze_repurpose_input(
    article_text: str = "",
    uploaded_file=None,
    router_state: dict | None = None
) -> dict:
    router_state = router_state or {}
    article_text = article_text.strip() if article_text else ""

    if not article_text and uploaded_file is None:
        raise ValueError("Please paste content or upload a file before proceeding.")

    uploaded_file_name = uploaded_file.name if uploaded_file else None
    uploaded_file_type = uploaded_file.type if uploaded_file else None
    uploaded_file_size = uploaded_file.size if uploaded_file else None

    # -----------------------------
    # IMAGE FILE
    # -----------------------------
    if uploaded_file is not None and is_image_file(uploaded_file):
        image_brief = analyze_image_for_repurposing(
            uploaded_file=uploaded_file,
            router_state=router_state
        )

        return {
            "content_path": "repurpose",
            "source_type": "text_and_image" if article_text else "image",
            "article_text": article_text if article_text else None,
            "uploaded_file_name": uploaded_file_name,
            "uploaded_file_type": uploaded_file_type,
            "uploaded_file_size": uploaded_file_size,
            "extracted_text": article_text if article_text else "",
            "content_brief": image_brief
        }

    # -----------------------------
    # DOCUMENT FILE
    # -----------------------------
    extracted_file_text = ""

    if uploaded_file is not None:
        if not is_document_file(uploaded_file):
            raise ValueError("Unsupported file type. Please upload PDF, DOCX, TXT, JPG, JPEG, or PNG.")

        extracted_file_text = extract_text_from_uploaded_file(uploaded_file)

        if not extracted_file_text or not extracted_file_text.strip():
            raise ValueError(
                "No readable text was extracted from the uploaded file. "
                "Please upload a text-based PDF, DOCX, TXT file, or paste the content manually."
            )

    # -----------------------------
    # COMBINE TEXT
    # -----------------------------
    if article_text and extracted_file_text:
        source_type = "text_and_file"
        combined_text = f"""
PASTED TEXT:
{article_text}

UPLOADED FILE CONTENT:
{extracted_file_text}
"""
    elif article_text:
        source_type = "text"
        combined_text = article_text
    else:
        source_type = "file"
        combined_text = extracted_file_text

    if not combined_text or not combined_text.strip():
        raise ValueError("No content found to analyze.")

    content_brief = summarize_content_for_repurposing(
        content_text=combined_text,
        router_state=router_state,
        source_type=source_type
    )

    if not content_brief or not content_brief.strip():
        raise ValueError("The content analyzer returned an empty analysis.")

    return {
        "content_path": "repurpose",
        "source_type": source_type,
        "article_text": article_text if article_text else None,
        "uploaded_file_name": uploaded_file_name,
        "uploaded_file_type": uploaded_file_type,
        "uploaded_file_size": uploaded_file_size,
        "extracted_text": combined_text,
        "content_brief": content_brief
    }