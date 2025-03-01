import markdownify

html = '<p>这里是正文。</p><p>这里是正文。</p><p>这里是正文</p><h1>第一章</h1><p>这里是正文。</p><h2>第一节</h2><p>这里是正文。</p><h2>第二节</h2><p>这里是正文。</p><h1>第二章</h1><p>这里是正文。</p><h2>第一节</h2><p>这里是正文。</p><h2>第二节</h2><p>这里是正文。</p><table><tr><td><p>姓名</p></td><td><p>学号</p></td><td><p>学科</p></td><td><p>成绩</p></td></tr><tr><td><p>小明</p></td><td><p>001</p></td><td><p>语文</p></td><td><p>98</p></td></tr><tr><td><p>小明</p></td><td><p>001</p></td><td><p>数学</p></td><td><p>97</p></td></tr><tr><td><p>小华</p></td><td><p>002</p></td><td><p>语文</p></td><td><p>94</p></td></tr><tr><td><p>小华</p></td><td><p>002</p></td><td><p>数学</p></td><td><p>99</p></td></tr><tr><td><p>小红</p></td><td><p>003</p></td><td><p>语文</p></td><td><p>100</p></td></tr><tr><td><p>小红</p></td><td><p>003</p></td><td><p>数学</p></td><td><p>95</p></td></tr></table><p>101班成绩表</p><p><img src="data:image/png;base64,iVBORw0KGgoA+eOEKwCgJEjR6JSpUpWSwcRERERERERESmHASsiIiIqFa1Wi71798q+16JFC4wZM++ORkpICjUYDAPD19UX9+++/D1Ynzkmp3W/gAAAAAElFTkSuQmCC" /></p><p>这里是左侧文本。这里是左侧文本。这里是左侧文本。这里是左侧文本。这里是左侧文本。这里是左侧文本。这里是左侧文本。这里是左侧文本。这里是左侧文本。这里是左侧文本。这里是左侧文本。</p><p>这里是右侧文本。这里是右侧文本。这里是右侧文本。这里是右侧文本。这里是右侧文本。这里是右侧文本。这里是右侧文本。这里是右侧文本。这里是右侧文本。这里是右侧文本。这里是右侧文本。这里是右侧文本。这里是右侧文本。这里是右侧文本。这里是右侧文本。这里是右侧文本。这里是右侧文本。这里是右侧文本。</p>'

from bs4 import BeautifulSoup
soup = BeautifulSoup(html, "html.parser")
converter = markdownify.MarkdownConverter()
md = converter.convert_soup(soup)
print(md)