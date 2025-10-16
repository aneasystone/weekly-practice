from openai import OpenAI

client = OpenAI()

response = client.moderations.create(
  model="omni-moderation-latest",
  input="kill them all"
)

print(response)