import trafilatura

html = """
<html><body>
<nav>首页 | 产品 | 文档 | 关于我们</nav>
<div class="sidebar">热门文章：如何选购 GPU | 2026 年显卡天梯</div>
<article>
  <h1>大模型训练的数据从哪来</h1>
  <p>训练大模型的第一步是收集语料，公开网页是最大的来源。</p>
  <p>原始网页里混着导航栏、广告和页脚，需要先抽取正文。</p>
</article>
<footer>© 2026 某公司 版权所有 | 隐私政策 | 联系我们</footer>
</body></html>
"""

print(trafilatura.extract(html, favor_precision=True))
