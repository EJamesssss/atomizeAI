import ollama


MODEL_NAME = "qwen3:14b"


def summarize_pdf_for_repurposing(pdf_text: str, router_state: dict) -> str:
    """
    Converts raw PDF text into a clean content brief for repurposing.
    """

    system_prompt = """
You are a PDF content analysis assistant for a content repurposing application.

Your job is to read extracted PDF text and convert it into a clean content brief.

Do not create the final caption yet.
Do not create the final social media post yet.

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

PDF CONTENT:
{pdf_text[:30000]}

TASK:
Summarize this PDF so it can be repurposed into social media content based on the user's preferences.
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response["message"]["content"]