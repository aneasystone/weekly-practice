# WEEK033 - gRPC 快速入门

[RPC](https://en.wikipedia.org/wiki/Remote_procedure_call) 又被称为 **远程过程调用**，英文全称为 **Remote Procedure Call**，是一种服务间的通信规范，它可以让你像调用本地方法一样调用远程服务提供的方法，而不需要关心底层的通信细节。RPC 的概念早在上个世纪七八十年代就已经被提出，1984 年，Birrell 和 Nelson 在 ACM Transactions on Computer Systems 期刊上发表了一篇关于 RPC 的经典论文 [Implementing remote procedure calls](https://www.cs.cmu.edu/~dga/15-712/F07/papers/birrell842.pdf)，论文中首次给出了实现 RPC 的基本框架：

![](./images/rpc.png)

从这个框架中可以看到很多现代 RPC 框架的影子，比如客户端和服务端的 Stub、序列化和反序列化等，事实上，所有后来的 RPC 框架几乎都是源自于这个原型。

不过在那个年代，RPC 的争议是非常大的，由于网络环境的不可靠性，RPC 永远都不可能做到像调用本地方法一样。大家提出了一堆问题，比如：故障恢复、请求重试、异步请求、服务寻址等，在那个互联网都还没有出现的年代，一堆大神们就已经在讨论分布式系统间的调用问题了，而他们讨论的问题焦点，基本上都演变成了 RPC 历史中永恒的话题。

为了解决这些问题，软件架构经历了一代又一代的发展和演进。1988 年，Sun 公司推出了第一个商业化的 RPC 库 [Sun RPC](https://web.cs.wpi.edu/~rek/DCS/D04/SunRPC.html) ，并被定义为标准的 RPC 规范；1991 年，非营利性组织 OMG 发布 [CORBA](https://www.omg.org/spec/CORBA/)，它通过接口定义语言 IDL 中的抽象类型映射让异构环境之间的互操作成为了可能；不过由于其复杂性，很快就被微软推出的基于 XML 的 [SOAP](https://www.w3schools.com/xml/xml_soap.asp) 技术所打败，随后 SOAP 作为 W3C 标准大大推动了 Web Service 概念的发展；像 SOAP 这种基于 XML 的 RPC 技术被称为 [XML-RPC](https://en.wikipedia.org/wiki/XML-RPC)，它最大的问题是 XML 报文内容过于冗余，对 XML 的解析效率也很低，于是 JSON 应运而生，进而导致 RESTful 的盛行；不过无论是 XML 还是 JSON，都是基于文本传输，性能都无法让人满意，直到 2008 年，Google 开源 [Protocol Buffers](https://protobuf.dev/)，这是一种高效的结构化数据存储格式，可以用于结构化数据的序列化，非常适合做数据存储或 RPC 数据交换格式；可能是由于微服务的流行，之后的 RPC 框架如雨后春笋般蓬勃发展，同年，Facebook 向 Apache 贡献了开源项目 [Thrift](https://thrift.apache.org/)，2009 年，Hadoop 之父 Doug Cutting 开发出 [Avro](https://avro.apache.org/)，成为 Hadoop 的一个子项目，随后又脱离 Hadoop 成为 Apache 顶级项目；2011 年，阿里也开源了它自研的 RPC 框架 [Dubbo](https://cn.dubbo.apache.org/zh-cn/)，和前两个一样，最后也贡献给了 Apache；2015 年，Google 开源 [gRPC](https://grpc.io) 框架，开创性地使用 HTTP/2 作为传输协议，基于 HTTP/2 的多路复用和服务端推送技术，gRPC 支持双向流式通信，这使得 RPC 框架终于不再拘泥于万年不变的 C/S 模型了。

2017 年，gRPC 作为孵化项目成为 CNCF 的一员，不论是 Envoy 还是 Istio 等 Service Mesh 方案，都将 gRPC 作为一等公民，可以预见的是，谷歌正在将 gRPC 打造成云原生时代通信层事实上的标准。

## 从 `Hello World` 开始

## 参考

* [gRPC 官方文档](https://grpc.io/docs/guides/)
* [gRPC 官方文档中文版](https://doc.oschina.net/grpc)
* [Awesome gRPC](https://github.com/grpc-ecosystem/awesome-grpc)
* [gRPC教程](https://www.liwenzhou.com/posts/Go/gRPC/)
* [那些年，我们追过的RPC](https://zhuanlan.zhihu.com/p/29028054)
* [RPC 发展史](https://cloud.tencent.com/developer/article/1864288)
* [GRPC简介](https://zhuanlan.zhihu.com/p/411315625)
* [怎么看待谷歌的开源 RPC 框架 gRPC？](https://www.zhihu.com/question/30027669)
