from qdrant_client import QdrantClient
from llm import to_embedding, completion

client = QdrantClient("127.0.0.1", port=6333)

def search(kb_name, vector, limit):
	search_results = client.search(
		collection_name=kb_name,
		query_vector=vector,
		limit=limit,
		search_params={"exact": False, "hnsw_ef": 128}
	)
	return search_results

def query(question):
    vector = to_embedding(question)
    search_results = search('kb', vector, 3)
    return completion(question, search_results)
    
if __name__ == '__main__':
	answer = query('小明家的宠物狗叫什么名字？')
	print(answer)
