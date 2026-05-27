import time
import ollama


MODEL_NAME = "qwen3:8b"
DEBUG_GENERATOR = True


def debug_print(label, start_time):
    if DEBUG_GENERATOR:
        elapsed = time.perf_counter() - start_time
        print(f"[DEBUG] {label}: {elapsed:.2f} seconds")


def generate_content_from_payload(payload: dict) -> str:
    total_start = time.perf_counter()

    content_brief = payload.get("content_brief", "")
    platform = payload.get("platform", "")
    output_type = payload.get("output_type", "")
    target_audience = payload.get("target_audience", "")
    tone = payload.get("tone", "")
    length = payload.get("length", "")
    language = payload.get("language", "")

    if not content_brief:
        raise ValueError("Content brief is missing.")

    if not output_type:
        raise ValueError("Output type is missing.")

    system_prompt = """
You are AtomizeAI, a content generation assistant.

Your job is to create the user's selected content output based on:
- analyzed source content
- selected platform
- selected output type
- target audience
- tone
- length
- language

Do not explain your process.
Do not mention that you are an AI.
Return only the final generated content.
"""

    user_prompt = f"""
CONTENT ANALYSIS:
{content_brief}

USER PREFERENCES:
Platform: {platform}
Output Type: {output_type}
Target Audience: {target_audience}
Tone: {tone}
Length: {length}
Language: {language}

TASK:
Generate a {output_type} for {platform}.

Follow these rules:
1. Match the selected output type exactly.
2. Use the selected tone.
3. Write for the selected target audience.
4. Use the selected language.
5. Respect the selected length.
6. Base the content only on the content analysis.
7. Do not invent unsupported facts, offers, prices, or product claims.
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
            "temperature": 0.7,
            "num_predict": 700
        }
    )

    debug_print("Ollama generation completed", ollama_start)
    debug_print("Total generator duration", total_start)

    return response["message"]["content"]