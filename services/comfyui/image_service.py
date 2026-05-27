from services.models.image_prompt_generator import generate_image_prompt_from_payload
from services.comfyui.workflow_builder import build_image_workflow
from services.comfyui.client import (
    queue_prompt,
    wait_for_completion,
    extract_generated_images
)


def generate_image_from_payload(payload: dict) -> dict:
    image_prompt = generate_image_prompt_from_payload(payload)

    if not image_prompt or not image_prompt.strip():
        raise ValueError("Image prompt generator returned an empty prompt.")

    workflow = build_image_workflow(
        prompt_text=image_prompt,
        filename_prefix="atomizeai-image",
        width=1024,
        height=1024
    )

    workflow_prompt = workflow["57:27"]["inputs"]["text"]

    if not workflow_prompt or not workflow_prompt.strip():
        raise ValueError("Workflow prompt is empty before sending to ComfyUI.")

    print("[DEBUG] Image prompt generated:")
    print(image_prompt)

    print("[DEBUG] Prompt inserted into ComfyUI workflow:")
    print(workflow_prompt)

    prompt_id = queue_prompt(workflow)
    history_item = wait_for_completion(prompt_id)
    images = extract_generated_images(history_item)

    return {
        "image_prompt": image_prompt,
        "workflow_prompt": workflow_prompt,
        "prompt_id": prompt_id,
        "images": images
    }