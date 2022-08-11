# WEEK018 - 使用 Github Actions 跟踪 Github 趋势项目

[GitHub Actions](https://docs.github.com/cn/actions) 是 GitHub 于 2018 年 10 月推出的一款 CI/CD 服务。一个标准的 CI/CD 流程通常是一个工作流（`workflow`），工作流中包含了一个或多个任务（`job`），而每个任务都是由多个执行步骤（`step`）组成。

GitHub Actions 的创新之处在于它将 CI/CD 中的每个执行步骤划分成一个个原子的操作（`action`），这些操作可以是编译代码、调用某个接口、执行代码检查或是部署服务等。很显然这些原子操作是可以在不同的 CI/CD 流程中复用的，于是 GitHub 允许开发者将这些操作编写成脚本存在放 GitHub 仓库里，供其他人使用。GitHub 提供了一些 [官方的 actions](https://github.com/actions)，比如 [actions/setup-python](https://github.com/actions/setup-python) 用于初始化 Python 环境，[actions/checkout](https://github.com/actions/checkout) 用于签出某个代码仓库。由于每个 action 都对应一个 GitHub 仓库，所以也可以像下面这样引用 action 的某个分支、某个标签甚至某个提交记录： 

```
actions/setup-node@master  # 指向一个分支
actions/setup-node@v1.0    # 指向一个标签
actions/setup-node@74bc508 # 指向一个 commit
```

你可以在 [GitHub Marketplace](https://github.com/marketplace?type=actions) 中搜索你想使用的 action，另外，还有一份关于 GitHub Actions 的 awesome 清单 [sdras/awesome-actions](https://github.com/sdras/awesome-actions)，也可以找到不少的 action。

## Github Actions 入门示例

https://github.com/actions/starter-workflows

## 跟踪 Github 趋势项目

[bonfy/github-trending](https://github.com/bonfy/github-trending)

## 本地运行 Github Actions

https://github.com/nektos/act

## 参考

* [GitHub Actions 文档](https://docs.github.com/cn/actions)
* [GitHub Actions 入门教程](https://www.ruanyifeng.com/blog/2019/09/getting-started-with-github-actions.html)
