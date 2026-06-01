import time
import uuid
import requests
from urllib.parse import urlencode


COMFYUI_BASE_URL = "http://127.0.0.1:8188"


def queue_prompt(workflow: dict) -> str:
    client_id = str(uuid.uuid4())

    response = requests.post(
        f"{COMFYUI_BASE_URL}/prompt",
        json={
            "prompt": workflow,
            "client_id": client_id
        },
        timeout=60
    )

    response.raise_for_status()
    data = response.json()

    return data["prompt_id"]


def get_history(prompt_id: str) -> dict:
    response = requests.get(
        f"{COMFYUI_BASE_URL}/history/{prompt_id}",
        timeout=60
    )

    response.raise_for_status()
    return response.json()


def wait_for_completion(prompt_id: str, max_wait_seconds: int = 300):
    start_time = time.time()

    while time.time() - start_time < max_wait_seconds:
        history = get_history(prompt_id)

        if prompt_id in history:
            return history[prompt_id]

        time.sleep(2)

    raise TimeoutError("ComfyUI image generation timed out.")


def extract_generated_images(history_item: dict):
    images = []

    outputs = history_item.get("outputs", {})

    for node_id, output in outputs.items():
        for image in output.get("images", []):
            filename = image.get("filename")
            subfolder = image.get("subfolder", "")
            image_type = image.get("type", "output")

            if filename:
                images.append({
                    "filename": filename,
                    "subfolder": subfolder,
                    "type": image_type
                })

    return images


def get_image_bytes(image_data: dict) -> bytes:
    params = {
        "filename": image_data["filename"],
        "subfolder": image_data.get("subfolder", ""),
        "type": image_data.get("type", "output")
    }

    response = requests.get(
        f"{COMFYUI_BASE_URL}/view?{urlencode(params)}",
        timeout=60
    )

    response.raise_for_status()
    return response.content