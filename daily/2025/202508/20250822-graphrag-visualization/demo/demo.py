import networkx as nx

# 创建无向图
G = nx.Graph()

# 添加节点
nodes = [
    ("n1", {"label": "Node 1"}),
    ("n2", {"label": "Node 2"}),
]
for name, attrs in nodes:
    G.add_node(name, **attrs)

# 添加边
relationships = [
    ("n1", "n2", {"weight": 3.5}),
]

for source, target, attrs in relationships:
    G.add_edge(source, target, **attrs)

# 将图保存为 GraphML 格式
nx.write_graphml(G, "demo.graphml", encoding='utf-8')
