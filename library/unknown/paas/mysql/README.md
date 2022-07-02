## MySQL

### 最简单的运行方式

```
$ docker run -p 3306:3306 --name mysql -e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.6
```

### 自定义配置文件

```
$ docker run -p 3306:3306 --name mysql \
    -v $PWD/conf:/etc/mysql/conf.d \
	-e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.6
```

### 挂载数据和日志目录

```
$ docker run -p 3306:3306 --name mysql \
    -v $PWD/conf:/etc/mysql/conf.d \
	-v $PWD/logs:/logs \
	-v $PWD/data:/var/lib/mysql \
	-e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.6
```

### 初始化脚本

```
$ docker run -p 3306:3306 --name mysql \
    -v $PWD/conf:/etc/mysql/conf.d \
	-v $PWD/logs:/logs \
	-v $PWD/data:/var/lib/mysql \
	-v $PWD/init:/docker-entrypoint-initdb.d \
	-e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.6
```

https://www.runoob.com/docker/docker-install-mysql.html