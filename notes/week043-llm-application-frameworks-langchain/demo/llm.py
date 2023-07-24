from langchain.llms import OpenAI

llm = OpenAI(temperature=0.9)
response = llm.predict("给水果店取一个名字")
print(response)

# 果舞时光

response = llm.predict("将下面的句子翻译成英文：今天的天气真不错")
print(response)

# The weather is really nice today.
