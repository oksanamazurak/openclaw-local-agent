
import streamlit as st
from core.agent import run_agent, check_proactive_tasks
from tools.todo_manager import load_todos_for_ui
from ui.session import get_long_term, get_persona
from ui.components.todo_board import render_todo_board


def _maybe_show_proactive_suggestion() -> None:
    if st.session_state["proactive_shown"]:
        return

    todos = load_todos_for_ui()
    pending = [t for t in todos if not t.get("done")]
    if pending:
        with st.spinner("Checking tasks..."):
            suggestion = check_proactive_tasks(
                todos, get_persona(), st.session_state["model_name"]
            )
        if suggestion:
            st.session_state["chat_history"].append(
                {"role": "assistant", "content": suggestion}
            )

    st.session_state["proactive_shown"] = True


def _render_chat_history() -> None:
    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])


def render_agent_page() -> None:
    agent_name = st.session_state["agent_name"]

    col_chat, col_todo = st.columns([3, 1])

    with col_todo:
        render_todo_board()

    with col_chat:
        st.markdown(f"### {agent_name}")
        _maybe_show_proactive_suggestion()
        _render_chat_history()

        if "pending_input" in st.session_state:
            pending = st.session_state.pop("pending_input")
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    ltm = get_long_term()
                    try:
                        response, monologue = run_agent(
                            user_input=pending,
                            persona=get_persona(),
                            short_term=st.session_state["short_term"],
                            long_term=ltm,
                            model_name=st.session_state["model_name"],
                            monologue=st.session_state.get("monologue", []),
                        )
                        st.session_state["monologue"] = monologue
                    except Exception as e:
                        response = f"Error: {e}"
            st.session_state["chat_history"].append({"role": "assistant", "content": response})
            st.rerun()

        user_input = st.chat_input(f"Message {agent_name}...")
        if user_input:
            st.session_state["chat_history"].append({"role": "user", "content": user_input})
            st.session_state["pending_input"] = user_input
            st.rerun()
