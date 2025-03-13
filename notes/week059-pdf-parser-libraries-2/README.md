# WEEK060 - 盘点 Python 中那些 PDF 解析库（二）

接 [上篇](../week059-pdf-parser-libraries/README.md)，继续盘点 Python 中那些 PDF 解析库。

## unstructured

https://github.com/Unstructured-IO/unstructured

https://docs.unstructured.io/open-source/introduction/supported-file-types

https://docs.unstructured.io/open-source/concepts/partitioning-strategies

https://docs.unstructured.io/open-source/how-to/set-ocr-agent

https://blog.csdn.net/phillihp/article/details/140200102

https://github.com/Megvii-BaseDetection/YOLOX

https://huggingface.co/unstructuredio/yolo_x_layout

https://github.com/Unstructured-IO/unstructured-inference/blob/main/unstructured_inference/models/tables.py

https://www.nltk.org/data.html

https://github.com/facebookresearch/detectron2

## Table Transformer

接下来再介绍一个表格提取的库：来自微软的 [Table Transformer](https://github.com/microsoft/table-transformer)。

上面介绍 Camelot 和 Tabula 的时候提到过各种模式，其实都是基于规则的算法，而 Table Transformer 则是基于深度学习算法，且是基于 Transformer 模型。

https://arxiv.org/pdf/2110.00061

https://huggingface.co/datasets/bsmock/pubtables-1m/tree/main

https://huggingface.co/bsmock/tatr-pubtables1m-v1.0/tree/main

https://huggingface.co/microsoft/table-transformer-detection/tree/main

TATR 可以被训练以在许多文档领域中表现良好，训练您自己的模型所需的一切都包含在这里。但目前仅提供在 PubTables-1M 数据集上训练的 TATR 的预训练模型权重。（请参阅附加文档以了解如何训练您自己的多领域模型。）

TATR 是一个对象检测模型，可以从图像输入中识别表格。基于 TATR 构建的推理代码需要文本提取（来自 OCR 或直接从 PDF）作为单独的输入，以便在其 HTML 或 CSV 输出中包含文本。

https://docs.llamaindex.ai/en/v0.10.18/examples/multi_modal/multi_modal_pdf_tables.html

https://github.com/NielsRogge/Transformers-Tutorials/blob/master/Table%20Transformer/Inference_with_Table_Transformer_(TATR)_for_parsing_tables.ipynb

https://blog.csdn.net/weixin_38235865/article/details/130113534

https://zhuanlan.zhihu.com/p/642965291

https://zhuanlan.zhihu.com/p/689418869

### DETR

https://github.com/microsoft/table-transformer/blob/main/detr/models/detr.py

https://github.com/facebookresearch/detr

https://huggingface.co/docs/transformers/main/en/model_doc/detr

## Nougat

https://github.com/facebookresearch/nougat

https://arxiv.org/pdf/2308.13418

https://facebookresearch.github.io/nougat/

https://github.com/NielsRogge/Transformers-Tutorials/blob/master/Nougat/Inference_with_Nougat_to_read_scientific_PDFs.ipynb

## Donut

https://zhuanlan.zhihu.com/p/633696599

## docTR

https://github.com/mindee/doctr

## docling

https://github.com/DS4SD/docling

## omniparse

https://github.com/adithya-s-k/omniparse

## marker

https://github.com/VikParuchuri/marker

## surya

https://github.com/VikParuchuri/surya

## PDF-Extract-Kit

https://github.com/opendatalab/PDF-Extract-Kit

## zerox

https://github.com/getomni-ai/zerox

## PDFMathTranslate

https://github.com/Byaidu/PDFMathTranslate

## comic-translate

https://github.com/ogkalu2/comic-translate

## mPLUG-DocOwl

https://github.com/X-PLUG/mPLUG-DocOwl

## reportlab

https://docs.reportlab.com/

## 参考

* [How to Process PDFs in Python: A Step-by-Step Guide](https://unstructured.io/blog/how-to-process-pdf-in-python)
* [Pix2Text V1.1 新版发布，支持 PDF 转 Markdown | Breezedeus.com](https://www.breezedeus.com/article/p2t-v1.1)
* [使用视觉语言模型进行 PDF 检索 [译] | 宝玉的分享](https://baoyu.io/translations/rag/retrieval-with-vision-language-models-colpali)
* [PDF智能解析：RAG策略下的技术架构与实现](https://mp.weixin.qq.com/s/nOXtdDyE6nP6UXlRJMMK8Q)
* [LLM之RAG实战（二十九）| 探索RAG PDF解析](https://mp.weixin.qq.com/s/3_9L7MSfE38pGv8nmB6Mrg)
* [RAG增强之路：增强PDF解析并结构化技术路线方案及思路](https://mp.weixin.qq.com/s/UOPDuv9hi2MJEhOHM_TZ8A)

### Integrations

* [LangChain - Document Loaders](https://python.langchain.com/v0.1/docs/modules/data_connection/document_loaders/pdf/)
* [Llama Hub - Data Loaders](https://llamahub.ai/?tab=readers)
* [QuivrHQ/quivr](https://github.com/QuivrHQ/quivr)
* [Cinnamon/kotaemon](https://github.com/Cinnamon/kotaemon)

### PDF + RAG

* [Using LlamaParse for Knowledge Graph Creation from Documents | by Fanghua (Joshua) Yu | Apr, 2024 | Medium](https://medium.com/@yu-joshua/using-llamaparse-for-knowledge-graph-creation-from-documents-3bd1e1849754)
* [Multi-document Agentic RAG using Llama-Index and Mistral | by Plaban Nayak | The AI Forum | May, 2024 | Medium](https://medium.com/the-ai-forum/multi-document-agentic-rag-using-llama-index-and-mistral-b334fa45d3ee)
* [Building a Multi-Document ReAct Agent for Financial Analysis using LlamaIndex and Qdrant | by M K Pavan Kumar | Jun, 2024 | Stackademic](https://blog.stackademic.com/building-a-multi-document-react-agent-for-financial-analysis-using-llamaindex-and-qdrant-72a535730ac3)
* [RAG + LlamaParse: Advanced PDF Parsing for Retrieval | by Ryan Siegler | KX Systems | May, 2024 | Medium](https://medium.com/kx-systems/rag-llamaparse-advanced-pdf-parsing-for-retrieval-c393ab29891b)
