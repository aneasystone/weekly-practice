from langchain.chains import TransformChain

from faiss_db import init_faiss_db
faiss_db = init_faiss_db('./kb.txt')

def similarity_search(inputs: dict) -> dict:
    text = inputs["text"]
    search_result = faiss_db.similarity_search(text)
    return {"search_result": search_result[0].page_content}

transform_chain = TransformChain(
    input_variables=["text"], output_variables=["search_result"], transform=similarity_search
)
result = transform_chain.run('小明家的宠物狗叫什么名字？')
print(result)
