from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Fetch variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

from supabase import create_client, Client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
response = (
    supabase.table("students")
    .select("*")
    .execute()
)
print(response)


# response = (
#     supabase.table("students")
#     .select("name, age")
#     .execute()
# )
# print(response)

# response = (
#     supabase.table("students")
#     .insert({"name": "zhangsan", "age": 18})
#     .execute()
# )
# print(response)

# response = (
#     supabase.table("students")
#     .insert([
#         {"name": "zhangsan", "age": 18},
#         {"name": "lisi", "age": 20}
#     ])
#     .execute()
# )
# print(response)

# response = (
#     supabase.table("students")
#     .update({"age": 20})
#     .eq("name", "zhangsan")
#     .execute()
# )
# print(response)

# response = (
#     supabase.table("students")
#     .upsert({"id": 15, "name": "zhangsan", "age": 20})
#     .execute()
# )
# print(response)

# response = (
#     supabase.table("students")
#     .delete()
#     .eq("id", 15)
#     .execute()
# )
# print(response)

# response = (
#     supabase.table("students")
#     .delete()
#     .eq("name", "zhangsan")
#     .execute()
# )
# print(response)

# response = (
#     supabase.table("students")
#     .delete()
#     .in_("id", [14, 13, 12, 11])
#     .execute()
# )
# print(response)
