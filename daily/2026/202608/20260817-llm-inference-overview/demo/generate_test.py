from transformers import AutoModelForCausalLM, AutoTokenizer

# 1. 加载分词器和模型
model_name = "Qwen/Qwen3-0.6B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# 2. 分词：文本变成 token 编号
messages = [{"role": "user", "content": "用一句话解释什么是大模型推理"}]
text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
inputs = tokenizer(text, return_tensors="pt")

# 3. 生成：Prefill + Decode 循环都在这一步里
outputs = model.generate(**inputs, max_new_tokens=1024)

# 4. 反分词：token 编号还原成文本
response = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
print(response)
