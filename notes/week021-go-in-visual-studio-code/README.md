# WEEK021 - 使用 Visual Studio Code 进行 Go 开发

[Visual Studio Code](https://code.visualstudio.com/)（简称 VS Code）是微软于 2015 年 4 月在微软开发者大会（Microsoft Build 2015）上开源的一款非常优秀的跨平台源代码编辑器，它不仅原生支持 JavaScript、TypeScript、CSS 和 HTML，而且可以通过强大的插件系统支持其他任意的编程语言，比如：[Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)、[Java](https://marketplace.visualstudio.com/items?itemName=vscjava.vscode-java-pack)、[C/C++](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools)、[Go](https://marketplace.visualstudio.com/items?itemName=golang.Go) 等等。你可以在 [插件市场](https://marketplace.visualstudio.com/vscode) 找到更多其他的插件。通过统一的接口模型，VS Code 为不同的编程语言提供了统一的编程体验，你再也不需要在不同语言的 IDE 之间来回切换了。

VS Code 为不同的编程语言提供了如下通用的语言特性：

* 语法高亮（Syntax highlighting）、括号匹配（Bracket matching）
* 代码自动补全（IntelliSense）
* 语法检查（Linting and corrections）
* 代码导航（Go to Definition, Find All References）
* 调试
* 重构

VS Code 使用 [Monaco Editor](https://microsoft.github.io/monaco-editor/) 作为其底层的代码编辑器，不仅可以跨平台使用，而且还可以通过浏览器在线使用，你可以访问 [vscode.dev](https://vscode.dev/)，操作界面和桌面版几乎是一样的。在 2019 年的 Stack Overflow 组织的开发者调查中，VS Code 被认为是最受开发者欢迎的开发环境。

## 安装 Go 插件

[Go 语言](https://go.dev/) 又被称为 Golang，是 Google 开发的一种静态强类型、编译型、并发型，并具有垃圾回收功能的编程语言。它于 2007 年 9 月开始设计，并在 2009 年 11 月正式发布并完全开源，至今已有 13 年的历史了。目前的 Go 语言在国内外的技术社区都非常热门，并诞生了很多著名的开源项目，如 Kubernetes、etcd 和 Prometheus 等，在近年来热门的微服务架构和云原生技术的发展中起到了举足轻重的作用。

在这篇笔记中，我们将学习如何在 VS Code 中进行 Go 语言的开发。

首先打开官网的 [Download and install](https://go.dev/doc/install) 页面，按照提示的步骤下载并安装 Go 语言开发环境。

然后在 VS Code 中安装 [Go 插件](https://marketplace.visualstudio.com/items?itemName=golang.go)：

![](./images/go-extension.png)

此时，我们只需要打开以 `.go` 结尾的文件，就可以激活该插件，左下角会显示出 [Go 的状态栏](https://github.com/golang/vscode-go/wiki/ui#using-the-go-status-bar)，并在状态栏上可以看到当前使用的 Go 版本：

![](./images/status-bar-menu.png)

另外，这个插件还依赖 [一些 Go 工具](https://github.com/golang/vscode-go/wiki/tools)，比如 [gopls](https://golang.org/s/gopls)、[dlv](https://github.com/go-delve/delve) 等。gopls 是 Go 官方的 language server，dlv 使用 Delve 进行 Go 语言的调试和测试，都是开发过程中必不可少的组件。如果其中任何一个工具缺失，VS Code 下面的状态栏就会弹出 `⚠️ Analysis Tools Missing` 的警告提示，点击提示将自动下载安装这些工具：

![](./images/install-tools.gif)

安装完成后，一切准备就绪，就可以开始我们的 Go 语言之旅了。

> You are ready to Go :-)

从这里可以看到 Go 插件支持的 [所有特性](https://github.com/golang/vscode-go/wiki/features)。

## Go 入门示例

这一节我们将演示如何在 VS Code 中开发一个 Go 项目。首先创建一个空目录 `demo`，并在 VS Code 中打开它。然后我们新建一个终端，输入下面的命令创建一个 Go 模块（`module`）：

```
$ go mod init example.com/demo
go: creating new go.mod: module example.com/demo
```

运行成功后，可以发现创建了一个 `go.mod` 文件，这个文件类似于 Maven 项目中 `pom.xml` 文件，用于管理项目依赖的模块。早期的版本中，Go 语言是没有依赖管理功能的，所有依赖的第三方包都放在 `GOPATH` 目录下，这就导致了同一个包只能保存一个版本，如果不同的项目依赖同一个包的不同版本，该怎么办呢？

于是 Go 语言从 v1.5 版本开始引入 `vendor` 模式，如果项目目录下有 `vendor` 目录，那么 Go 会优先使用 `vendor` 内的包，可以使用 [godep](https://github.com/tools/godep) 或 [dep](https://github.com/golang/dep) 来管理 `vender` 模式下的依赖包。

不过从 v1.11 版本开始，官方又推出了 `Go module` 功能，并在 v1.13 版本中作为 Go 语言默认的依赖管理工具。使用 `Go module` 依赖管理会在项目根目录下生成 `go.mod` 和 `go.sum` 两个文件。

我们打开 `go.mod` 这个文件，目前内容还比较简单，只是定义了当前的模块名以及使用的 Go 版本：

```
module example.com/demo

go 1.19
```

接下来我们在项目中创建一个 包（`package`），也就是一个目录，比如 `hello`，并在该目录下创建一个文件 `hello.go`，打开这个文件时会激活 Go 插件。等插件加载完毕，我们就可以编写 Go 代码了，在文件中输入如下内容：

```go
package hello

func SayHello() string {
	return "Hello world"
}
```

第一行使用 `package` 声明包，然后下面通过 `func` 定义了一个 `SayHello() string` 方法，注意在 Go 语言中类型是写在方法名后面的。

接下来，在项目根目录下创建一个 `main.go` 文件，内容如下：

```go
package main

import (
	"fmt"

	"example.com/demo/hello"
)

func main() {
	fmt.Println(hello.SayHello())
}
```

第一行依然是使用 `package` 来声明包，每个 `.go` 文件都需要声明包，只不过包名不同；然后使用 `import` 导入我们要使用的包，这里我们使用了 `fmt` 这个系统包，它是用于打印输出的，还使用了我们上面创建的 `example.com/demo/hello` 这个包，这样我们就可以调用其他包里的方法了；最后通过 `func` 定义了一个 `main()` 方法，这个方法是整个程序的入口。

就这样一个简单的示例项目就完成了。我们打开终端，输入 `go run` 命令即可运行程序：

```
$ go run main.go
Hello world
```

或者使用 `go build` 将代码编译为可执行程序：

```
$ go build main.go
```

运行生成的可执行程序：

```
$ ./main
Hello world
```

## 引用三方包

上面的例子中我们只使用了系统包和自己代码中的包，如果要使用第三方包该怎么办呢？

我们可以使用 `go get` 下载第三方包并将依赖更新到 `go.mod` 文件中，比如我们要添加 [rsc.io/quote](https://pkg.go.dev/rsc.io/quote) 这个依赖包，执行如下命令：

```
$ go get rsc.io/quote
go: downloading rsc.io/quote v1.5.2
go: added golang.org/x/text v0.0.0-20170915032832-14c0d48ead0c
go: added rsc.io/quote v1.5.2
```

这个命令默认会从 Go 官方的模块代理（https://proxy.golang.org）下载依赖包，如果遇到网络问题，可以使用下面的命令改为国内的代理（https://goproxy.cn）：

```
$ go env -w GOPROXY=https://goproxy.cn,direct
```

`go get` 命令执行成功后，重新打开 `go.mod` 文件，可以看到自动添加了依赖：

```
require (
	golang.org/x/text v0.0.0-20170915032832-14c0d48ead0c // indirect
	rsc.io/quote v1.5.2 // indirect
	rsc.io/sampler v1.3.0 // indirect
)
```

这时我们就可以在代码中使用 `rsc.io/quote` 这个包了：

```
package main

import (
	"fmt"

	"example.com/demo/hello"
	"rsc.io/quote"
)

func main() {
	fmt.Println(hello.SayHello())
	fmt.Println(quote.Go())
}
```

重新运行程序：

```
$ go run main.go
Hello world
Don't communicate by sharing memory, share memory by communicating.
```

## 编写单元测试

这一节我们使用 Go 语言的标准库 `testing` 对我们的代码进行单元测试。Go 语言推荐将测试文件和源代码文件放在一起，测试文件以 `_test.go` 结尾，比如我们要对上面的 `hello.go` 编写单元测试，可以在同目录创建一个 `hello_test.go` 文件，文件内容如下：

```go
package hello_test

import (
	"testing"

	"example.com/demo/hello"
)

func TestSayHello(t *testing.T) {
	if hello.SayHello() != "Hello world" {
		t.Fatal("Not good")
	}
}
```

测试用例名称一般命名为 Test 加上待测试的方法名，比如这里的 `TestSayHello` 是对 `SayHello` 的测试，测试用的参数有且只有一个，在这里是 `t *testing.T`，表示这是一个单元测试，如果是基准测试，这个参数类型为 `*testing.B`。

VS Code 会自动识别单元测试的包和方法，并在包和方法上显示一个链接：

![](./images/unit-test.png)

我们可以点击方法上的 `run test` 或 `debug test` 来执行测试，或者使用 `go test` 命令来执行，由于这个测试是写在 `hello` 这个目录下，我们需要进入该目录执行测试：

```
$ cd hello
$ go test
PASS
ok      example.com/demo/hello  0.277s
```

这里有一点需要特别注意，我们在这个文件的最顶部声明包时用的是 `package hello_test`，而不是 `package hello`，其实两种方法都可以，这取决于你编写的是黑盒测试还是白盒测试。如果你使用 `package hello`，那么在单元测试代码中就可以对私有方法进行测试，相当于白盒测试，而这里我们使用的是黑盒测试，也就是只对包里公共方法进行测试。

## 调试 Go 程序

在上面的单元测试方法上面有一个 `debug test` 链接，点击该链接就可以调试 Go 程序了。如果要以调试模式启动 `main()` 函数，可以打开 `main.go` 文件，使用 F5 快捷键启动调试器。

![](./images/go-debugging.png)

或者打开 VS Code 的 “运行和调试” 侧边栏，然后点击 “运行和调试” 按钮也可以启动调试器。如果调试器启动成功，我们可以在下方的调试控制台看到类似这样的输出：

```
Starting: C:\Users\aneasystone\go\bin\dlv.exe dap --check-go-version=false --listen=127.0.0.1:60508 from d:\code\weekly-practice\notes\week021-go-in-visual-studio-code\demo
DAP server listening at: 127.0.0.1:60508
```

Go 语言的官方调试器是 [dlv](https://github.com/go-delve/delve/blob/master/Documentation/usage/dlv.md)，它的全称为 `Delve`，VSCode 通过运行 [dlv dap](https://github.com/go-delve/delve/blob/master/Documentation/usage/dlv_dap.md) 命令来启动 Go 语言的调试器，这个命令会在本地启动一个 TCP 服务器，并通过 [DAP 协议（Debug Adaptor Protocol）]((https://microsoft.github.io/debug-adapter-protocol/)) 和 VS Code 进行通信实现调试的功能。

使用 F5 快捷键或 “运行和调试” 按钮时，VS Code 会使用默认配置对当前打开的文件进行调试。如果想修改配置参数，我们可以创建一个 `launch.json` 配置文件：

![](./images/create-launch-json.png)

点击 “创建 launch.json 文件” 按钮会弹出一个下拉框，我们可以：

* 调试一个包（Launch Package）
* 附加到本地进程（Attach to local process）
* 连接到远程服务（Connect to server）

我们选择第一个，创建的 `launch.json` 配置文件如下：

```json
{
	"version": "0.2.0",
	"configurations": [
		{
			"name": "Launch Package",
			"type": "go",
			"request": "launch",
			"mode": "auto",
			"program": "${fileDirname}"
		}
	]
}
```

我们将 `${fileDirname}` 变量修改为 `.`，表示项目的根目录。这样我们就可以在打开任意文件的时候快速调试 `main()` 方法了，而不用每次都打开 `main.go` 文件来调试。如果我们需要对调试器进行配置，比如配置命令行参数启动（`args`），修改当前工作目录（`cwd`），配置 dlv 调试器（`dlvFlags`）等等，我们在 `launch.json` 中输入引号后 VS Code 会自动提示所有支持的配置项：

![](./images/create-launch-json-args.png)

这些配置项的含义可以参考 [Launch.json Attributes](https://github.com/golang/vscode-go/wiki/debugging#launchjson-attributes)。

## 参考

1. [Go in Visual Studio Code](https://code.visualstudio.com/docs/languages/go)
1. [VSCode Go Wiki](https://github.com/golang/vscode-go/wiki)
1. [Go Documentation](https://go.dev/doc/)
1. [Getting started with VS Code Go](https://www.youtube.com/watch?v=1MXIGYrMk80)
1. [Go语言之依赖管理](https://www.liwenzhou.com/posts/Go/go_dependency/)
1. [Go Test 单元测试简明教程](https://geektutu.com/post/quick-go-test.html)
1. [Proper package naming for testing with the Go language](https://stackoverflow.com/questions/19998250/proper-package-naming-for-testing-with-the-go-language/31443271)
1. [Debug Go programs in VS Code](https://github.com/golang/vscode-go/wiki/debugging)
