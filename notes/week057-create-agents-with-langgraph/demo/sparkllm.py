from langchain_community.llms import SparkLLM

# https://python.langchain.com/v0.2/docs/integrations/llms/sparkllm/

llm = SparkLLM(
    # spark_api_url="wss://spark-api.xf-yun.com/v3.5/chat",
    # spark_llm_domain="generalv3.5"
    
    spark_api_url="wss://spark-api.xf-yun.com/v4.0/chat",
    spark_llm_domain="4.0Ultra"
)

res = llm.invoke("What's your name?")
print(res)
