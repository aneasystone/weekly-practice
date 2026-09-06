import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "Qwen/Qwen3-0.6B"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, dtype="auto")

prompt = "用一句话介绍杭州："
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

def generate(**kwargs):
    torch.manual_seed(42)  # 固定随机种子，方便对比
    out = model.generate(**inputs, max_new_tokens=60, **kwargs)
    return tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)

# 温度 0：等价于贪心，用 do_sample=False 实现
print("-"*10)
print(generate(do_sample=False))

# 温度 0.7：常见对话配置
print("-"*10)
print(generate(do_sample=True, temperature=0.7, top_p=0.9))

# 温度 1.5：高温，观察失控效果
print("-"*10)
print(generate(do_sample=True, temperature=1.5, top_p=0.9))

# # top_p=0.5：固定温度 1.0，收缩候选池
# print("-"*10)
# print(generate(do_sample=True, temperature=1.0, top_p=0.5))

# # top_p=1.0：不截断，整个词表都参与采样
# print("-"*10)
# print(generate(do_sample=True, temperature=1.0, top_p=1.0))

# # top_k=10：固定候选数量截断
# print("-"*10)
# print(generate(do_sample=True, temperature=1.0, top_k=10))

# # 重复惩罚：贪心加上 repetition_penalty，看能不能打破原地打转
# print("-"*10)
# print(generate(do_sample=False, repetition_penalty=1.5))
