from langchain import PromptTemplate, OpenAI, LLMChain

llm = OpenAI(temperature=0.9)
prompt = PromptTemplate.from_template("将下面的句子翻译成英文：{sentence}")

llm_chain = LLMChain(
    llm = llm, 
    prompt = prompt
)
result = llm_chain("今天的天气真不错")
print(result['text'])
