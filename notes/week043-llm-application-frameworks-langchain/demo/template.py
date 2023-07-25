from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

prompt = PromptTemplate.from_template("将下面的句子翻译成英文：{sentence}")
text = prompt.format(sentence="今天的天气真不错")

llm = OpenAI(temperature=0.9)
response = llm.predict(text)
print(response)

# Today's weather is really great.

system_message_prompt = SystemMessagePromptTemplate.from_template("你是一个翻译助手，可以将{input_language}翻译成{output_language}。")
human_message_prompt = HumanMessagePromptTemplate.from_template("{text}")
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
messages = chat_prompt.format_messages(input_language="中文", output_language="英文", text="今天的天气真不错")

chat = ChatOpenAI(temperature=0.9)
response = chat.predict_messages(messages)
print(response.content)

# The weather today is really good.
