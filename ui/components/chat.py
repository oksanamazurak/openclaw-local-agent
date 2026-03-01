
import streamlit as st
from backend.agent import run_agent, check_proactive_tasks
from backend.tools import load_todos_for_ui
from ui.session import get_long_term, get_persona


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


def _render_history() -> None:
    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])


def _handle_user_input() -> None:
    agent_name = st.session_state["agent_name"]
    user_input = st.chat_input(f"Message {agent_name}...")
    if not user_input:
        return

    st.session_state["chat_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    ltm = get_long_term()
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response, monologue = run_agent(
                    user_input=user_input,
                    persona=get_persona(),
                    short_term=st.session_state["short_term"],
                    long_term=ltm,
                    model_name=st.session_state["model_name"],
                    monologue=st.session_state.get("monologue", []),
                )
                st.session_state["monologue"] = monologue
            except Exception as e:
                response = f"Error: {e}"
        st.markdown(response)

    st.session_state["chat_history"].append({"role": "assistant", "content": response})
    st.rerun()


def render_chat() -> None:
    st.markdown(f"### {st.session_state['agent_name']}")
    _maybe_show_proactive_suggestion()
    _render_history()
    _handle_user_input()
