import json
import streamlit as st


def copy_to_clipboard_button(text: str, button_label: str = "Copy Generated Content"):
    safe_text = json.dumps(text)

    st.iframe(
        f"""
        <button
            onclick='copyText()'
            style="
                width: 100%;
                padding: 10px 16px;
                border-radius: 8px;
                border: 1px solid #444;
                background-color: transparent;
                color: white;
                cursor: pointer;
                font-size: 14px;
            "
        >
            {button_label}
        </button>

        <script>
            function copyText() {{
                const text = {safe_text};
                navigator.clipboard.writeText(text).then(function() {{
                    const button = document.querySelector("button");
                    const originalText = button.innerText;

                    button.innerText = "Copied!";
                    setTimeout(function() {{
                        button.innerText = originalText;
                    }}, 1500);
                }});
            }}
        </script>
        """,
        height=50
    )