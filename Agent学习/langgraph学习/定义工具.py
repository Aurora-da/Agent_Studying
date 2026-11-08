from dotenv import load_dotenv
from typing import Annotated, Literal

from typing_extensions import TypedDict
from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import ToolNode, tools_condition


load_dotenv('.env')


# 自定义状态
class State(TypedDict):
    messages: Annotated[list, add_messages]


# 创建图构建器
graph_builder = StateGraph(State)


# 1.定义工具
search_tool = TavilySearch(max_results=2)
tools=[search_tool]


# 2.初始化 LLM 并绑定工具
llm = init_chat_model("deepseek:deepseek-flash")
llm_with_tools = llm.bind_tools(tools)


# 3.chatbot 节点：调用绑定了工具的 LLM
def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


# 4.添加节点
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools))


# 5.添加边
graph_builder.add_edge(START, "chatbot")
# 增加一个条件边，如果最后一条消息有 tool_calls 就去 tools，否则直接去 END。
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
# 工具执行完成后回到 chatbot，让模型基于搜索结果来继续回答。
graph_builder.add_edge("tools", "chatbot")


# 6.编译
checkpointer = InMemorySaver()
graph = graph_builder.compile(checkpointer=checkpointer)


if __name__ == "__main__":
    config = {"configurable": {"thread_id": "user-1"}}

    while True:
        user_input = input("你：").strip()
        if user_input.lower() in ("quit", "exit"):
            break
        if not user_input:
            continue

        result = graph.invoke(
            {"messages": [{"role": "user", "content": user_input}]},
            config=config,
        )
        print("AI:", result["messages"][-1].content)