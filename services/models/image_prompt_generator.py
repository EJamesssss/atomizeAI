import ollama

from utils.settings import DEBUG_MODE

MODEL_NAME = "qwen3:8b"
DEBUG_IMAGE_PROMPT = DEBUG_MODE


def debug_print(message):
    if DEBUG_IMAGE_PROMPT:
        print(f"[IMAGE PROMPT DEBUG] {message}")


def build_fallback_image_prompt(payload: dict) -> str:
    content_brief = payload.get("content_brief", "")
    target_audience = payload.get("target_audience", "")
    tone = payload.get("tone", "")

    return f"""
{content_brief}

Create a realistic, visually clear image based on the main subject and important visual details above.
Dynamic composition, natural lighting, clear subject focus, high-quality image, suitable for {target_audience}, {tone} mood.
""".strip()


def clean_prompt(prompt: str) -> str:
    if not prompt:
        return ""

    prompt = prompt.strip()

    # Remove common model wrappers if any
    prompt = prompt.replace("Prompt:", "").replace("Image prompt:", "").strip()

    # Remove Qwen thinking tags if present
    if "</think>" in prompt:
        prompt = prompt.split("</think>")[-1].strip()

    return prompt


def generate_image_prompt_from_payload(payload: dict) -> str:
    content_brief = payload.get("content_brief", "")
    source_type = payload.get("source_type", "")
    generated_content = payload.get("generated_content", "")
    target_audience = payload.get("target_audience", "")
    tone = payload.get("tone", "")

    if not content_brief:
        raise ValueError("Content brief is missing.")

    system_prompt = """
You are an image prompt writer for ComfyUI.

Convert analyzed content into one short, concrete image-generation prompt.

Write in this format:
[main subject], [important visible details], [background/environment]. [lighting], [color mood], [camera framing or visual style].

Good example:
Latina female with thick wavy hair, harbor boats and pastel houses behind. Breezy seaside light, warm tones, cinematic close-up.

Rules:
- Return only the final prompt.
- Do not explain.
- Do not use bullet points.
- Do not use labels.
- Do not write captions, slogans, hashtags, or CTA.
- Focus only on what should be visible in the image.
- Keep it concise and visual.
"""

    user_prompt = f"""
/no_think

SOURCE TYPE:
{source_type}

ANALYZED CONTENT:
{content_brief}

GENERATED CONTENT:
{generated_content}

USER PREFERENCES:
Target Audience: {target_audience}
Tone: {tone}

TASK:
Create one visually descriptive image prompt for ComfyUI.

Prioritize the analyzed content over the generated caption.

Example style:
Latina female with thick wavy hair, harbor boats and pastel houses behind. Breezy seaside light, warm tones, cinematic close-up.
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        options={
            "temperature": 0.4,
            "num_predict": 180
        }
    )

    debug_print(f"Raw Ollama response: {response}")

    prompt = response.get("message", {}).get("content", "")
    prompt = clean_prompt(prompt)

    debug_print(f"Cleaned prompt: {prompt}")

    if not prompt:
        debug_print("Qwen returned empty prompt. Using fallback prompt.")
        prompt = build_fallback_image_prompt(payload)

    if not prompt:
        raise ValueError("Image prompt generator returned an empty prompt.")

    return prompt