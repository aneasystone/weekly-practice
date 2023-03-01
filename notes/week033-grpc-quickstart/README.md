# WEEK033 - gRPC 快速入门

[RPC](https://en.wikipedia.org/wiki/Remote_procedure_call) 又被称为 **远程过程调用**，英文全称为 **Remote Procedure Call**，是一种服务间的通信规范，它可以让你像调用本地方法一样调用远程服务提供的方法，而不需要关心底层的通信细节。RPC 的概念早在上个世纪七八十年代就已经被提出，1984 年，Birrell 和 Nelson 在 ACM Transactions on Computer Systems 期刊上发表了一篇关于 RPC 的经典论文 [Implementing remote procedure calls](https://www.cs.cmu.edu/~dga/15-712/F07/papers/birrell842.pdf)，论文中首次给出了实现 RPC 的基本框架：

![](./images/rpc.png)

从这个框架中可以看到很多现代 RPC 框架的影子，比如客户端和服务端的 Stub、序列化和反序列化等，事实上，所有后来的 RPC 框架几乎都是源自于这个原型。

不过在那个年代，RPC 的争议是非常大的，由于网络环境的不可靠性，RPC 永远都不可能做到像调用本地方法一样。大家提出了一堆问题，比如：故障恢复、请求重试、异步请求、服务寻址等，在那个互联网都还没有出现的年代，一堆大神们就已经在讨论分布式系统间的调用问题了，而他们讨论的问题焦点，基本上都演变成了 RPC 历史中永恒的话题。

为了解决这些问题，软件架构经历了一代又一代的发展和演进。1988 年，Sun 公司推出了第一个商业化的 RPC 库 [Sun RPC](https://web.cs.wpi.edu/~rek/DCS/D04/SunRPC.html) ，并被定义为标准的 RPC 规范；1991 年，非营利性组织 OMG 发布 [CORBA](https://www.omg.org/spec/CORBA/)，它通过接口定义语言 IDL 中的抽象类型映射让异构环境之间的互操作成为了可能；不过由于其复杂性，很快就被微软推出的基于 XML 的 [SOAP](https://www.w3schools.com/xml/xml_soap.asp) 技术所打败，随后 SOAP 作为 W3C 标准大大推动了 Web Service 概念的发展；像 SOAP 这种基于 XML 的 RPC 技术被称为 [XML-RPC](https://en.wikipedia.org/wiki/XML-RPC)，它最大的问题是 XML 报文内容过于冗余，对 XML 的解析效率也很低，于是 JSON 应运而生，进而导致 RESTful 的盛行；不过无论是 XML 还是 JSON，都是基于文本传输，性能都无法让人满意，直到 2008 年，Google 开源 [Protocol Buffers](https://protobuf.dev/)，这是一种高效的结构化数据存储格式，可以用于结构化数据的序列化，非常适合做数据存储或 RPC 数据交换格式；可能是由于微服务的流行，之后的 RPC 框架如雨后春笋般蓬勃发展，同年，Facebook 向 Apache 贡献了开源项目 [Thrift](https://thrift.apache.org/)，2009 年，Hadoop 之父 Doug Cutting 开发出 [Avro](https://avro.apache.org/)，成为 Hadoop 的一个子项目，随后又脱离 Hadoop 成为 Apache 顶级项目；2011 年，阿里也开源了它自研的 RPC 框架 [Dubbo](https://cn.dubbo.apache.org/zh-cn/)，和前两个一样，最后也贡献给了 Apache；2015 年，Google 开源 [gRPC](https://grpc.io) 框架，开创性地使用 HTTP/2 作为传输协议，基于 HTTP/2 的多路复用和服务端推送技术，gRPC 支持双向流式通信，这使得 RPC 框架终于不再拘泥于万年不变的 C/S 模型了。

2017 年，gRPC 作为孵化项目成为 CNCF 的一员，不论是 Envoy 还是 Istio 等 Service Mesh 方案，都将 gRPC 作为一等公民，可以预见的是，谷歌正在将 gRPC 打造成云原生时代通信层事实上的标准。

## 从 `Hello World` 开始

这一节我们使用 Go 语言实现一个简单的 `Hello World` 服务，学习 gRPC 的基本概念。首先，我们通过 `go mod init` 初始化示例项目：

```
$ mkdir demo && cd demo
$ go mod init example.com/demo
go: creating new go.mod: module example.com/demo
go: to add module requirements and sums:
        go mod tidy
```

然后获取 `grpc` 依赖：

```
$ go get google.golang.org/grpc@latest
go: downloading golang.org/x/net v0.5.0
go: downloading golang.org/x/sys v0.4.0
go: downloading google.golang.org/genproto v0.0.0-20230110181048-76db0878b65f
go: downloading golang.org/x/text v0.6.0
go: added github.com/golang/protobuf v1.5.2
go: added golang.org/x/net v0.5.0
go: added golang.org/x/sys v0.4.0
go: added golang.org/x/text v0.6.0
go: added google.golang.org/genproto v0.0.0-20230110181048-76db0878b65f
go: added google.golang.org/grpc v1.53.0
go: added google.golang.org/protobuf v1.28.1
```

### 编写 `.proto` 文件

正如前文所述，Google 在 2009 年开源了一种高效的结构化数据存储格式 - [Protocol Buffers](https://protobuf.dev/)，这种格式非常适合用于 RPC 的数据交换，所以顺理成章的，Google 在开发 gRPC 时就采用了 Protocol Buffers 作为默认的数据格式。不过要注意的是 Protocol Buffers 不仅仅是一种数据格式，而且也是一种 **IDL**（Interface Description Language，接口描述语言），它通过一种中立的方式来描述接口和数据类型，从而实现跨语言和跨平台开发。

一般使用 `.proto` 后缀的文件来定义接口和数据类型，所以接下来，我们要创建一个 `hello.proto` 文件，我们将其放在 `proto` 目录下：

```
$ mkdir proto
$ vim hello.proto
```

文件内容如下：

```
syntax = "proto3";

option go_package = "example.com/demo/proto";

service HelloService {
  rpc SayHello (HelloRequest) returns (HelloResponse) {}
}

message HelloRequest {
  string name = 1;
}

message HelloResponse {
  string message = 1;
}
```

我们在第一行指定使用 `proto3` 语法，这是目前推荐的版本，如果不指定，默认将使用 `proto2`，可能会导致一些版本兼容性的问题。随后我们用关键字 `service` 定义了一个 `HelloService` 服务，该服务包含一个 `SayHello` 方法，方法的入参为 `HelloRequest`，出参为 `HelloResponse`，这两个消息类型都在后面通过关键字 `message` 所定义。Protocol Buffers 的语法非常直观，也比较容易理解，这里只是使用了一些简单的语法，其他更复杂的语法可以参考 [Protocol Buffers 的官方文档](https://protobuf.dev/programming-guides/proto3/)，另外这里有一份 [中文语法指南](https://www.liwenzhou.com/posts/Go/Protobuf3-language-guide-zh/) 也可供参考。

编写好 `hello.proto` 文件之后，我们还需要一些工具将其转换为 Go 语言。这些工具包括：

* `protoc`
* `protoc-gen-go`
* `protoc-gen-go-grpc`

`protoc` 是 Protocol Buffers 编译器，用于将 `.proto` 文件转换为其他编程语言，而不同语言的转换工作由不同语言的插件来实现。Go 语言的插件有两个：`protoc-gen-go` 和 `protoc-gen-go-grpc`，插件 `protoc-gen-go` 会生成一个后缀为 `.pb.go` 的文件，其中包含 `.proto` 文件中定义数据类型和其序列化方法；插件 `protoc-gen-go-grpc` 会生成一个后缀为 `_grpc.pb.go` 的文件，其中包含供客户端调用的服务方法和服务器要实现的接口类型。

`protoc` 可以从 Protocol Buffers 的 [Release 页面](https://github.com/protocolbuffers/protobuf/releases) 下载，下载后将 bin 目录添加到 PATH 环境变量即可：

```
$ curl -LO https://github.com/protocolbuffers/protobuf/releases/download/v22.0/protoc-22.0-linux-x86_64.zip
```

`protoc-gen-go` 和 `protoc-gen-go-grpc` 两个插件可以通过 `go install` 命令直接安装：

```
$ go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.28.1
$ go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.2.0
```

安装完成后使用 `--version` 参数检测各个命令是否正常：

```
$ protoc --version
libprotoc 22.0

$ protoc-gen-go --version
protoc-gen-go v1.28.1

$ protoc-gen-go-grpc --version
protoc-gen-go-grpc 1.2.0
```

一切就绪后，就可以使用下面这行命令生成相应的 Go 代码了：

```
$ cd proto
$ protoc --go_out=. --go_opt=paths=source_relative \
	--go-grpc_out=. --go-grpc_opt=paths=source_relative \
	hello.proto
```

这个命令在当前目录下生成了 `hello.pb.go` 和 `hello_grpc.pb.go` 两个文件。

### 实现服务端

### 测试服务端

### 实现客户端

## gRPC 的四种形式

## 参考

* [gRPC 官方文档](https://grpc.io/docs/guides/)
* [gRPC 官方文档中文版](https://doc.oschina.net/grpc)
* [Awesome gRPC](https://github.com/grpc-ecosystem/awesome-grpc)
* [gRPC教程](https://www.liwenzhou.com/posts/Go/gRPC/)
* [Protocol Buffers V3中文语法指南[翻译]](https://www.liwenzhou.com/posts/Go/Protobuf3-language-guide-zh/)
* [那些年，我们追过的RPC](https://zhuanlan.zhihu.com/p/29028054)
* [RPC 发展史](https://cloud.tencent.com/developer/article/1864288)
* [GRPC简介](https://zhuanlan.zhihu.com/p/411315625)
* [怎么看待谷歌的开源 RPC 框架 gRPC？](https://www.zhihu.com/question/30027669)
