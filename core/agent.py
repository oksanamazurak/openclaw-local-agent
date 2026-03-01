
from typing import Annotated, TypedDict

from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from core.llm import build_llm, DEFAULT_MODEL
from core.prompts import SYSTEM_PROMPT, PROACTIVE_PROMPT
from memory.short_term import ShortTermMemory
from memory.long_term import LongTermMemory
from tools.tool_registry import get_all_tools, save_to_memory


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def _build_system_prompt(persona: dict, ltm_context: str) -> str:
    name = persona.get("agent_name", "OpenClaw")
    role = persona.get("agent_role", "Personal Assistant")
    instructions = persona.get("system_instructions", "")
    user_name = persona.get("user_name", "User")
    user_info = persona.get("user_info", "")

    prompt = SYSTEM_PROMPT.format(
        name=name,
        role=role,
        user_name=user_name,
        user_info=f"User info: {user_info}" if user_info else "",
        instructions=f"Special instructions: {instructions}" if instructions else "",
        ltm_context=f"\n--- Relevant memories ---\n{ltm_context}" if ltm_context else "",
    )
    return "\n".join(line for line in prompt.splitlines() if line.strip())


_graph_cache: dict = {}


def build_graph(model_name: str = DEFAULT_MODEL):
    tools = get_all_tools()
    llm = build_llm(model_name).bind_tools(tools, tool_choice="auto")
    tool_node = ToolNode(tools)

    def chatbot(state: AgentState) -> dict:
        return {"messages": [llm.invoke(state["messages"])]}

    def should_use_tools(state: AgentState) -> str:
        last = state["messages"][-1]
        if isinstance(last, AIMessage) and last.tool_calls:
            return "tools"
        return END

    graph = StateGraph(AgentState)
    graph.add_node("chatbot", chatbot)
    graph.add_node("tools", tool_node)
    graph.add_edge(START, "chatbot")
    graph.add_conditional_edges("chatbot", should_use_tools, {"tools": "tools", END: END})
    graph.add_edge("tools", "chatbot")
    return graph.compile()


def get_or_build_graph(model_name: str = DEFAULT_MODEL):
    """Return a cached compiled graph for *model_name*, building it on first use."""
    if model_name not in _graph_cache:
        _graph_cache[model_name] = build_graph(model_name)
    return _graph_cache[model_name]


def invalidate_graph_cache(model_name: str | None = None) -> None:
    """Drop cached graph(s) so they are rebuilt on the next call.

    Pass *model_name* to invalidate only that model; omit it to clear all.
    """
    if model_name is None:
        _graph_cache.clear()
    else:
        _graph_cache.pop(model_name, None)


def run_agent(
    user_input: str,
    persona: dict,
    short_term: ShortTermMemory,
    long_term: LongTermMemory | None,
    model_name: str = DEFAULT_MODEL,
    monologue: list | None = None,
) -> tuple[str, list[dict]]:
    """Run one full agent turn. Returns (response_text, monologue)."""
    if monologue is None:
        monologue = []

    ltm_context = ""
    if long_term:
        try:
            ltm_docs = long_term.search(user_input, k=3)
            if ltm_docs:
                ltm_context = "\n".join(d["document"] for d in ltm_docs)
                monologue.append({"step": "memory_retrieval", "detail": f"Found {len(ltm_docs)} relevant memories"})
        except Exception as e:
            monologue.append({"step": "memory_retrieval", "detail": f"LTM search failed: {e}"})

    system_msg = SystemMessage(content=_build_system_prompt(persona, ltm_context))
    user_msg = HumanMessage(content=user_input)
    short_term.add(user_msg)

    all_messages = [system_msg] + short_term.get_messages()
    monologue.append({"step": "thinking", "detail": f"Processing: '{user_input[:80]}...'"})

    try:
        result = get_or_build_graph(model_name).invoke({"messages": all_messages})
    except Exception as e:
        error_msg = f"Agent error: {e}"
        monologue.append({"step": "error", "detail": error_msg})
        return error_msg, monologue

    result_messages = result.get("messages", [])

    response_text = ""
    for msg in reversed(result_messages):
        if isinstance(msg, AIMessage) and msg.content and not msg.tool_calls:
            response_text = msg.content
            break

    if not response_text:
        response_text = "I processed your request but have no textual response."

    for msg in result_messages:
        if isinstance(msg, AIMessage) and msg.tool_calls:
            for tc in msg.tool_calls:
                monologue.append({"step": "tool_call", "detail": f"Calling tool: {tc['name']}({tc.get('args', {})})"})
        if isinstance(msg, ToolMessage):
            monologue.append({"step": "tool_result", "detail": f"Tool '{msg.name}' returned: {str(msg.content)[:200]}"})

    if long_term:
        for msg in result_messages:
            if isinstance(msg, AIMessage) and msg.tool_calls:
                for tc in msg.tool_calls:
                    if tc["name"] == "save_to_memory":
                        text_to_save = tc["args"].get("text", "")
                        if text_to_save:
                            try:
                                long_term.store(text_to_save, {"source": "agent"})
                                monologue.append({"step": "memory_save", "detail": f"Stored: '{text_to_save[:100]}'"})
                            except Exception as e:
                                monologue.append({"step": "memory_save_error", "detail": str(e)})

    short_term.add(AIMessage(content=response_text))
    monologue.append({"step": "response", "detail": f"Replied: '{response_text[:100]}...'"})

    return response_text, monologue


def check_proactive_tasks(
    todos: list[dict],
    persona: dict,
    model_name: str = DEFAULT_MODEL,
) -> str | None:
    """Check for unfinished tasks and generate a proactive suggestion."""
    pending = [t for t in todos if not t.get("done")]
    if not pending:
        return None

    task_list = "\n".join(f"- #{t['id']}: {t['task']}" for t in pending)
    name = persona.get("agent_name", "OpenClaw")
    prompt = PROACTIVE_PROMPT.format(name=name, task_list=task_list)

    try:
        from langchain_core.messages import HumanMessage as HM
        llm = build_llm(model_name, temperature=0.7)
        response = llm.invoke([HM(content=prompt)])
        return response.content
    except Exception:
        task = pending[0]
        return f"Hey! I see we still have an open task: **#{task['id']}: {task['task']}**. Want me to help with that?"
