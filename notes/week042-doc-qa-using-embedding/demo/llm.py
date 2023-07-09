import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def to_embedding(text_string):
	model_id = "text-embedding-ada-002"
	embedding = openai.Embedding.create(input=text_string, model=model_id)['data'][0]['embedding']
	return embedding

def format_prompt(question, search_results):
	
	system_content = '你是一个知识库助手，你将根据我提供的知识库内容来回答问题'
	
	user_content = '已知有知识库内容如下：\n'
	for index, item in enumerate(search_results):
		user_content += str(index+1) + '. ' + item.payload['text'] + '\n'
	user_content += '请根据知识库回答以下问题：' + question

	print(user_content)

	return [
        {'role': 'system', 'content': system_content},
        {'role': 'user', 'content': user_content},
    ]

def completion(question, search_results):
	completion = openai.ChatCompletion.create(
        temperature=0.7,
        model="gpt-3.5-turbo",
        messages=format_prompt(question, search_results),
    )
	return completion.choices[0].message.content
