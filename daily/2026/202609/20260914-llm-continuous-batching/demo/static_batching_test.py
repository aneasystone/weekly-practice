import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "Qwen/Qwen3-0.6B"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, dtype="auto")

# 三条 prompt，预期的输出长度差异很大
prompts = [
    "用一句话介绍杭州。",
    "写一首关于秋天的五言绝句。",
    "详细解释为什么天空是蓝色的，不少于三百字。",
]

# 套对话模板，Qwen3 关掉思考模式，让回答尽快收尾
texts = [
    tokenizer.apply_chat_template(
        [{"role": "user", "content": p}],
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False,
    )
    for p in prompts
]

# 批式生成要左填充，保证每条序列的最后一个位置就是新 token 的位置
tokenizer.padding_side = "left"
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

inputs = tokenizer(texts, return_tensors="pt", padding=True).to(model.device)
prompt_len = inputs["input_ids"].shape[1]

outputs = model.generate(**inputs, max_new_tokens=512, do_sample=False)

for i, out in enumerate(outputs):
    new_tokens = out[prompt_len:]
    n = int((new_tokens != tokenizer.pad_token_id).sum())
    ended = tokenizer.eos_token_id in new_tokens.tolist() or tokenizer.pad_token_id in new_tokens.tolist()
    print(f"请求 {i}: 有效生成 {n} 个 token, 自然结束: {ended}")
    print(tokenizer.decode(new_tokens, skip_special_tokens=True))
    print("-" * 20)
