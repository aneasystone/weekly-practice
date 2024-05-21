from langchain.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from tqdm import tqdm

embeddings_model = OpenAIEmbeddings()

# Initialize the Chinook database
# Chinook database can be downloaded here: https://github.com/lerocha/chinook-database

CONNECTION_STRING = "postgresql+psycopg2://root:123456@localhost:5432/vectordb"
db = SQLDatabase.from_uri(CONNECTION_STRING)

# db.run('CREATE EXTENSION vector;')
# db.run('ALTER TABLE "Track" ADD COLUMN "embeddings" vector;')

# Generate the embedding for each track title

tracks = db.run('SELECT "Name" FROM "Track"')
song_titles = [s[0] for s in eval(tracks)]
title_embeddings = embeddings_model.embed_documents(song_titles)
print(len(title_embeddings))

# Store the embeddings in the `Track` table

for i in tqdm(range(len(title_embeddings))):
    title = song_titles[i].replace("'", "''")
    embedding = title_embeddings[i]
    sql_command = (
        f'UPDATE "Track" SET "embeddings" = ARRAY{embedding} WHERE "Name" ='
        + f"'{title}'"
    )
    db.run(sql_command)

# Test the semantic search

embeded_title = embeddings_model.embed_query("hope about the future")
query = (
    'SELECT "Track"."Name" FROM "Track" WHERE "Track"."embeddings" IS NOT NULL ORDER BY "embeddings" <-> '
    + f"'{embeded_title}' LIMIT 5"
)
print(db.run(query))
