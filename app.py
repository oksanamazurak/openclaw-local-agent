import streamlit as st

st.set_page_config(
    page_title="OpenClaw Agent",
    layout="wide",
    initial_sidebar_state="expanded",
)

from ui.session import init_session
from ui.components.sidebar import render_sidebar
from ui.page_agent import render_agent_page
from ui.page_debug import render_debug_page

init_session()
render_sidebar()

page = st.radio(
    "Navigate",
    ["Agent Interface", "Under the Hood"],
    horizontal=True,
    label_visibility="collapsed",
)

if page == "Agent Interface":
    render_agent_page()
elif page == "Under the Hood":
    render_debug_page()
