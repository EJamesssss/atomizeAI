from services.extractors.file_text_extractor import extract_text_from_uploaded_file
from services.models.content_summarizer import summarize_content_for_repurposing


def analyze_repurpose_input(
    article_text: str = "",
    uploaded_file=None,
    router_state: dict | None = None
) -> dict:
    """
    Builds the Step 2 repurpose payload.

    Accepts:
    - pasted text only
    - uploaded file only
    - pasted text + uploaded file
    """

    router_state = router_state or {}
    article_text = article_text.strip() if article_text else ""

    if not article_text and uploaded_file is None:
        raise ValueError("Please paste content or upload a file before proceeding.")

    extracted_file_text = ""
    uploaded_file_name = None
    uploaded_file_type = None
    uploaded_file_size = None

    if uploaded_file is not None:
        extracted_file_text = extract_text_from_uploaded_file(uploaded_file)
        uploaded_file_name = uploaded_file.name
        uploaded_file_type = uploaded_file.type
        uploaded_file_size = uploaded_file.size

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

    content_brief = summarize_content_for_repurposing(
        content_text=combined_text,
        router_state=router_state,
        source_type=source_type
    )

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