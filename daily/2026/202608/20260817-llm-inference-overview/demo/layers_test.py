from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen3-0.6B")

# 模型一共有多少层
print(model.config.num_hidden_layers)

# 打印第 0 层，看看一层里面都有什么
print(model.model.layers[0])

config = model.config
print(config.vocab_size)           # 151936，词表大小
print(config.hidden_size)          # 1024，嵌入向量的维度
print(config.num_attention_heads)  # 16，Q 的注意力头数
print(config.num_key_value_heads)  # 8，K、V 的注意力头数
print(config.head_dim)             # 128，每个头的维度
