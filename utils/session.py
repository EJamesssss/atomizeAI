import streamlit as st

def init_payload():
  if "ai_payload" not in st.session_state:
    st.session_state.ai_payload = {}

def update_payload(data: dict):
    init_payload()
    st.session_state.ai_payload.update(data)


def get_payload():
    init_payload()
    return st.session_state.ai_payload