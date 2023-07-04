import os
import openai
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

os.environ['http_proxy'] = 'socks5://127.0.0.1:7890'
os.environ['https_proxy'] = 'socks5://127.0.0.1:7890'

openai.api_key = os.getenv("OPENAI_API_KEY")

def to_embedding(text_string):
	model_id = "text-embedding-ada-002"
	embedding = openai.Embedding.create(input=text_string, model=model_id)['data'][0]['embedding']
	return embedding

client = QdrantClient("127.0.0.1", port=6333)
client.recreate_collection(
	collection_name="kb",
	vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
)
