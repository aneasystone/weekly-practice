# WEEK025 - WebAssembly 学习笔记

[WebAssembly](https://webassembly.org/)（简称 WASM）是一种以安全有效的方式运行可移植程序的新兴 Web 技术，它的开发团队来自 Mozilla、Google、Microsoft 和 Apple，分别代表着四大网络浏览器 Firefox、Chrome、Microsoft Edge 和 Safari，从 2017 年 11 月开始，这四大浏览器就开始实验性的支持 WebAssembly。当时 WebAssembly 还没有形成标准，这么多的浏览器开发商对某个尚未标准化的技术达成如此一致的意见，这在历史上是很罕见的，可以看出这绝对是一项值得关注的技术，被号称为 `the future of web development`。

WebAssembly 在 2019 年 12 月 5 日被万维网联盟（W3C）推荐，与 HTML，CSS 和 JavaScript 一起，成为 Web 的第四种语言。

## 关于历史

JavaScript 诞生于 1995 年 5 月，一个让人津津乐道的故事是，当时刚加入网景的 [Brendan Eich](https://zh.wikipedia.org/wiki/%E5%B8%83%E8%98%AD%E7%99%BB%C2%B7%E8%89%BE%E5%85%8B) 仅仅花了十天时间就开发出了 JavaScript 语言。开发 JavaScript 的初衷是为 HTML 提供一种脚本语言使得网页变得更动态，当时根本就没有考虑什么浏览器兼容性、安全性、移植性这些东西，对性能也没有特别的要求。但随着 Web 技术的发展，网页要解决的问题已经远不止简单的文本信息，而是包括了更多的高性能图像处理和 3D 渲染等方面，这时，JavaScript 的性能问题就凸显出来了。于是，如何让 JavaScript 执行的更快，变成了各大浏览器生产商争相竞逐的目标。

https://www.sohu.com/a/145566886_505793

https://stackoverflow.com/questions/44931479/compiling-vs-transpiling

https://web.archive.org/web/20221013220648/https://techcrunch.com/2015/06/17/google-microsoft-mozilla-and-others-team-up-to-launch-webassembly-a-new-binary-format-for-the-web/

https://web.archive.org/web/20220801052932/https://brendaneich.com/2015/06/from-asm-js-to-webassembly/

https://web.archive.org/web/20170327132956/https://arstechnica.com/information-technology/2013/05/native-level-performance-on-the-web-a-brief-examination-of-asm-js/

https://web.archive.org/web/20170320002809/https://arstechnica.com/information-technology/2015/06/the-web-is-getting-its-bytecode-webassembly/

https://blog.csdn.net/weixin_43895948/article/details/119276306

https://blog.51cto.com/u_15087086/2598661

Chrome 从 2013 年开始支持 PNaCl（Portable Native Client），为开发者提供一种用于构建高性能 Web 应用的技术，但这项技术只有 Google 支持。

在这一背景下，Google 决定停止支持 PNaCl。Chromium 官方博客宣布，将在 2018 年第一季度移除对 PNaCl 的支持，表示 WebAssembly 生态系统更适合高性能 Web 应用。


https://www.zhihu.com/question/362649730

https://www.zhihu.com/question/31415286

https://www.jianshu.com/p/ad2769f4c32e

https://codechina.gitcode.host/programmer/2017/programmer-2017-55.html

https://juejin.cn/post/7052901106631999495

## 参考

1. [WebAssembly 官网](https://webassembly.org/)
1. [WebAssembly | MDN](https://developer.mozilla.org/en-US/docs/WebAssembly)
1. [WebAssembly 中文网](http://webassembly.org.cn/)
1. [WebAssembly System Interface](https://github.com/WebAssembly/WASI)
1. [WebAssembly Design Documents](https://github.com/WebAssembly/design)
1. [WebAssembly Specification](https://webassembly.github.io/spec/core/index.html)
1. [asm.js 和 Emscripten 入门教程](https://www.ruanyifeng.com/blog/2017/09/asmjs_emscripten.html)
1. [WebAssembly - 维基百科](https://zh.wikipedia.org/wiki/WebAssembly)
