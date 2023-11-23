# WEEK049 - 在 Kubernetes 中调度 GPU 资源

在人工智能越来越普及的今天，GPU 也变得越来越常见，无论是传统的机器学习和深度学习，还是现在火热的大语言模型和文生图模型，GPU 都是绕不开的话题。最近在工作中遇到一个需求，需要在 Kubernetes 中动态地调度和使用 GPU 资源，关于 GPU 这块一直是我的知识盲区，于是趁着业余时间恶补下相关的知识。

## GPU 环境准备

学习 GPU 有一定的门槛，不仅是因为好点的显卡都价格不菲，而且使用它还要搭配有相应的硬件环境，虽然笔记本也可以通过显卡扩展坞来使用，但是性能有一定的损失。对于有条件的同学，网上有很多关于如何搭建自己的深度学习工作站的教程可供参考，对此我也没有什么经验，此处略过；对于没有条件的同学，网上也有很多白嫖 GPU 的攻略，我在 [week037-ai-painting-with-google-colab](../week037-ai-painting-with-google-colab/README.md) 这篇博客中也介绍了如何在 Google Colab 中免费使用 GPU 的方法；不过这些环境一般都是做机器学习相关的实验，如果想在上面做一些更底层的实验，比如安装 Docker，部署 Kubernetes 集群等，就不太合适了。

正在无奈之际，我突然想到了阿里云的云服务器 ECS 有一个按量付费的功能，于是便上去瞅了瞅，发现有一种规格叫 **共享型 GPU 实例**，4 核 CPU，8G 内存，显卡为 NVIDIA A10，显存 2G，虽然配置不高，但是足够我们做实验的了，价格也相当便宜，一个小时只要一块八：

![](./images/aliyun-ecs.png)

于是便抱着试一试的态度下了一单，然后开始了下面的实验。

### 安装 NVIDIA 驱动

登录刚买的服务器，我们可以通过 `lspci` 看到 NVIDIA 的这张显卡：

```
# lspci | grep NVIDIA
00:07.0 VGA compatible controller: NVIDIA Corporation Device 2236 (rev a1)
```

此时这个显卡还不能直接使用，我们还需要安装 NVIDIA 的显卡驱动。访问 [NVIDIA Driver Downloads](https://www.nvidia.com/Download/Find.aspx)，在这里找到你的显卡型号并下载：

![](./images/nvidia-driver-download.png)

### 安装 CUDA 驱动

https://developer.nvidia.com/cuda-toolkit-archive

## 在 Docker 容器中使用 GPU 资源

https://www.cnblogs.com/linhaifeng/p/16108285.html

## 在 Kubernetes 中调度 GPU 资源

Kubernetes 具有对机器的资源进行分配和使用的能力，比如可以指定容器最多使用多少内存以及使用多少 CPU 计算资源。

### 安装 NVIDIA 设备插件

https://github.com/NVIDIA/k8s-device-plugin#quick-start

### 调度 GPU 资源

https://kuboard.cn/learning/k8s-practice/gpu/gpu.html

https://www.cnblogs.com/linhaifeng/p/16111733.html

https://icloudnative.io/posts/add-nvidia-gpu-support-to-k8s-with-containerd/

## 监控 GPU 资源的使用

https://blog.kubecost.com/blog/nvidia-gpu-usage/

## 参考

* [k8s 调度 GPU](https://www.cnblogs.com/linhaifeng/p/16111733.html)
* [docker使用GPU总结](https://www.cnblogs.com/linhaifeng/p/16108285.html)
* [NVIDIA device plugin for Kubernetes](https://github.com/NVIDIA/k8s-device-plugin#quick-start)
* [Schedule GPUs](https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/)
* [调度 GPU | Kuboard](https://kuboard.cn/learning/k8s-practice/gpu/gpu.html)
* [Monitoring NVIDIA GPU Usage in Kubernetes with Prometheus](https://blog.kubecost.com/blog/nvidia-gpu-usage/)
* [Kubernetes 教程：在 Containerd 容器中使用 GPU](https://icloudnative.io/posts/add-nvidia-gpu-support-to-k8s-with-containerd/)
