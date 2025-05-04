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

# response = (
#     supabase.table("students")
#     .select("*")
#     .not_.is_("name", "null")
#     .execute()
# )
# print(response)

# response = (
#     supabase.table("students")
#     .select("*")
#     .gt("age", 15)
#     .lt("age", 18)
#     .execute()
# )
# print(response)

# response = (
#     supabase.table("students")
#     .select("*")
#     .or_("age.lte.15,age.gte.18")
#     .execute()
# )
# print(response)

# --------------------
#  ranges and arrays
# --------------------

# response = (
#     supabase.table("examples")
#     .insert([
#         {"range_column": [1, 5], "array_column": [1, 2, 3, 4, 5]},
#         {"range_column": [6, 10], "array_column": [6, 7, 8, 9, 10]},
#     ])
#     .execute()
# )
# print(response)

# response = (
#     supabase.table("examples")
#     .select("*")
#     .contains("array_column", ["1", "2", "3"])
#     .execute()
# )
# print(response)

# response = (
#     supabase.table("examples")
#     .select("*")
#     .contained_by("array_column", ["1", "2", "3", "4", "5", "6"])
#     .execute()
# )
# print(response)

# response = (
#     supabase.table("examples")
#     .select("*")
#     .overlaps("array_column", ["1", "3", "5"])
#     .execute()
# )
# print(response)

# --------------------
#  jsons
# --------------------

# response = (
#     supabase.table("examples2")
#     .insert([
#         {"json_column": {"name": "zhangsan", "age": 15}},
#         {"json_column": {"name": "lisi", "age": 16}},
#     ])
#     .execute()
# )
# print(response)

# response = (
#     supabase.table("examples2")
#     .select("id, json_column->name, json_column->age")
#     .execute()
# )
# print(response)

# response = (
#     supabase.table("examples2")
#     .select("*")
#     .eq("json_column->age", 15)
#     .execute()
# )
# print(response)

# response = (
#     supabase.table("examples2")
#     .select("*")
#     .eq("json_column->>name", "zhangsan")
#     .execute()
# )
# print(response)

response = (
    supabase.table("students")
    .select("*")
    .text_search("name", "'John' | 'Bob'", options={"type": "websearch", "config": "english"},)
    .execute()
)
print(response)

response = (
    supabase.table("students")
    .select("*")
    .text_search("name", "'Smith' & 'Bob'", options={"type": "websearch", "config": "english"},)
    .execute()
)
print(response)