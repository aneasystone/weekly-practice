# WEEK059 - 实战 PDF 解析

使用 RAG 实现企业私域知识问答是目前最流行也是最前沿的大模型技术之一，在 [week054-advanced-rag-notes](../week054-advanced-rag-notes/README.md) 这篇笔记中，我介绍了很多种不同的高级 RAG 技术，其关注点更多的是如何检索私域知识以及如何将检索结果灌输到大模型中，并没有深入如何获得这些私域知识。

现实中，绝大数企业私域知识都是非结构化的，散落在各种网页、文档或邮件附件里，如果能将这些内容解析出来，对企业来说无疑是巨大的价值。而在这些非结构化的文档中，PDF 文档占比很高，使得 PDF 解析对 RAG 至关重要。

## 开源 PDF 解析库一览

PDF 全称 Portable Document Format（可移植文档格式），于 1993 年由 Adobe 公司开发，鉴于其跨平台性、高安全性、开放标准、可搜索性和可访问性等优势，已经成为全球范围内广泛使用的文件格式。Python 中有着大量的 PDF 解析库，这一节常用的 PDF 解析库做一个盘点，方便自己后期技术选型时做参考。

* [pypdf](https://github.com/py-pdf/pypdf)
* [pdfminer.six](https://github.com/pdfminer/pdfminer.six)
* [pypdfium2](https://github.com/pypdfium2-team/pypdfium2)
* [pdfplumber](https://github.com/jsvine/pdfplumber)
* [PyMuPDF](https://github.com/pymupdf/PyMuPDF)
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

## 基本使用

### pypdf

pypdf 是一个免费且开源的纯 Python PDF 库，能够分割、合并、裁剪和转换 PDF 文件的页面，可以向 PDF 文件添加自定义数据，对 PDF 文件进行加密和解密。当然，pypdf 还可以从 PDF 中提取文本、图片、附件、批注和元数据等。

```
from pypdf import PdfReader

reader = PdfReader("./pdfs/example.pdf")
number_of_pages = len(reader.pages)
print('Total %d pages.' % (number_of_pages))
for i in range(number_of_pages):
    print('----- Page %d -----' % (i+1))
    page = reader.pages[i]
    text = page.extract_text()
    print(text)

    for count, image_file_object in enumerate(page.images):
        with open(str(count) + image_file_object.name, "wb") as fp:
            fp.write(image_file_object.data)
```

可以看出 pypdf 的用法较为简单，我们只能拿到每一页的文本和图片内容，拿不到更多的详细信息，比如文本字体和大小，块位置等，这些信息在处理复杂场景时是必不可少的。所以 pypdf 只适合 PDF 的内容比较规整的场景。

### pdfminer.six

[pdfminer 最初由 Euske 开发](https://github.com/euske/pdfminer)，但是只支持 Python 2，不支持 Python 3，于是社区在他的基础上引入了 [six](https://github.com/benjaminp/six)，这是一个无需修改代码，就可以同时兼容 Python 2 和 3 的库，所以叫做 `pdfminer.six`。它也是一个纯 Python 编写的 PDF 库，专注于获取和分析文本数据。

使用 `extract_text` 方法实现类似 pypdf 的效果，直接返回文本：

```
from pdfminer.high_level import extract_text

text = extract_text("./pdfs/example.pdf")
print(text)
```

或者使用 `extract_pages` 方法提取元素的详细信息，包括文本的精确位置、字体、大小或颜色：

```
from pdfminer.high_level import extract_pages

for page in extract_pages("./pdfs/example.pdf"):
    for element in page:
        print(element)
```

这里的元素可能是 `LTTextBox`、`LTFigure`、`LTLine`、`LTRect` 或 `LTImage`，它们的层次结构如下所示：

![](./images/pdfminersix-layout.png)

其中 `LTTextBox` 还可以继续遍历得到 `LTTextLine`，`LTTextLine` 再继续遍历得到 `LTChar`：

```
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar

for page in extract_pages("./pdfs/example.pdf"):
    for element in page:
        if isinstance(element, LTTextContainer):
            for text_line in element:
                for character in text_line:
                    if isinstance(character, LTChar):
                        print(character.get_text())
                        print(character.fontname)
                        print(character.size)
        else:
            print(element)
```

#### 布局分析

PDF 文件和 `.txt` 或 Word 在格式上有着很大的不同，它不包含任何类似于段落、句子甚至单词的内容。它由一系列对象及其结构信息组成，这些对象共同描述一个或多个页面的外观，可能还附带有其他交互元素和更高级别的应用程序数据。这使得从 PDF 文件中提取有意义的文本片段变得困难，组成段落的字符与组成表格、页面底部或图表描述的字符没有任何区别。

上一节我们知道，通过 pdfminer.six 可以拿到元素的位置信息，通过这些位置信息我们可以重建句子或段落的布局。布局分析由三个不同阶段组成：将字符分组为单词和行，然后将行分组为框，最后以层次结构方式将文本框分组。这是一种最经典的基于规则的 **布局分析算法（Layout analysis algorithm）**。

布局分析依赖于几个重要参数，比如字符间距、行间距、行重叠等，这些参数都是 [LAParams 类](https://pdfminersix.readthedocs.io/en/latest/reference/composable.html#laparams) 的一部分。

更多说明请参考 [Converting a PDF file to text](https://pdfminersix.readthedocs.io/en/latest/topic/converting_pdf_to_text.html) 这篇文档。

### pypdfium2

[PDFium](https://pdfium.googlesource.com/pdfium/+/refs/heads/main) 被认为是开源世界中最高质量的 PDF 渲染引擎之一，它最初是基于福昕软件（Foxit Software）的 PDF SDK 开发的，在 2014 年被 Google 开源。PDFium 支持多种操作系统，包括 Windows、macOS、Linux 等，它还被编译到 iOS、Android 等移动平台上，支持跨平台应用；除了基本的 PDF 渲染功能，PDFium 还支持生成、编辑、文本提取、搜索、注解、表单填充等高级功能。PDFium 是一个高效、可靠的 PDF 渲染引擎，广泛应用于 Chrome 浏览器和其他第三方项目中。其开源性质和丰富的功能使其成为处理 PDF 文档的理想选择，由于基于 C++ 开发，处理大文件速度优于纯 Python 库。

pypdfium2 是 PDFium 库的 Python 3 绑定，它提供了一些辅助方法简化 PDFium 库的使用，同时原始的 PDFium/ctypes API 仍然可访问。下面的示例代码演示了如何通过 pypdfium2 的 `get_text_bounded()` 方法将 PDF 中的文本提取出来：

```
import pypdfium2 as pdfium

pdf = pdfium.PdfDocument("./pdfs/example.pdf")
for i in range(len(pdf)):
    print('----- Page %d -----' % (i+1))
    page = pdf[i]
    textpage = page.get_textpage()
    text_all = textpage.get_text_bounded()
    print(text_all)
```

和 pdfminer.six 一样，我们也可以通过 `get_rect()` 获取每个文本块的位置：

```
textpage = page.get_textpage()
rect_count = textpage.count_rects()
print(rect_count)
for i in range(rect_count):
    rect = textpage.get_rect(i)
    print(rect)
    text = textpage.get_text_bounded(rect[0], rect[1], rect[2], rect[3])
    print(text)
```

得到文本块的位置后，就可以使用布局分析算法对版面进行分析，比如行检测（通过 Y 坐标差异判断是否在同一行）、列检测（通过 X 坐标差异判断是否属于同一列）或表格边界检测等等。

此外，PDFium 还提供了一个 `render()` 方法，可以方便地将 PDF 转换为图片：

```
bitmap = page.render(
    scale = 1,    # 72dpi resolution
    rotation = 0, # no additional rotation
)
pil_image = bitmap.to_pil()
pil_image.save('x.png')
```

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
