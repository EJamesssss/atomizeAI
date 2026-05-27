import ollama


MODEL_NAME = "qwen3:8b"

import time

### DEBUGGER

DEBUG_ANALYZER = True


def debug_print(label, start_time):
    if DEBUG_ANALYZER:
        elapsed = time.perf_counter() - start_time
        print(f"[DEBUG] {label}: {elapsed:.2f} seconds")


### DEBUGGER ends here

def summarize_content_for_repurposing(
    content_text: str,
    router_state: dict | None = None,
    source_type: str = "text"
) -> str:
    total_start = time.perf_counter()

    router_state = router_state or {}

    if not content_text or not content_text.strip():
        raise ValueError("No content found to summarize.")

    max_chars = 12000
    trimmed_content = content_text[:max_chars]

    debug_print(f"Content trimmed from {len(content_text)} to {len(trimmed_content)} chars", total_start)

    system_prompt = """
You are a content analysis assistant for a content repurposing application.

Your job is to read provided content and convert it into a clean content brief.

Do not create the final caption yet.
Do not create the final social media post yet.
Do not create the final output yet.

Return a structured summary with:
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
{trimmed_content}

TASK:
Summarize this content so it can be repurposed based on the user's preferences.
"""

    prompt_start = time.perf_counter()
    debug_print(f"Prompt built ({len(user_prompt)} chars)", prompt_start)

    ollama_start = time.perf_counter()

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        options={
            "temperature": 0.2,
            "num_predict": 700
        }
    )

    debug_print("Ollama chat completed", ollama_start)
    debug_print("Total summarizer duration", total_start)

    return response["message"]["content"]