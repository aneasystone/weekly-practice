from langchain import PromptTemplate, OpenAI, LLMChain

llm = OpenAI(temperature=0.9)
# prompt = PromptTemplate.from_template("将下面的句子翻译成{lang}：{sentence}")
prompt = PromptTemplate(
    input_variables=['lang', 'sentence'],
    template = "将下面的句子翻译成{lang}：{sentence}"
)

llm_chain = LLMChain(
    llm = llm, 
    prompt = prompt
)
result = llm_chain({"lang": "日语", "sentence": "今天的天气真不错"})
print(result['text'])

# 今日の天気は本当に良いです。
