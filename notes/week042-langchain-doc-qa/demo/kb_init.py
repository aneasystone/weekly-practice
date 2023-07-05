import tqdm
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from qdrant_client.http.models import PointStruct
from llm import to_embedding

client = QdrantClient("127.0.0.1", port=6333)

def create_kb(kb_name):	
	client.recreate_collection(
		collection_name=kb_name,
		vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
	)

def init_kb(kb_name, kb_file):
	id = 1
	with open(kb_file, 'r', encoding='utf-8') as f:
		for line in tqdm.tqdm(f.readlines()):
			embedding = to_embedding(line)
			client.upsert(
				collection_name=kb_name,
				wait=True,
				points=[
					PointStruct(id=id, vector=embedding, payload={"text": line}),
				],
			)
			id += 1

if __name__ == '__main__':
	create_kb('kb')
	init_kb('kb', './kb.txt')
