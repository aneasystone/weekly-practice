from typing import Any, Dict
from langchain.llms import OpenAI
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains.router.llm_router import LLMRouterChain
from langchain.schema import BaseOutputParser

class CustomerOutputParser(BaseOutputParser[Dict[str, str]]):

    next_input: str = ""

    def parse(self, text: str) -> Dict[str, Any]:
        parsed = {
            "destination": text.strip(),
            "next_inputs": { "input": self.next_input }
        }
        return parsed

router_template = """\
你是一个问题分类助手，已知定义了下面这些分类：

physics: 这是一个物理相关的问题
math: 这是一个数学相关的问题
default: 其他未知分类的问题

用户的问题是：

{input}

请给出该问题对应的分类名称：
"""

query = "什么是黑体辐射？"

router_prompt = PromptTemplate(
    template=router_template,
    input_variables=["input"],
    output_parser=CustomerOutputParser(next_input=query),
)

llm_chain = LLMChain(llm=OpenAI(), prompt=router_prompt, verbose=True)
router_chain = LLMRouterChain(llm_chain=llm_chain, verbose=True)
result = router_chain.route(query)
print(result)
