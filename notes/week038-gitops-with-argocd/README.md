# WEEK038 - 基于 Argo CD 的 GitOps 实践笔记

[GitOps](https://www.weave.works/technologies/gitops/) 这个概念最早是由 [Weaveworks](https://www.weave.works) 在 2017 年提出的，它是一种全新的基于 Kubernetes 集群管理和应用程序交付的方式。

## Argo CD 简介

基于 GitOps 理念，很快诞生出一批 **声明式的持续交付**（ Declarative Continuous Deployment ）工具，[Argo CD](https://argoproj.github.io/cd/) 就是其中之一，它是 Argo 生态的一部分，可以通过声明式的方式部署 Kubernetes 资源。

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
