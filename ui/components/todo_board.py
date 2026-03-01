import streamlit as st
from tools.todo_manager import load_todos_for_ui, mark_todo_done


def _done_card(task: str, task_id: int) -> None:
    checkbox_html = (
        '<span style="display:inline-flex;align-items:center;justify-content:center;'
        'width:18px;height:18px;border-radius:50%;background:#22c55e;'
        'color:white;font-size:11px;flex-shrink:0;">✓</span>'
    )
    st.markdown(
        f"""<div style="display:flex;align-items:center;gap:10px;
            padding:8px 12px;margin-bottom:6px;border-radius:8px;
            background:rgba(34,197,94,0.06);border-left:3px solid #22c55e;">
            {checkbox_html}
            <span style="font-size:13px;color:#9ca3af;text-decoration:line-through;">{task}</span>
            <span style="margin-left:auto;font-size:11px;color:#6b7280;">#{task_id}</span>
        </div>""",
        unsafe_allow_html=True,
    )


def _pending_card(task: str, task_id: int) -> None:
    checkbox_html = (
        '<span style="display:inline-flex;align-items:center;justify-content:center;'
        'width:18px;height:18px;border-radius:50%;border:2px solid #6366f1;'
        'background:transparent;flex-shrink:0;"></span>'
    )
    col_card, col_btn = st.columns([5, 1])
    with col_card:
        st.markdown(
            f"""<div style="display:flex;align-items:center;gap:10px;
                padding:8px 12px;margin-bottom:6px;border-radius:8px;
                background:rgba(99,102,241,0.06);border-left:3px solid #6366f1;">
                {checkbox_html}
                <span style="font-size:13px;color:#e2e8f0;">{task}</span>
                <span style="margin-left:auto;font-size:11px;color:#6b7280;">#{task_id}</span>
            </div>""",
            unsafe_allow_html=True,
        )
    with col_btn:
        if st.button("✓", key=f"done_{task_id}", help="Mark as done", use_container_width=True):
            mark_todo_done(task_id)
            st.rerun()


def render_todo_board() -> None:
    st.markdown("### To-Do Board")
    todos = load_todos_for_ui()

    if not todos:
        st.caption("No tasks yet. Ask the agent to add one!")
        return

    for item in todos:
        if item["done"]:
            _done_card(item["task"], item["id"])
        else:
            _pending_card(item["task"], item["id"])
