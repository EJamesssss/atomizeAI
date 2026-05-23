import ollama


MODEL_NAME = "qwen3:14b"


def generate_caption(completed_prompt: str) -> str:
    system_prompt = """
You are an expert social media content repurposing assistant.

You create final social media captions based on a completed prompt.

Follow the requested platform, tone, language, CTA, audience, and length.

Return only the final content.
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": completed_prompt},
        ],
    )

    return response["message"]["content"]