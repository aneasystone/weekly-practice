# WEEK059 - 实战 PDF 解析

使用 RAG 实现企业私域知识问答是目前最流行也是最前沿的大模型技术之一，在 [week054-advanced-rag-notes](../week054-advanced-rag-notes/README.md) 这篇笔记中，我介绍了很多种不同的高级 RAG 技术，其关注点更多的是如何检索私域知识以及如何将检索结果灌输到大模型中，并没有深入如何获得这些私域知识。

现实中，绝大数企业私域知识都是非结构化的，散落在各种网页、文档或邮件附件里，如果能将这些内容解析出来，对企业来说无疑是巨大的价值。而在这些非结构化的文档中，PDF 文档占比很高，使得 PDF 解析对 RAG 至关重要。

## 开源 PDF 解析库一览

PDF 全称 Portable Document Format（可移植文档格式），于 1993 年由 Adobe 公司开发，鉴于其跨平台性、高安全性、开放标准、可搜索性和可访问性等优势，已经成为全球范围内广泛使用的文件格式。这一节对 Python 中常用的 PDF 解析库做一个盘点。

* [PyPDF](https://github.com/py-pdf/pypdf)
* [pdfminer.six](https://github.com/pdfminer/pdfminer.six)
* [pdfplumber](https://github.com/jsvine/pdfplumber)
* [PyMuPDF](https://github.com/pymupdf/PyMuPDF)
* [pypdfium2](https://github.com/pypdfium2-team/pypdfium2)
* [pikepdf](https://github.com/pikepdf/pikepdf)
* [markitdown](https://github.com/microsoft/markitdown)
* [unstructured](https://github.com/Unstructured-IO/unstructured)
* [docTR](https://github.com/mindee/doctr)
* [docling](https://github.com/DS4SD/docling)
* [omniparse](https://github.com/adithya-s-k/omniparse)
* [PDF-Extract-Kit](https://github.com/opendatalab/PDF-Extract-Kit)
* [OCRmyPDF](https://github.com/ocrmypdf/OCRmyPDF)
* [gptpdf](https://github.com/CosmosShadow/gptpdf)
* [zerox](https://github.com/getomni-ai/zerox)
* [PDFMathTranslate](https://github.com/Byaidu/PDFMathTranslate)
* [comic-translate](https://github.com/ogkalu2/comic-translate)
* [mPLUG-DocOwl](https://github.com/X-PLUG/mPLUG-DocOwl)
* [Tabula](https://github.com/tabulapdf/tabula)
* [Camelot](https://github.com/camelot-dev/camelot)
* [Table Transformer](https://github.com/microsoft/table-transformer)
* [Nougat](https://github.com/facebookresearch/nougat)

---

* [LangChain - Document Loaders](https://python.langchain.com/v0.1/docs/modules/data_connection/document_loaders/pdf/)
* [Llama Hub - Data Loaders](https://llamahub.ai/?tab=readers)
* [QuivrHQ/quivr](https://github.com/QuivrHQ/quivr)
* [Cinnamon/kotaemon](https://github.com/Cinnamon/kotaemon)

## 解析 PDF 的难点

### 表格提取

### 排版识别

### 图片处理

## 参考

* [How to Process PDFs in Python: A Step-by-Step Guide](https://unstructured.io/blog/how-to-process-pdf-in-python)
* [MarkItDown深入研究](http://www.hubwiz.com/blog/markitdown-a-deep-dive/)
* [文档处理之10种PDF解析工具测评](https://mp.weixin.qq.com/s/HaHnWb5LCJM6kuSphgKykQ)
* [Pix2Text V1.1 新版发布，支持 PDF 转 Markdown | Breezedeus.com](https://www.breezedeus.com/article/p2t-v1.1)
* [使用视觉语言模型进行 PDF 检索 [译] | 宝玉的分享](https://baoyu.io/translations/rag/retrieval-with-vision-language-models-colpali)
* [PDF智能解析：RAG策略下的技术架构与实现](https://mp.weixin.qq.com/s/nOXtdDyE6nP6UXlRJMMK8Q)
* [LLM之RAG实战（二十九）| 探索RAG PDF解析](https://mp.weixin.qq.com/s/3_9L7MSfE38pGv8nmB6Mrg)

### PDF + RAG

* [Using LlamaParse for Knowledge Graph Creation from Documents | by Fanghua (Joshua) Yu | Apr, 2024 | Medium](https://medium.com/@yu-joshua/using-llamaparse-for-knowledge-graph-creation-from-documents-3bd1e1849754)
* [Multi-document Agentic RAG using Llama-Index and Mistral | by Plaban Nayak | The AI Forum | May, 2024 | Medium](https://medium.com/the-ai-forum/multi-document-agentic-rag-using-llama-index-and-mistral-b334fa45d3ee)
* [Building a Multi-Document ReAct Agent for Financial Analysis using LlamaIndex and Qdrant | by M K Pavan Kumar | Jun, 2024 | Stackademic](https://blog.stackademic.com/building-a-multi-document-react-agent-for-financial-analysis-using-llamaindex-and-qdrant-72a535730ac3)
* [RAG + LlamaParse: Advanced PDF Parsing for Retrieval | by Ryan Siegler | KX Systems | May, 2024 | Medium](https://medium.com/kx-systems/rag-llamaparse-advanced-pdf-parsing-for-retrieval-c393ab29891b)
