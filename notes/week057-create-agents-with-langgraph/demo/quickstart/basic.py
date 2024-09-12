### 定义状态图

from langgraph.graph import StateGraph, MessagesState

graph_builder = StateGraph(MessagesState)

### 定义模型和 chatbot 节点

from langchain_openai import ChatOpenAI

llm = ChatOpenAI()

def chatbot(state: MessagesState):
    return {"messages": [llm.invoke(state["messages"])]}

### 构建和编译图

from langgraph.graph import END, START

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()

### 运行

from langchain_core.messages import HumanMessage

response = graph.invoke(
    {"messages": [HumanMessage(content="合肥今天天气怎么样？")]}
)
response["messages"][-1].pretty_print()
