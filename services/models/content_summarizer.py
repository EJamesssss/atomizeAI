import time
import ollama


MODEL_NAME = "qwen2.5:7b"
DEBUG_ANALYZER = True


def debug_print(label, start_time):
    if DEBUG_ANALYZER:
        elapsed = time.perf_counter() - start_time
        print(f"[DEBUG] {label}: {elapsed:.2f} seconds")


def summarize_content_for_repurposing(
    content_text: str,
    router_state: dict | None = None,
    source_type: str = "text"
) -> str:
    total_start = time.perf_counter()

    router_state = router_state or {}

    if not content_text or not content_text.strip():
        raise ValueError("No content found to summarize.")

    max_chars = 6000
    trimmed_content = content_text[:max_chars]

    debug_print(
        f"Content trimmed from {len(content_text)} to {len(trimmed_content)} chars",
        total_start
    )

    system_prompt = """
You are a content analysis assistant.

Your job is to analyze the provided content and extract only the important source information.

Do not create captions.
Do not create hooks.
Do not suggest content angles.
Do not infer target audience unless explicitly stated.
Do not generate marketing copy.

Return only this format:

Content summary:
Main topic:
Key message or purpose:
Important details:
Notable phrases or exact wording:
Facts, offers, products, or names mentioned:
Missing or unclear information:
"""

    user_prompt = f"""
Source type:
{source_type}

Content:
{trimmed_content}

Analyze the content and return only the source information.
"""

    debug_print(f"Prompt built ({len(user_prompt)} chars)", total_start)

    ollama_start = time.perf_counter()

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        options={
            "temperature": 0.1,
            "num_predict": 350
        }
    )

    debug_print("Ollama chat completed", ollama_start)
    debug_print("Total summarizer duration", total_start)

    return response["message"]["content"]