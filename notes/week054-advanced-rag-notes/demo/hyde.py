from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

system = """You are an expert about a set of software for building LLM-powered applications called LangChain, LangGraph, LangServe, and LangSmith.

LangChain is a Python framework that provides a large set of integrations that can easily be composed to build LLM applications.
LangGraph is a Python package built on top of LangChain that makes it easy to build stateful, multi-actor LLM applications.
LangServe is a Python package built on top of LangChain that makes it easy to deploy a LangChain application as a REST API.
LangSmith is a platform that makes it easy to trace and test LLM applications.

Answer the user question as best you can. Answer as though you were writing a tutorial that addressed the user question."""
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "{question}"),
    ]
)
llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
qa_no_context = prompt | llm | StrOutputParser()

# answer = qa_no_context.invoke(
#     {
#         "question": "how to use multi-modal models in a chain and turn chain into a rest api"
#     }
# )
# print(answer)

from langchain_core.runnables import RunnablePassthrough

hyde_chain = RunnablePassthrough.assign(hypothetical_document=qa_no_context)

answer = hyde_chain.invoke(
    {
        "question": "how to use multi-modal models in a chain and turn chain into a rest api"
    }
)
print(answer)
