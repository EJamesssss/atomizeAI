import base64
import ollama


MODEL_NAME = "qwen2.5vl:7b"


def analyze_image_for_repurposing(uploaded_file, router_state: dict) -> str:
    """
    Analyze an uploaded image and return a content brief for repurposing.
    """

    uploaded_file.seek(0)
    image_bytes = uploaded_file.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    system_prompt = """
You are an image analysis assistant for a content repurposing application.

Your job is to analyze the uploaded image and convert it into a useful content brief.

Do not write the final caption yet.
Do not create an image prompt yet.

Return a structured image summary that can help another model create a social media caption.

Include:
1. Main subject
2. Visible objects or products
3. Scene or environment
4. Mood or emotion
5. Possible marketing angle
6. Suggested caption hooks
7. Important visual details to mention
8. What should not be assumed
"""

    user_prompt = f"""
USER PREFERENCES / ROUTER STATE:
{router_state}

TASK:
Analyze this uploaded image for social media content repurposing.
Create a clear image summary that can be used to generate a caption based on the user's platform, tone, goal, language, CTA, and length preferences.
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
                "images": [image_base64],
            },
        ],
    )

    return response["message"]["content"]