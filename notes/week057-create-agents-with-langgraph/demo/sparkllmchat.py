from langchain_community.chat_models import ChatSparkLLM

from langchain_core.messages import HumanMessage

# https://python.langchain.com/v0.2/docs/integrations/chat/sparkllm/

chat = ChatSparkLLM(
    # spark_api_url="wss://spark-api.xf-yun.com/v3.5/chat",
    # spark_llm_domain="generalv3.5"
    
    spark_api_url="wss://spark-api.xf-yun.com/v4.0/chat",
    spark_llm_domain="4.0Ultra",
    streaming=True,
)

message = HumanMessage(content="Hello")
result = chat.invoke([message])
print(result)

# for chunk in chat.stream("你是谁？"):
#     print(chunk.content, end="")
# print()
