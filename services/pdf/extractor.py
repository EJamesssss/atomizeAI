import fitz


def extract_pdf_text(uploaded_file) -> str:
    """
    Extract text from a PDF uploaded.
    """
    uploaded_file.seek(0)
    pdf_bytes = uploaded_file.read()

    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    pages = []

    for page_index, page in enumerate(doc, start=1):
        text = page.get_text("text").strip()

        if text:
            pages.append(f"\n--- Page {page_index} ---\n{text}")

    return "\n".join(pages).strip()