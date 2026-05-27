import os
import tempfile
import time
import ollama


VISION_MODEL_NAME = "qwen2.5vl:7b"
DEBUG_ANALYZER = True


def debug_print(label, start_time):
    if DEBUG_ANALYZER:
        elapsed = time.perf_counter() - start_time
        print(f"[DEBUG] {label}: {elapsed:.2f} seconds")


def analyze_image_for_repurposing(uploaded_file, router_state=None) -> str:
    router_state = router_state or {}
    total_start = time.perf_counter()

    suffix = os.path.splitext(uploaded_file.name)[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(uploaded_file.getvalue())
        temp_file_path = temp_file.name

    debug_print("Image saved to temp file", total_start)

    try:
        system_prompt = """
You are an image analysis assistant for a content repurposing application.

Analyze the uploaded image and create a concise content brief.

Do not create the final caption.
Do not create the final social media post.

Return only this format:

Visible elements:
Main subject:
Text visible in image:
Brand/product clues:
Possible message:
Target audience clues:
Suggested content angles:
Suggested hook ideas:
Avoid / do not misrepresent:
"""

        user_prompt = f"""
Router state:
{router_state}

Analyze this image for content repurposing.
"""

        ollama_start = time.perf_counter()

        response = ollama.chat(
            model=VISION_MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt,
                    "images": [temp_file_path]
                }
            ],
            options={
                "temperature": 0.2,
                "num_predict": 400
            }
        )

        debug_print("Qwen2.5-VL image analysis completed", ollama_start)
        debug_print("Total image analyzer duration", total_start)

        return response["message"]["content"]

    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)