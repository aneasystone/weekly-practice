import torch

a = torch.tensor(3.0, requires_grad=True)
b = torch.tensor(2.0, requires_grad=True)
c = torch.tensor(1.0, requires_grad=True)

d = a * b   # 前向：d = 6
f = d + c   # 前向：f = 7

f.backward()  # 反向传播，梯度写入 .grad

print(a.grad)  # tensor(2.)
print(b.grad)  # tensor(3.)
print(c.grad)  # tensor(1.)
