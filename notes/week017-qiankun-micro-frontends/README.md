# WEEK017 - 使用 qiankun 开发微前端应用

[微前端（Micro Frontends）](https://micro-frontends.org/) 这个概念是在 2016 年底的时候在 [ThoughtWorks Technology Radar](https://www.thoughtworks.com/radar/techniques/micro-frontends) 上首次提出来的，它将服务端的微服务概念延伸到前端领域。随着应用规模的不断变大，传说中的 SPA（单页面应用）会变得越来越复杂，也越来越难以维护。这样大规模的前端应用一般都是由很多相对独立的功能模块组合而成，且不同的功能模块由不同的团队负责，根据分而治之的思想，于是就有了将这些功能模块拆分成不同前端项目的想法，微前端技术也就此诞生。

[qiankun](https://qiankun.umijs.org/zh) 是阿里开源的一款微前端框架，它的灵感来自于 [single-spa](https://github.com/CanopyTax/single-spa) 项目，号称 **可能是你见过最完善的微前端解决方案**。single-spa 于 2018 年诞生，也是一个用于前端微服务化的解决方案，它实现了路由劫持和应用加载，不过它的缺点是不够灵活，不能动态加载 js 文件，而且没有处理样式隔离，不支持 js 沙箱机制。qiankun 于 2019 年开源，提供了更加开箱即用的 API (single-spa + sandbox + import-html-entry)，它基于 single-spa，具备 js 沙箱、样式隔离、HTML Loader、预加载 等微前端系统所需的能力。qiakun 升级 2.0 后，支持多个微应用的同时加载，有了这个特性，我们基本可以像接入 iframe 一样方便的接入微应用。

## 官方示例

`qiankun` 的源码里提供了大量完整的示例项目，我们先来体验体验这些示例，感受下微前端的魅力。首先，将 `qiankun` 的代码 clone 到本地：

```
$ git clone https://github.com/umijs/qiankun.git
```

`qiankun` 使用 [Yarn](https://yarnpkg.com/) 构建和打包项目，首先安装 Yarn：

```
$ npm install -g yarn
```

然后安装 `qiankun` 框架所依赖的包以及示例项目：

```
$ yarn install
$ yarn examples:install
```

示例项目中包含了各种不同框架的实现，比如 `Vue`、`Vue 3`、`React 15`、`React 16`、`Angular 9` 以及使用 jQuery 实现的纯 HTML 项目，Yarn 会依次安装各个示例项目的依赖包，整个过程会比较长，安装完成之后，使用下面的命令运行示例项目：

```
$ yarn examples:start
```

然后打开浏览器，访问 `http://localhost:7099/`：

![](./images/example.gif)

或者使用下面的命令运行 `multiple demo`：

```
$ yarn examples:start-multiple
```

![](./images/qiankun-multiple-demo.png)

## 开发实战

这一节我们将从零开始，使用 `qiankun` 搭建一个简单的微前端项目，这个项目包括一个主应用和两个子应用。

### 准备主应用

我们直接使用 `vue-cli` 创建一个 Vue 脚手架项目，首先确保已安装 Node.js 环境：

```
$ node -v
v16.14.2

$ npm -v
8.5.0
```

然后安装最新版本的 `vue-cli`：

```
$ npm install -g @vue/cli

$ vue -V
@vue/cli 5.0.8
```

使用 `vue-cli` 创建 demo 项目：

```
$ vue create demo

?  Your connection to the default npm registry seems to be slow.  
   Use https://registry.npmmirror.com for faster installation? Yes

Vue CLI v5.0.8
? Please pick a preset: Default ([Vue 3] babel, eslint)

Vue CLI v5.0.8
✨  Creating project in D:\code\weekly-practice\notes\week017-qiankun-micro-frontends\demo.
⚙️  Installing CLI plugins. This might take a while...

added 849 packages in 36s
🚀  Invoking generators...
📦  Installing additional dependencies...

added 95 packages in 11s
⚓  Running completion hooks...

📄  Generating README.md...

🎉  Successfully created project demo.      
👉  Get started with the following commands:

 $ cd demo
 $ npm run serve
```

使用 `npm run serve` 即可启动项目，启动成功后在浏览器中访问 `http://localhost:8080/`：

![](./images/vue-demo.png)

### 准备子应用

然后照葫芦画瓢，使用 `vue-cli` 创建 app1 和 app2 项目：

```
vue create app1


Vue CLI v5.0.8
? Please pick a preset: Default ([Vue 3] babel, eslint)
? Pick the package manager to use when installing dependencies: Yarn


Vue CLI v5.0.8
✨  Creating project in D:\code\weekly-practice\notes\week017-qiankun-micro-frontends\app1.
⚙️  Installing CLI plugins. This might take a while...

yarn install v1.22.19
info No lockfile found.
[1/4] Resolving packages...
[2/4] Fetching packages...
[3/4] Linking dependencies...

success Saved lockfile.
Done in 22.33s.
🚀  Invoking generators...
📦  Installing additional dependencies...

yarn install v1.22.19
[1/4] Resolving packages...
[2/4] Fetching packages...
[3/4] Linking dependencies...
[4/4] Building fresh packages...
success Saved lockfile.
Done in 7.88s.
⚓  Running completion hooks...

📄  Generating README.md...

🎉  Successfully created project app1.
👉  Get started with the following commands:

 $ cd app1
 $ yarn serve
```

使用 `vue-cli` 创建的项目默认端口是 8080，为了不和主应用冲突，需要修改 `vue.config.js` 配置文件，将子应用的端口修改为 8081 和 8082：

```
const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    port: 8081
  }
})
```

https://github.com/jiasx/mic-front-react

https://github.com/jiasx/mic-front-vue2.0

## 参考

1. [qiankun 官方文档](https://qiankun.umijs.org/zh)
1. [qiankun 技术圆桌 | 分享一些 qiankun 开发及微前端实践过程中的心得](https://www.yuque.com/kuitos/gky7yw)
1. [万字长文-落地微前端 qiankun 理论与实践指北](https://juejin.cn/post/7069566144750813197)
1. [Micro Frontends | extending the microservice idea to frontend development](https://micro-frontends.org/)
1. [single-spa](https://zh-hans.single-spa.js.org/docs/getting-started-overview)
1. [微前端框架 之 single-spa 从入门到精通](https://mp.weixin.qq.com/s?__biz=MzA3NTk4NjQ1OQ==&mid=2247484245&idx=1&sn=9ee91018578e6189f3b11a4d688228c5&chksm=9f696021a81ee937847c962e3135017fff9ba8fd0b61f782d7245df98582a1410aa000dc5fdc&scene=178&cur_album_id=2251416802327232513#rd)
1. [微前端框架 之 qiankun 从入门到源码分析](https://mp.weixin.qq.com/s?__biz=MzA3NTk4NjQ1OQ==&mid=2247484411&idx=1&sn=7e67d2843b8576fce01b18269f33f7e9&chksm=9f69608fa81ee99954b6b5a1e3eb40e194c05c1edb504baac27577a0217f61c78ff9d0bb7e23&scene=178&cur_album_id=2251416802327232513#rd)
