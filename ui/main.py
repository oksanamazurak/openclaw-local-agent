"""
OpenClaw — Streamlit entry point.
"""

import streamlit as st

st.set_page_config(
    page_title="OpenClaw Agent",
    layout="wide",
    initial_sidebar_state="expanded",
)

from ui.session import init_session
from ui.components.sidebar import render_sidebar
from ui.components.todo_board import render_todo_board
from ui.components.chat import render_chat
from ui.components.debug import render_debug_page

init_session()
render_sidebar()

page = st.radio(
    "Navigate",
    ["Agent Interface", "Under the Hood"],
    horizontal=True,
    label_visibility="collapsed",
)

if page == "Agent Interface":
    col_chat, col_todo = st.columns([3, 1])
    with col_todo:
        render_todo_board()
    with col_chat:
        render_chat()

elif page == "Under the Hood":
    render_debug_page()