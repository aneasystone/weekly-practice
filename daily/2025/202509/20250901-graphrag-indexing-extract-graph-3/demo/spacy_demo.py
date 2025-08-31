import spacy

# 1. 加载模型
model_name = "en_core_web_sm"
try:
    nlp = spacy.load(model_name)
except OSError:
    print(f"Model not found. Attempting to download...")
    from spacy.cli.download import download
    download(model_name)
    nlp = spacy.load(model_name)

# python -m spacy download en_core_web_sm
# /work/.venv/bin/python: No module named pip
# uv pip install pip

# 2. 处理文本
text = "Apple Inc, founded by Steve Jobs, develops innovative iPhone technology in California."
doc = nlp(text)

# 3. 分词和词性标注
print("分词和词性标注：")
for token in doc:
    print(f"{token.text:12} {token.pos_:8} {token.tag_:6} {token.lemma_}")

# 输出示例：
# Apple        PROPN    NNP    Apple
# Inc          PROPN    NNP    Inc
# ,            PUNCT    ,      ,
# founded      VERB     VBN    found
# by           ADP      IN     by
# Steve        PROPN    NNP    Steve
# ...

# 4. 命名实体识别
print("\n命名实体：")
for ent in doc.ents:
    print(f"{ent.text:20} {ent.label_:10} {spacy.explain(ent.label_)}")

# 输出示例：
# Apple Inc            ORG        Companies, agencies, institutions
# Steve Jobs           PERSON     People, including fictional
# iPhone               PRODUCT    Objects, vehicles, foods, etc.
# California           GPE        Countries, cities, states

# 5. 名词块提取
print("\n名词块：")
for chunk in doc.noun_chunks:
    print(f"{chunk.text:25} {chunk.root.text:10} {chunk.root.dep_}")

# 输出示例：
# Apple Inc                 Inc        nsubj
# Steve Jobs               Jobs       pobj  
# innovative iPhone technology  technology nobj
# California               California pobj

# 6. 依赖句法分析
print("\n依赖关系：")
for token in doc:
    print(f"{token.text:12} <- {token.dep_:10} -- {token.head.text}")

# 输出示例：
# Apple        <- compound   -- Inc
# Inc          <- nsubj      -- develops  
# founded      <- acl        -- Inc
# by           <- agent      -- founded
# Steve        <- compound   -- Jobs
