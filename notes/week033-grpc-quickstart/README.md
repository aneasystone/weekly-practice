# WEEK033 - gRPC 快速入门

[RPC](https://en.wikipedia.org/wiki/Remote_procedure_call) 又被称为 **远程过程调用**，英文全称为 **Remote Procedure Call**，是一种服务间的通信规范，它可以让你像调用本地方法一样调用远程服务提供的方法，而不需要关心底层的通信细节。RPC 的概念早在上个世纪七八十年代就已经被提出，1984 年，Birrell 和 Nelson 在 ACM Transactions on Computer Systems 期刊上发表了一篇关于 RPC 的经典论文 [Implementing remote procedure calls](https://www.cs.cmu.edu/~dga/15-712/F07/papers/birrell842.pdf)，论文中首次给出了实现 RPC 的基本框架：

![](./images/rpc.png)

从这个框架中可以看到很多现代 RPC 框架的影子，比如客户端和服务端的 Stub、序列化和反序列化等，事实上，所有后来的 RPC 框架几乎都是源自于这个原型。

不过在那个年代，RPC 的争论是非常大的，由于网络环境的不可靠性，RPC 永远都不可能做到像调用本地方法一样。大家提出了一堆问题，比如：故障恢复、请求重试、异步请求、服务寻址等，在那个互联网都还没有出现的年代，一堆大神们就已经在讨论分布式系统间的调用问题了，而他们讨论的问题焦点，基本上都演变成了 RPC 历史中永恒的话题。

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
