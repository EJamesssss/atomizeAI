import ollama

from utils.settings import DEBUG_MODE


MODEL_NAME = "qwen3:8b"
DEBUG_ANALYZER = DEBUG_MODE


def debug_print(message):
    if DEBUG_ANALYZER:
        print(f"[CONTENT ANALYZER DEBUG] {message}")


def clean_analysis_response(text: str) -> str:
    if not text:
        return ""

    text = text.strip()

    if "</think>" in text:
        text = text.split("</think>")[-1].strip()

    text = text.replace("Analysis:", "").strip()

    return text


def build_fallback_analysis(content_text: str, source_type: str) -> str:
    preview = content_text[:1200].strip()

    return f"""
Content summary:
The uploaded {source_type} contains readable content, but the AI analyzer returned an empty response.

Main topic:
Needs manual review from extracted content.

Key message or purpose:
Needs manual review from extracted content.

Important details:
{preview}

Notable phrases or exact wording:
See important details above.

Facts, offers, products, or names mentioned:
Needs manual review.

Missing or unclear information:
The analyzer response was empty, so this is a fallback brief.
""".strip()


def summarize_content_for_repurposing(
    content_text: str,
    router_state: dict | None = None,
    source_type: str = "text"
) -> str:
    router_state = router_state or {}

    if not content_text or not content_text.strip():
        raise ValueError("No content found to summarize.")

    max_chars = 6000
    trimmed_content = content_text[:max_chars]

    system_prompt = """
You are a content analysis assistant.

Analyze the provided content and extract only the important source information.

Do not create captions.
Do not create hooks.
Do not suggest content angles.
Do not generate marketing copy.

Return a visible response only.
Return exactly this format:

Content summary:
Main topic:
Key message or purpose:
Important details:
Notable phrases or exact wording:
Facts, offers, products, or names mentioned:
Missing or unclear information:
"""

    user_prompt = f"""
/no_think

Source type:
{source_type}

Content:
{trimmed_content}

Task:
Analyze the content and return the structured source information.
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        options={
            "temperature": 0.1,
            "num_predict": 450
        }
    )

    debug_print(f"Raw Ollama response: {response}")

    analysis = response.get("message", {}).get("content", "")
    analysis = clean_analysis_response(analysis)

    debug_print(f"Cleaned analysis: {analysis}")

    if not analysis:
        debug_print("Analyzer returned empty response. Using fallback analysis.")
        analysis = build_fallback_analysis(trimmed_content, source_type)

    return analysis