import copy
import json
import random
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
WORKFLOW_TEMPLATE_PATH = BASE_DIR / "workflows" / "image_z_image_turbo.json"


def load_workflow_template():
    print("Workflow path:", WORKFLOW_TEMPLATE_PATH)
    print("Exists:", WORKFLOW_TEMPLATE_PATH.exists())

    with open(WORKFLOW_TEMPLATE_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def build_image_workflow(
    prompt_text: str,
    filename_prefix: str = "atomizeai-image",
    width: int = 1024,
    height: int = 1024
):
    workflow = load_workflow_template()
    workflow = copy.deepcopy(workflow)

    # Prompt node
    workflow["57:27"]["inputs"]["text"] = prompt_text

    # Size node
    workflow["57:13"]["inputs"]["width"] = width
    workflow["57:13"]["inputs"]["height"] = height

    # Save image node
    workflow["9"]["inputs"]["filename_prefix"] = filename_prefix

    # Random seed per generation
    workflow["57:3"]["inputs"]["seed"] = random.randint(1, 999999999999999)

    return workflow