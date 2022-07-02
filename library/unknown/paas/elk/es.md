## Elasticsearch

### 安装

添加 elasticsearch 的 yum 源：

```
cd /etc/yum.repos.d
vi elasticsearch7.repo

[elasticsearch-7.x]
name=Elasticsearch repository for 7.x packages
baseurl=https://mirror.tuna.tsinghua.edu.cn/elasticstack/7.x/yum/
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=1
autorefresh=1
type=rpm-md
```

安装并启动：

```
yum install elasticsearch

systemctl start elasticsearch
systemctl status elasticsearch
systemctl enable elasticsearch
```

查看系统内核参数，确认 `max_map_count` 设置是否正确：

```
sysctl vm.max_map_count
vm.max_map_count = 262144
```

检查ES正常运行：

```
curl -X GET "localhost:9200/?pretty"
{
  "name" : "centos7",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "7wWOyxwyRiuPIC80FjewmQ",
  "version" : {
    "number" : "7.3.0",
    "build_flavor" : "default",
    "build_type" : "rpm",
    "build_hash" : "de777fa",
    "build_date" : "2019-07-24T18:30:11.767338Z",
    "build_snapshot" : false,
    "lucene_version" : "8.1.0",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}
```

安装国际化分词插件analysis-icu:

```
cd /usr/share/elasticsearch/bin
elasticsearch-plugin install analysis-icu
elasticsearch/bin/elasticsearch-plugin list
analysis-icu
```

* https://blog.frognew.com/2019/08/elasticsearch-7.x-yum-install.html
