import os
import openai

os.environ['http_proxy'] = 'socks5://127.0.0.1:7890'
os.environ['https_proxy'] = 'socks5://127.0.0.1:7890'

openai.api_key = os.getenv("OPENAI_API_KEY")

text_string = "sample text"
model_id = "text-embedding-ada-002"

embedding = openai.Embedding.create(input=text_string, model=model_id)['data'][0]['embedding']
print(len(embedding))
