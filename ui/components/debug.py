import streamlit as st
from ui.session import get_long_term


def _render_working_memory() -> None:
    st.markdown("#### Current context window sent to Ollama")
    messages = st.session_state["short_term"].to_dicts()
    if not messages:
        st.info("No messages in working memory yet. Start chatting!")
        return

    for i, msg in enumerate(messages):
        role = msg["role"]
        icon = {"human": "[human]", "ai": "[ai]", "system": "[system]", "tool": "[tool]"}.get(role, "[?]")
        with st.expander(f"{icon} {role.upper()} — message #{i + 1}", expanded=(i >= len(messages) - 3)):
            st.code(msg["content"], language=None)


def _render_long_term_memory() -> None:
    st.markdown("#### ChromaDB Vector Database Contents")
    ltm = get_long_term()

    if not ltm:
        st.warning("ChromaDB is not connected. Make sure the chroma service is running.")
        return

    st.metric("Documents stored", ltm.count())

    all_docs = ltm.get_all()
    if all_docs:
        for doc in all_docs:
            with st.expander(f"{doc['document'][:80]}..."):
                st.write("**Full text:**", doc["document"])
                st.write("**ID:**", doc["id"])
                st.write("**Metadata:**", doc.get("metadata", {}))
    else:
        st.info("No documents in long-term memory yet.")

    st.divider()
    st.markdown("##### Search relevance test")
    search_q = st.text_input("Query to test relevance:", key="ltm_search")
    if search_q:
        results = ltm.search(search_q, k=5)
        if results:
            for r in results:
                dist = r.get("distance", "N/A")
                st.markdown(f"- **Distance: {dist}** — {r['document'][:120]}")
        else:
            st.caption("No results found.")


def _render_monologue() -> None:
    st.markdown("#### Agent's Thought Process")
    monologue = st.session_state.get("monologue", [])

    if not monologue:
        st.info("No reasoning steps recorded yet. Chat with the agent to see its thinking!")
        return

    icons = {
        "thinking": ">",
        "memory_retrieval": ">",
        "tool_call": ">",
        "tool_result": ">",
        "memory_save": ">",
        "response": ">",
        "error": "[error]",
    }
    for entry in monologue:
        step = entry.get("step", "")
        detail = entry.get("detail", "")
        icon = icons.get(step, "-")
        st.markdown(f"{icon} **{step}**: {detail}")


def render_debug_page() -> None:
    st.markdown("### Under the Hood — Debug & Memory")
    tab_wm, tab_ltm, tab_mono = st.tabs(
        ["Working Memory", "Long-Term Storage", "Internal Monologue"]
    )

    with tab_wm:
        _render_working_memory()

    with tab_ltm:
        _render_long_term_memory()

    with tab_mono:
        _render_monologue()
