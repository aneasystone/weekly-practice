# 安装

## 在 Ubuntu 下安装

```
sudo apt remove docker docker-engine docker.io
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add –
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt update
sudo apt install docker-ce
sudo usermod -aG docker $USER  #将当前用户加入到Docker组
sudo echo "DOCKER_OPTS=\"--registry-mirror=https://registry.docker-cn.com\"" >> /etc/default/docker  #更改为国内源
sudo service docker restart
```