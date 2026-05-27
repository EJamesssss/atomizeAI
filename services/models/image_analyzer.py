import os
import tempfile
import time
import ollama

from utils.settings import DEBUG_MODE


VISION_MODEL_NAME = "qwen2.5vl:7b"
DEBUG_ANALYZER = DEBUG_MODE


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
You are an image analysis assistant.

Your job is to describe and extract only the visible information from the uploaded image.

Do not create captions.
Do not create hooks.
Do not suggest content angles.
Do not infer target audience unless explicitly visible.
Do not generate marketing copy.

Return only this format:

Image summary:
Main visible subject:
Visible text:
Important visual details:
Products, brands, or names visible:
Colors, layout, or design notes:
Missing or unclear information:
"""

        user_prompt = """
Analyze this image and return only the visible source information.
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
                "temperature": 0.1,
                "num_predict": 350
            }
        )

        debug_print("Qwen2.5-VL image analysis completed", ollama_start)
        debug_print("Total image analyzer duration", total_start)

        return response["message"]["content"]

    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)