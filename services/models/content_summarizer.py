import ollama


MODEL_NAME = "qwen3:14b"


def summarize_content_for_repurposing(
    content_text: str,
    router_state: dict | None = None,
    source_type: str = "text"
) -> str:
    """
    Converts raw text from pasted content, PDF, DOCX, or TXT into a clean content brief.
    """

    router_state = router_state or {}

    if not content_text or not content_text.strip():
        raise ValueError("No content found to summarize.")

    system_prompt = """
You are a content analysis assistant for a content repurposing application.

Your job is to read provided content and convert it into a clean content brief.

The content may come from pasted text, a PDF, a DOCX file, or a TXT file.

Do not create the final caption yet.
Do not create the final social media post yet.
Do not create the final output yet.

Return a structured summary that will help another model repurpose the content.

Include:
1. Main topic
2. Key message
3. Important details
4. Useful quotes or phrases, if any
5. Target audience clues
6. Suggested content angles
7. Suggested social media hook ideas
8. What should be avoided or not misrepresented

Be concise but complete.
"""

    user_prompt = f"""
USER PREFERENCES / ROUTER STATE:
{router_state}

SOURCE TYPE:
{source_type}

CONTENT:
{content_text[:30000]}

TASK:
Summarize this content so it can be repurposed based on the user's preferences.
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response["message"]["content"]