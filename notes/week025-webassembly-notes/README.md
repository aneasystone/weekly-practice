# WEEK025 - WebAssembly 学习笔记

[WebAssembly](https://webassembly.org/)（简称 WASM）是一种以安全有效的方式运行可移植程序的新兴 Web 技术，它的开发团队来自 Mozilla、Google、Microsoft 和 Apple，分别代表着四大网络浏览器 Firefox、Chrome、Microsoft Edge 和 Safari，从 2017 年 11 月开始，这四大浏览器就开始实验性的支持 WebAssembly。当时 WebAssembly 还没有形成标准，这么多的浏览器开发商对某个尚未标准化的技术达成如此一致的意见，这在历史上是很罕见的，可以看出这绝对是一项值得关注的技术，被号称为 `the future of web development`。

WebAssembly 在 2019 年 12 月 5 日被万维网联盟（W3C）推荐，与 HTML，CSS 和 JavaScript 一起，成为 Web 的第四种语言。

## WebAssembly 之前的历史

JavaScript 诞生于 1995 年 5 月，一个让人津津乐道的故事是，当时刚加入网景的 [Brendan Eich](https://zh.wikipedia.org/wiki/%E5%B8%83%E8%98%AD%E7%99%BB%C2%B7%E8%89%BE%E5%85%8B) 仅仅花了十天时间就开发出了 JavaScript 语言。开发 JavaScript 的初衷是为 HTML 提供一种脚本语言使得网页变得更动态，当时根本就没有考虑什么浏览器兼容性、安全性、移植性这些东西，对性能也没有特别的要求。但随着 Web 技术的发展，网页要解决的问题已经远不止简单的文本信息，而是包括了更多的高性能图像处理和 3D 渲染等方面，这时，JavaScript 的性能问题就凸显出来了。于是，如何让 JavaScript 执行的更快，变成了各大浏览器生产商争相竞逐的目标。

### 浏览器的性能之战

这场关于浏览器的性能之战在 2008 年由 Google 带头打响，这一年的 9 月 2 日，Google 发布了一款跨时代的浏览器 Chrome，具备简洁的用户界面和极致的用户体验，内置的 [V8](https://v8.dev/) 引擎采用了全新的 JIT 编译（Just-in-time compilation，即时编译）技术，使得浏览器的响应速度得到了几倍的提升。次年，Apple 发布了他们的浏览器新版本 Safari 4，其中引入新的 Nitro 引擎（也被称为 SquirrelFish 或 [JavaScriptCore](https://trac.webkit.org/wiki/JavaScriptCore)），同样使用的是 JIT 技术。紧接着，Mozilla 在 Firefox 3.5 中引入 [TraceMonkey](https://en.wikipedia.org/wiki/SpiderMonkey) 技术，Microsoft 在 2011 年也推出 [Chakra](https://en.wikipedia.org/wiki/Chakra_(JScript_engine)) 引擎。

JIT 技术的推出大大提高了 JavaScript 的性能：

![](./images/jit-performance.png)

随着性能的提升，JavaScript 的应用范围也得到了极大的扩展，Web 内容变得更加丰富，图片、视频、游戏，等等等等，甚至有人将 JavaScript 用于后端开发（Node.js）。不过由于 JavaScript 动态类型和解释执行的特性，它天生在性能上存在着缺陷，通过 JIT 的优化很快就遇到了瓶颈。但是日益丰富的 Web 内容对 JavaScript 的性能提出了更高的要求，尤其是 3D 游戏，这些游戏在 PC 上跑都很吃力，更别说在浏览器里运行了。

如何让 JavaScript 执行地更快，是摆在各大浏览器生产商面前的一大难题，很快，Google 和 Mozilla 交出了各自的答卷。

### Google 的 NaCl 解决方案

Google 在 2008 年开源了 [NaCl 技术](https://developer.chrome.com/docs/native-client/nacl-and-pnacl/)，并在 2011 年的 Chrome 14 中正式启用。NaCl 的全称为 Native Client，这是一种可以在浏览器中执行原生代码（native code）的技术，听起来很像是 Microsoft 当时所使用的 [ActiveX](https://en.wikipedia.org/wiki/ActiveX) 技术，不过 ActiveX 由于其安全性一直被人所诟病。而 NaCl 定义了一套原生代码的安全子集，执行于独立的沙盒环境之中，并通过一套被称为 PPAPI（Pepper Plugin API）的接口来和 JavaScript 交互，避免了可能的安全问题。NaCl 采取了和 JIT 截然不同的 AOT 编译（Ahead-of-time compilation，即提前编译）技术，所以在性能上的表现非常突出，几乎达到了和原生应用一样的性能。不过由于 NaCl 应用是 C/C++ 语言编写的，与 CPU 架构强关联，不具有可移植性，因此需要针对不同的平台进行开发以及编译，用户使用起来非常痛苦。

为了解决这个问题，Google 在 2013 年又推出了 PNaCl 技术（Portable Native Client），PNaCl 的创新之处在于使用 [LLVM IR](https://llvm.org/docs/LangRef.html)（Intermediate Representation）来分发应用，而不是直接分发原生代码，LLVM IR 也被称为 Bitcode，它是一种平台无关的中间语言表示，实现了和 Java 一样的目标：一次编译，到处运行。

如果我们站在今天的视角来看，PNaCl 这项技术是非常超前的，它的核心理念和如今的 WebAssembly 如出一辙，只不过它出现的时机不对，当时很多人都对在浏览器中执行原生代码持怀疑态度，担心可能出现和 ActiveX 一样的安全问题，而且当时 HTML5 技术正发展的如火如荼，人们都在想着如何从浏览器中移除诸如 Flash 或 Java Applet 这些 JavaScript 之外的技术，所以 PNaCl 技术从诞生以来，一直不温不火，尽管后来 Firefox 和 Opera 等浏览器也开始支持 NaCl 和 PPAPI，但是一直无法得到普及（当时的 IE 还占领着浏览器市场的半壁江山）。

随着 WebAssembly 技术的发展，Google Chrome 最终在 2018 年移除了对 PNaCl 的支持，决定全面拥抱 WebAssembly 技术。

### Mozilla 的 asm.js 解决方案

https://www.sohu.com/a/145566886_505793

https://tate-young.github.io/2020/03/02/webassembly.html

http://www.ruanyifeng.com/blog/2017/09/asmjs_emscripten.html

https://web.archive.org/web/20170327132956/https://arstechnica.com/information-technology/2013/05/native-level-performance-on-the-web-a-brief-examination-of-asm-js/

https://en.wikipedia.org/wiki/Asm.js

https://webassembly.org/docs/faq/

https://stackoverflow.com/questions/44931479/compiling-vs-transpiling

https://web.archive.org/web/20221013220648/https://techcrunch.com/2015/06/17/google-microsoft-mozilla-and-others-team-up-to-launch-webassembly-a-new-binary-format-for-the-web/

https://web.archive.org/web/20220801052932/https://brendaneich.com/2015/06/from-asm-js-to-webassembly/

https://web.archive.org/web/20170320002809/https://arstechnica.com/information-technology/2015/06/the-web-is-getting-its-bytecode-webassembly/

https://blog.csdn.net/weixin_43895948/article/details/119276306

https://blog.51cto.com/u_15087086/2598661

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
1. [浏览器是如何工作的：Chrome V8 让你更懂JavaScript](https://king-hcj.github.io/2020/10/05/google-v8/)
1. [A crash course in just-in-time (JIT) compilers](https://hacks.mozilla.org/2017/02/a-crash-course-in-just-in-time-jit-compilers/)
1. [WebAssembly完全入门——了解wasm的前世今身](https://www.cnblogs.com/detectiveHLH/p/9928915.html)
1. [浅谈WebAssembly历史](https://github.com/ErosZy/md/blob/master/WebAssembly%E4%B8%93%E6%A0%8F/1.%E6%B5%85%E8%BF%B0WebAssembly%E5%8E%86%E5%8F%B2.md)
