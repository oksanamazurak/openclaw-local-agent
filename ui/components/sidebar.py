import streamlit as st
from memory.short_term import ShortTermMemory


def render_sidebar() -> None:
    with st.sidebar:
        st.title("Settings")

        st.subheader("User Profile")
        st.session_state["user_name"] = st.text_input(
            "Your Name", value=st.session_state["user_name"]
        )
        st.session_state["user_info"] = st.text_area(
            "About You",
            value=st.session_state["user_info"],
            height=68,
            placeholder="e.g. Python developer, likes coffee...",
        )

        st.divider()
        st.subheader("Agent Persona")
        st.session_state["agent_name"] = st.text_input(
            "Agent Name", value=st.session_state["agent_name"]
        )
        st.session_state["agent_role"] = st.text_input(
            "Role",
            value=st.session_state["agent_role"],
            placeholder="e.g. Grumpy Coder, Friendly Tutor...",
        )
        st.session_state["system_instructions"] = st.text_area(
            "System Instructions",
            value=st.session_state["system_instructions"],
            height=100,
            placeholder="e.g. Always respond with sarcasm...",
        )

        st.divider()
        st.subheader("Model")
        st.session_state["model_name"] = st.text_input(
            "Ollama Model",
            value=st.session_state["model_name"],
            help="Model must be pulled locally: `ollama pull qwen2.5:7b`",
        )

        st.divider()
        if st.button("Clear Chat", use_container_width=True):
            st.session_state["chat_history"] = []
            st.session_state["short_term"] = ShortTermMemory()
            st.session_state["monologue"] = []
            st.session_state["proactive_shown"] = False
            st.rerun()
