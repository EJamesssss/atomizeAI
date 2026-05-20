import streamlit as st
from services.models.qwen import prompt_generator
import json

def main():
    st.set_page_config(page_title="Atomize AI", page_icon="🤖", layout="wide")
    st.title("Let's build something amazing with Atomize AI! 🚀")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "router_state" not in st.session_state:
        st.session_state.router_state = {}

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("What do you want to do?")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant"):
          with st.spinner("Thinking ..."):
              response = prompt_generator(st.session_state.messages, st.session_state.router_state)
              raw_response = response["message"]["content"]
              parsed_response = json.loads(raw_response)

              assistant_message = parsed_response["content"]
              st.markdown(assistant_message)
              st.session_state.messages.append({"role": "assistant", "content": assistant_message})

              metadata = parsed_response.get("metadata", {})

              st.session_state.router_state.update({
                  key: value
                  for key, value in metadata.items()
                  if value is not None
              })

              st.markdown(st.session_state.router_state)
              st.markdown("---")
              st.markdown(raw_response)

if __name__ == "__main__":    main()