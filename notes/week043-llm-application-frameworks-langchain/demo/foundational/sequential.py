from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

llm = OpenAI(temperature=0.7)
template = "你是一个地理学家，说出{country}五个著名城市名称，以逗号分割："
prompt_template = PromptTemplate.from_template(template)
city_chain = LLMChain(llm=llm, prompt=prompt_template, verbose=True)
# result = city_chain.run("中国")
# print(result)

llm = OpenAI(temperature=0.7)
template = "你是一个美食家，说出下面每个城市的一种美食：{city}"
prompt_template = PromptTemplate.from_template(template)
cate_chain = LLMChain(llm=llm, prompt=prompt_template, verbose=True)
# result = cate_chain.run("北京、上海、广州、深圳、杭州")
# print(result)

from langchain.chains import SimpleSequentialChain
overall_chain = SimpleSequentialChain(chains=[city_chain, cate_chain], verbose=True)
result = overall_chain.run("中国")
print(result)
