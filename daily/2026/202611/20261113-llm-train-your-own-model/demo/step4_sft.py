import torch
import torch.nn as nn
import torch.nn.functional as F
from tokenizers import Tokenizer, decoders

torch.manual_seed(42)

tokenizer = Tokenizer.from_file("mini_tokenizer.json")
tokenizer.decoder = decoders.ByteLevel()


# 一个 Transformer Block：自注意力 + 前馈网络，各配一个残差连接
class Block(nn.Module):
    def __init__(self, d, n_head, max_len):
        super().__init__()
        # 多头自注意力，batch_first=True 表示输入形状是 [batch, 序列长度, 维度]
        self.attn = nn.MultiheadAttention(d, n_head, batch_first=True)
        # 前馈网络：先把维度扩到 4 倍，过 GELU 激活，再压回 d
        # 扩展再压缩是 Transformer 的固定套路，让模型有更大的中间空间做非线性变换
        self.ffn = nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(), nn.Linear(4 * d, d))
        # 两个 LayerNorm，分别用在注意力和前馈网络之前
        self.ln1, self.ln2 = nn.LayerNorm(d), nn.LayerNorm(d)
        # 因果掩码：一个上三角矩阵，上三角为 True 的位置表示不允许注意力看到
        # 这样位置 t 只能看到前 t 个 token，看不到未来，这就是单向注意力
        mask = torch.triu(torch.ones(max_len, max_len), diagonal=1).bool()
        # 掩码是固定常量，不参与训练，但要跟着模型一起保存和搬设备
        # register_buffer 就是把它登记成模型的非训练状态，用普通属性赋值则不会跟随模型
        self.register_buffer("mask", mask)

    # x 是这个 Block 的输入，形状 [batch, 序列长度, d]，每个 token 一个 d 维向量
    def forward(self, x):
        # x 的形状是 [batch, 序列长度, d]，维度从 0 开始数，第 1 维就是序列长度
        # 实际序列长度可能小于 max_len，掩码切出对应大小
        T = x.size(1)
        # 先做 LayerNorm，再进注意力（Pre-Norm 结构，训练更稳定）
        h = self.ln1(x)
        # 三个 h 分别是 query、key、value，自注意力就是自己和自己做注意力
        # 最后加上残差连接：输出 = 原始输入 + 注意力结果，梯度可以直通
        x = x + self.attn(h, h, h, attn_mask=self.mask[:T, :T])[0]
        # 前馈网络同样先 LayerNorm，再加残差
        return x + self.ffn(self.ln2(x))


class MiniGPT(nn.Module):
    def __init__(self, vocab, d=384, n_head=6, n_layer=4, max_len=128):
        super().__init__()
        self.max_len = max_len
        # 词嵌入：把 token id 查表变成 d 维向量，词表大小是 vocab
        self.tok_emb = nn.Embedding(vocab, d)
        # 位置嵌入：把位置编号（0、1、2……）也查表变成 d 维向量
        self.pos_emb = nn.Embedding(max_len, d)
        # 堆叠 n_layer 个 Transformer Block
        self.blocks = nn.Sequential(*[Block(d, n_head, max_len) for _ in range(n_layer)])
        # 收尾的 LayerNorm
        self.ln_f = nn.LayerNorm(d)
        # 语言模型头：把 d 维向量投影成 vocab 维的 logits，每个位置一个分布
        self.head = nn.Linear(d, vocab, bias=False)

    def forward(self, idx, target=None):
        T = idx.size(1)
        # token 向量和位置向量相加，得到第一层的输入
        x = self.tok_emb(idx) + self.pos_emb(torch.arange(T, device=idx.device))
        # 过完所有 Block 和 LayerNorm，再过语言模型头
        # 输出 logits 的形状是 [batch, T, vocab]，每个位置一个概率分布的原始打分
        logits = self.head(self.ln_f(self.blocks(x)))
        loss = None
        # 传入了目标序列，就顺带算交叉熵损失；不传则只返回 logits，生成时用
        if target is not None:
            loss = F.cross_entropy(logits.view(-1, logits.size(-1)), target.view(-1))
        return logits, loss


device = "mps"
model = MiniGPT(vocab=tokenizer.get_vocab_size()).to(device)
model.load_state_dict(torch.load("mini_gpt_pretrain.pt"))

sft_data = [
    "<|user|>你是谁？<|bot|>我是小迷你，一个刚训练好的小模型。<|endoftext|>",
    "<|user|>小明喜欢什么？<|bot|>小明喜欢编程，他每天早上都会写代码。<|endoftext|>",
    "<|user|>训练模型需要什么？<|bot|>需要数据、算力和耐心。<|endoftext|>",
    "<|user|>大模型是什么？<|bot|>大模型是一种会说话的程序。<|endoftext|>",
    "<|user|>loss 下降说明什么？<|bot|>说明模型在学习。<|endoftext|>",
    "<|user|>编程让小明怎么样？<|bot|>编程让小明感到快乐。<|endoftext|>",
    "<|user|>你会说什么语言？<|bot|>我会说中文和英文。<|endoftext|>",
    "<|user|>小明是谁？<|bot|>小明是一个喜欢编程的少年。<|endoftext|>",
    "<|user|>什么是分词器？<|bot|>分词器把文本变成 token。<|endoftext|>",
    "<|user|>你的模型大吗？<|bot|>我的模型虽然小，但是能说话。<|endoftext|>",
    "<|user|>你开心吗？<|bot|>我每天都很开心。<|endoftext|>",
    "<|user|>再见<|bot|>再见，欢迎下次再来。<|endoftext|>",
]

opt = torch.optim.AdamW(model.parameters(), lr=1e-4, weight_decay=0.1)

for step in range(300):
    text = sft_data[step % len(sft_data)]
    ids = tokenizer.encode(text).ids
    if len(ids) < 2:
        continue
    x = torch.tensor(ids[:-1], device=device).unsqueeze(0)
    y = torch.tensor(ids[1:], device=device).unsqueeze(0)
    _, loss = model(x, y)
    opt.zero_grad()
    loss.backward()
    opt.step()
    if step % 10 == 0:
        print(f"sft step {step:3d} | loss {loss.item():.2f}")


@torch.no_grad()
def generate(idx, max_new=40, temperature=0.8):
    eos = tokenizer.token_to_id("<|endoftext|>")
    for _ in range(max_new):
        logits, _ = model(idx[:, -model.max_len:])
        probs = F.softmax(logits[:, -1, :] / temperature, dim=-1)
        nxt = torch.multinomial(probs, 1)
        idx = torch.cat([idx, nxt], dim=1)
        if nxt.item() == eos:
            break
    return idx


# prompt = "<|user|>小明喜欢什么？<|bot|>"
prompt = "<|user|>你好<|bot|>"
ids = tokenizer.encode(prompt).ids
x0 = torch.tensor(ids, device=device).unsqueeze(0)
out = tokenizer.decode(generate(x0)[0].tolist())
print("--- SFT 后 ---")
print("输入:", prompt)
print("输出:", out)
