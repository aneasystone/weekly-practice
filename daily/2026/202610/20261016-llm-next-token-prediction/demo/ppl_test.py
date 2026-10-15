import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "Qwen/Qwen3-0.6B"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, dtype="auto")

text = "北京是中国的首都，位于中国北方"
inputs = tokenizer(text, return_tensors="pt").to(model.device)

with torch.no_grad():
    outputs = model(**inputs)
logits = outputs.logits  # 形状 [batch, 序列长度, 词表大小]

# 位置 t 的输出预测的是位置 t+1 的 token，错开一位对齐
shift_logits = logits[:, :-1, :]
shift_labels = inputs["input_ids"][:, 1:]

# 逐位置计算交叉熵，先不做平均
losses = F.cross_entropy(shift_logits[0], shift_labels[0], reduction="none")

# 逐个位置打印 token 和它的损失
tokens = [tokenizer.decode([i]) for i in shift_labels[0]]
for tok, loss in zip(tokens, losses):
    print(f"{tok}\t{loss.item():.4f}")

avg_loss = losses.mean()
print("平均损失:", avg_loss.item())
print("整句 PPL:", torch.exp(avg_loss).item())

####

with torch.no_grad():
    loss = model(**inputs, labels=inputs["input_ids"]).loss
print("平均损失:", loss.item())
print("整句 PPL:", torch.exp(loss).item())
