from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Fetch variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

from supabase import create_client, Client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ----------------
# one to many
# ----------------

# 查询所有班级
# response = (
#     supabase.table("classes")
#     .select("name")
#     .execute()
# )
# print(response)

# 查询所有班级以及该班级的学生
# response = (
#     supabase.table("classes")
#     .select("name, students(name, age)")
#     .execute()
# )
# print(response)

# 查询一年级一班以及该班级的学生
# response = (
#     supabase.table("classes")
#     .select("name, students(name, age)")
#     .eq("name", "一年级一班")
#     .execute()
# )
# print(response)

# 查询所有班级以及该班级年龄为7岁的学生
# response = (
#     supabase.table("classes")
#     .select("name, students(name, age)")
#     .eq("students.age", 7)
#     .execute()
# )
# print(response)

# ----------------
# many to one
# ----------------

# 查询所有学生
# response = (
#     supabase.table("students")
#     .select("name, age")
#     .execute()
# )
# print(response)

# 查询所有学生以及该学生所属班级
# response = (
#     supabase.table("students")
#     .select("name, age, classes(name)")
#     .execute()
# )
# print(response)

# ----------------
# many to many
# ----------------

# 查询所有班级以及该班级的老师
# response = (
#     supabase.table("classes")
#     .select("name, teachers(name)")
#     .execute()
# )
# print(response)

# 查询所有老师以及该老师任教的班级
# response = (
#     supabase.table("teachers")
#     .select("name, classes(name)")
#     .execute()
# )
# print(response)

# ----------------
# one to one
# ----------------

# 查询所有老师以及该老师的详细信息
# response = (
#     supabase.table("teachers")
#     .select("name, teacher_profiles(address, phone)")
#     .execute()
# )
# print(response)

# 查询所有老师档案以及对应的老师
# response = (
#     supabase.table("teacher_profiles")
#     .select("address, phone, teachers(name)")
#     .execute()
# )
# print(response)

# ----------------
# multiple joins
# ----------------

response = (
    supabase.table("messages")
    .select("content,from:sender_id(name),to:receiver_id(name)")
    .execute()
)
print(response)

response = (
    supabase.table("orders")
    .select("""
        id, 
        shipping_address_id(name), 
        receiving_address_id(name)
    """)
    .execute()
)
print(response)

response = (
    supabase.table("orders")
    .select("""
        id, 
        shipping:shipping_address_id(name), 
        receiving:receiving_address_id(name)
    """)
    .execute()
)
print(response)

response = (
    supabase.table("orders")
    .select("id, shipping:addresses!shipping_address_id(name), receiving:addresses!receiving_address_id(name)")
    .execute()
)
print(response)

response = (
    supabase.table("orders")
    .select("id, shipping:shipping_address_id(name), receiving:receiving_address_id(name)")
    .eq("shipping.name", "北京市朝阳区")
    .execute()
)
print(response)

response = (
    supabase.table("orders")
    .select("id, shipping:shipping_address_id!inner(name), receiving:receiving_address_id!inner(name)")
    .eq("shipping.name", "北京市朝阳区")
    .execute()
)
print(response)