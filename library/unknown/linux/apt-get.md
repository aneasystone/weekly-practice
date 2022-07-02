## 设置 apt-get 源

Ubuntu 自带的 apt-get 源为 http://archive.ubuntu.com/ubuntu ，下载速度非常慢，需要换成国内的 apt-get 源。

### 国内 apt-get 源

* 清华大学：https://mirrors.tuna.tsinghua.edu.cn/help/ubuntu/
* 阿里云：https://yq.aliyun.com/articles/704603?spm=a2c4e.11155472.0.0.45c05de2jw5DhW

### 设置清华大学 apt-get 源

根据 Ubuntu 的版本选择对应的源文件，譬如 16.04 为 xenial，18.04 为 bionic，不要选错，将源文件保存到 sources.list 文件。

```
$ vim sources.list
```

Ubuntu 16.04 的 apt-get 源文件如下：

```
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial main restricted universe multiverse
# deb-src http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial main restricted universe multiverse
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-updates main restricted universe multiverse
# deb-src http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-updates main restricted universe multiverse
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-backports main restricted universe multiverse
# deb-src http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-backports main restricted universe multiverse
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-security main restricted universe multiverse
# deb-src http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-security main restricted universe multiverse
```

### 使用 docker 测试

```
$ sudo docker run -d --name u1 ubuntu:16.04 tail -f /dev/null
$ sudo docker cp sources.list u1:/etc/apt/sources.list
$ sudo docker exec -it u1 bash
root@80bc94cbe166:/# apt-get update
Get:1 http://mirrors.tuna.tsinghua.edu.cn/ubuntu xenial InRelease [247 kB]
Get:2 http://mirrors.tuna.tsinghua.edu.cn/ubuntu xenial-updates InRelease [109 kB]
Get:3 http://mirrors.tuna.tsinghua.edu.cn/ubuntu xenial-backports InRelease [107 kB]
Get:4 http://mirrors.tuna.tsinghua.edu.cn/ubuntu xenial-security InRelease [109 kB]
Get:5 http://mirrors.tuna.tsinghua.edu.cn/ubuntu xenial/main amd64 Packages [1558 kB]
Get:6 http://mirrors.tuna.tsinghua.edu.cn/ubuntu xenial/restricted amd64 Packages [14.1 kB]
Get:7 http://mirrors.tuna.tsinghua.edu.cn/ubuntu xenial/universe amd64 Packages [9827 kB]
Get:8 http://mirrors.tuna.tsinghua.edu.cn/ubuntu xenial/multiverse amd64 Packages [176 kB]
Get:9 http://mirrors.tuna.tsinghua.edu.cn/ubuntu xenial-updates/main amd64 Packages [1250 kB]
Get:10 http://mirrors.tuna.tsinghua.edu.cn/ubuntu xenial-updates/restricted amd64 Packages [13.1 kB]
Get:11 http://mirrors.tuna.tsinghua.edu.cn/ubuntu xenial-updates/universe amd64 Packages [968 kB]
Get:12 http://mirrors.tuna.tsinghua.edu.cn/ubuntu xenial-updates/multiverse amd64 Packages [19.1 kB]
Get:13 http://mirrors.tuna.tsinghua.edu.cn/ubuntu xenial-backports/main amd64 Packages [7942 B]
Get:14 http://mirrors.tuna.tsinghua.edu.cn/ubuntu xenial-backports/universe amd64 Packages [8532 B]
Get:15 http://mirrors.tuna.tsinghua.edu.cn/ubuntu xenial-security/main amd64 Packages [857 kB]
Get:16 http://mirrors.tuna.tsinghua.edu.cn/ubuntu xenial-security/restricted amd64 Packages [12.7 kB]
Get:17 http://mirrors.tuna.tsinghua.edu.cn/ubuntu xenial-security/universe amd64 Packages [557 kB]
Get:18 http://mirrors.tuna.tsinghua.edu.cn/ubuntu xenial-security/multiverse amd64 Packages [6121 B]
Fetched 15.8 MB in 4s (3360 kB/s)   
Reading package lists... Done
```