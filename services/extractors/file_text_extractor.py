from io import BytesIO

from pypdf import PdfReader
from docx import Document


def extract_text_from_uploaded_file(uploaded_file) -> str:
    """
    Extract text from an uploaded Streamlit file.

    Supported:
    - PDF
    - DOCX
    - TXT
    """

    if uploaded_file is None:
        raise ValueError("No file uploaded.")

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)

    if file_name.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)

    if file_name.endswith(".txt"):
        return extract_text_from_txt(uploaded_file)

    raise ValueError("Unsupported file type. Please upload PDF, DOCX, or TXT.")


def extract_text_from_pdf(uploaded_file) -> str:
    pdf_bytes = uploaded_file.getvalue()
    reader = PdfReader(BytesIO(pdf_bytes))

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text and text.strip():
            pages.append(text.strip())

    return "\n\n".join(pages)


def extract_text_from_docx(uploaded_file) -> str:
    docx_bytes = uploaded_file.getvalue()
    document = Document(BytesIO(docx_bytes))

    paragraphs = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    return "\n\n".join(paragraphs)


def extract_text_from_txt(uploaded_file) -> str:
    return uploaded_file.getvalue().decode("utf-8", errors="ignore")