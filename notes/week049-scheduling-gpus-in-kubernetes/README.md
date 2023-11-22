# WEEK049 - 在 Kubernetes 中调度 GPU 资源

在人工智能越来越普及的今天，GPU 也变得越来越常见，无论是传统的机器学习和深度学习，还是现在火热的大语言模型和文生图模型，GPU 都是绕不开的话题。

## GPU 环境准备

```
# lspci | grep NVIDIA
00:07.0 3D controller: NVIDIA Corporation GP104GL [Tesla P4] (rev a1)
```

### 安装 NVIDIA 驱动

https://www.nvidia.com/Download/Find.aspx

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
