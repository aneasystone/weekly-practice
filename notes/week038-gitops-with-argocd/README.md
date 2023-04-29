# WEEK038 - 基于 Argo CD 的 GitOps 实践笔记

[GitOps](https://www.weave.works/technologies/gitops/) 这个概念最早是由 [Weaveworks](https://www.weave.works) 的 CEO Alexis Richardson 在 2017 年提出的，它是一种全新的基于 Git 仓库来管理 Kubernetes 集群和交付应用程序的方式。它包含以下四个基本原则：

1. **声明式（Declarative）**：整个系统必须通过声明式的方式进行描述，比如 Kubernetes 就是声明式的，它通过 YAML 来描述系统的期望状态；
2. **版本控制和不可变（Versioned and immutable）**：所有的声明式描述都存储在 Git 仓库中，通过 Git 我们可以对系统的状态进行版本控制，记录了整个系统的修改历史，可以方便地回滚；
3. **自动拉取（Pulled automatically）**：我们通过提交代码的形式将系统的期望状态提交到 Git 仓库，系统从 Git 仓库自动拉取并做出变更，这种被称为 Pull 模式，整个过程不需要安装额外的工具，也不需要配置 Kubernetes 的认证授权；而传统的 CI/CD 工具如 Jenkins 或 CircleCI 等使用的是 Push 模式，这种模式一般都会在 CI 流水线运行完成后通过执行命令将应用部署到系统中，这不仅需要安装额外工具（比如 kubectl），还需要配置 Kubernetes 的授权，而且这种方式无法感知部署状态，所以也就无法保证集群状态的一致性了；
4. **持续调谐（Continuously reconciled）**：通过在目标系统中安装一个 Agent，一般使用 Kubernetes Operator 来实现，它会定期检测实际状态与期望状态是否一致，一旦检测到不一致，Agent 就会自动进行修复，确保系统达到期望状态，这个过程就是调谐（Reconciliation）；这样做的好处是将 Git 仓库作为单一事实来源，即使集群由于误操作被修改，Agent 也会通过持续调谐自动恢复。

其实，在提出 GitOps 概念之前，已经有另一个概念 IaC （Infrastructure as Code，基础设施即代码）被提出了，IaC 表示使用代码来定义基础设施，方便编辑和分发系统配置，它作为 DevOps 的最佳实践之一得到了社区的广泛关注。关于 IaC 和 GitOps 的区别，可以参考 [The GitOps FAQ](https://www.weave.works/technologies/gitops-frequently-asked-questions/)。

## Argo CD 简介

基于 GitOps 理念，很快诞生出了一批 **声明式的持续交付（Declarative Continuous Deployment）** 工具，比如 Weaveworks 的 [Flux CD](https://github.com/fluxcd/flux) 和 Intuit 的 [Argo CD](https://argoproj.github.io/cd/)，虽然 Weaveworks 是 GitOps 概念的提出者，但是从社区的反应来看，似乎 Argo CD 要更胜一筹。

这一节我们将学习 Argo CD，学习如何通过 Git 以及声明式描述来部署 Kubernetes 资源。

### 快速入门

https://argo-cd.readthedocs.io/en/stable/

## 参考

* [GitOps 介绍](https://icloudnative.io/posts/what-is-gitops/)
* [Argo CD 入门教程](https://icloudnative.io/posts/getting-started-with-argocd/)
* [GitOps 应用实践系列 - 综述](https://moelove.info/2021/10/19/GitOps-%E5%BA%94%E7%94%A8%E5%AE%9E%E8%B7%B5%E7%B3%BB%E5%88%97-%E7%BB%BC%E8%BF%B0/)
* [GitOps 应用实践系列 - Argo CD 的基本介绍](https://moelove.info/2021/10/21/GitOps-%E5%BA%94%E7%94%A8%E5%AE%9E%E8%B7%B5%E7%B3%BB%E5%88%97-Argo-CD-%E7%9A%84%E5%9F%BA%E6%9C%AC%E4%BB%8B%E7%BB%8D/)
* [GitOps 应用实践系列 - Flux CD 及其核心组件](https://moelove.info/2021/12/18/GitOps-%E5%BA%94%E7%94%A8%E5%AE%9E%E8%B7%B5%E7%B3%BB%E5%88%97-Flux-CD-%E5%8F%8A%E5%85%B6%E6%A0%B8%E5%BF%83%E7%BB%84%E4%BB%B6/)
* [Argo CD vs Flux CD — Right GitOps tool for your Kubernetes cluster](https://rajputvaibhav.medium.com/argo-cd-vs-flux-cd-right-gitops-tool-for-your-kubernetes-cluster-c71cff489d26)
* [Guide To GitOps](https://www.weave.works/technologies/gitops/)
* [The GitOps FAQ](https://www.weave.works/technologies/gitops-frequently-asked-questions/)
* [What Is GitOps](https://www.weave.works/blog/what-is-gitops-really)
* [The History of GitOps](https://www.weave.works/blog/the-history-of-gitops)
