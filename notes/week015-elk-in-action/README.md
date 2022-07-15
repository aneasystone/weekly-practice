# WEEK014 - 实战 ELK 搭建日志系统

`ELK` 是 `Elasticsearch` + `Logstash` + `Kibana` 的简称。`Elasticsearch` 是一个基于 `Lucene` 的分布式全文搜索引擎，提供 RESTful API 进行数据读写；`Logstash` 是一个收集，处理和转发事件和日志消息的工具；而 `Kibana` 是 Elasticsearch 的开源数据可视化插件，为查看存储在 Elasticsearch 提供了友好的 Web 界面，并提供了条形图，线条和散点图，饼图和地图等分析工具。

总的来说，Elasticsearch 负责存储数据，Logstash 负责收集日志，并将日志格式化后写入 Elasticsearch，Kibana 提供可视化访问 Elasticsearch 数据的功能。

## 安装 Elasticsearch

https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html

## 安装 Logstash

## 安装 Kibana

## 参考

1. [Elasticsearch Guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
1. [Logstash Guide](https://www.elastic.co/guide/en/logstash/current/index.html)
1. [Filebeat Guide](https://www.elastic.co/guide/en/beats/filebeat/current/index.html)
1. [Kibana Guide](https://www.elastic.co/guide/en/kibana/current/index.html)
1. [ELK6.0部署：Elasticsearch+Logstash+Kibana搭建分布式日志平台](https://ken.io/note/elk-deploy-guide)
1. https://github.com/xuwujing/java-study

## 更多

	Elasticsearch
	https://fuxiaopang.gitbooks.io/learnelasticsearch/

    Logstash
    https://doc.yonyoucloud.com/doc/logstash-best-practice-cn/index.html

    Filebeat
    https://www.ibm.com/developerworks/cn/opensource/os-cn-elk-filebeat/index.html
    https://blog.csdn.net/mawming/article/details/78344939