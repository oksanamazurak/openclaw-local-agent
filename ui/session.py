import streamlit as st
from memory.short_term import ShortTermMemory
from memory.long_term import LongTermMemory


def init_session() -> None:
    defaults = {
        "chat_history": [],
        "short_term": ShortTermMemory(),
        "long_term": None,
        "monologue": [],
        "proactive_shown": False,
        "user_name": "User",
        "user_info": "",
        "agent_name": "OpenClaw",
        "agent_role": "Personal Assistant",
        "system_instructions": "",
        "model_name": "qwen2.5:7b",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def get_long_term() -> LongTermMemory | None:
    if st.session_state["long_term"] is None:
        try:
            st.session_state["long_term"] = LongTermMemory()
        except Exception:
            pass
    return st.session_state["long_term"]


def get_persona() -> dict:
    return {
        "user_name": st.session_state["user_name"],
        "user_info": st.session_state["user_info"],
        "agent_name": st.session_state["agent_name"],
        "agent_role": st.session_state["agent_role"],
        "system_instructions": st.session_state["system_instructions"],
    }
