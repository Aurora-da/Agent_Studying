from dotenv import load_dotenv
from typing import Annotated

from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver


load_dotenv('.env')


# 自定义状态，messages是一个消息列表，add_messages 是一个 reducer，使用它能够将节点返回的消息由覆盖原列表改成累加消息
class State(TypedDict):
    messages: Annotated[list, add_messages]


# 创建图构建器
graph_builder = StateGraph(State)


# 初始化语言模型
llm = init_chat_model(
    "deepseek:deepseek-flash",
)


# 定义聊天机器人函数
def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}


# 添加节点和边
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")

checkpointer = InMemorySaver()
graph = graph_builder.compile(checkpointer=checkpointer)

if __name__ == "__main__":
    config = {"configurable": {"thread_id": "user-1"}}  # 同一个 thread_id 代表同一个对话

    while True:
        user_input = input("你：")

        if user_input.lower() in ("quit", "exit"):
            print("对话已经结束，欢迎您的下次使用。")
            break

        # 只传入新消息，历史由 checkpointer 自动恢复
        result = graph.invoke(
            {"messages": [{"role": "user", "content": user_input}]},
            config=config,
        )
        print("助手:", result["messages"][-1].content)