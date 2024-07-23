# dromara/liteflow - 轻量，快速，稳定可编排的组件式规则引擎

* GitHub：https://github.com/dromara/liteflow
* HomePage：https://liteflow.yomahub.com/

## 快速入门

首先在 pom.xml 文件中添加依赖：

```
<dependency>
    <groupId>com.yomahub</groupId>
    <artifactId>liteflow-spring-boot-starter</artifactId>
    <version>2.8.1</version>
</dependency>
```

然后定义组件 a：

```
@Component("a")
public class ACmp extends NodeComponent {

	@Override
	public void process() {
		System.out.println("Processing A component...");
	}
}
```

以此类推，再定义 b 和 c。

然后在配置文件中指定规则文件：

```
liteflow.rule-source=config/flow.el.xml
```

规则文件内容如下：

```
<?xml version="1.0" encoding="UTF-8"?>
<flow>
    <chain name="chain1">
        THEN(a, b, c);
    </chain>
</flow>
```

这时我们就可以执行这个规则了，只需要在代码中注入 `FlowExecutor` 即可：

```
@Component
public class DemoRunner implements CommandLineRunner {

	@Resource
    private FlowExecutor flowExecutor;
	
	@Override
	public void run(String... args) throws Exception {
		LiteflowResponse response = flowExecutor.execute2Resp("chain1", "param");
		System.out.println(String.format("RequestId = %s\r\nExecutorStepStr = %s\r\nMessage = %s\r\nisSuccess = %s", 
			response.getRequestId(),
			response.getExecuteStepStr(),
			response.getMessage(),
			response.isSuccess()));
	}
}
```

运行程序，执行结果如下：

```
> java -jar .\target\demo-0.0.1-SNAPSHOT.jar

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/
 :: Spring Boot ::                (v2.7.1)

2022-07-11 07:16:20.666  INFO 8268 --- [           main] com.example.demo.DemoApplication         : Starting DemoApplication v0.0.1-SNAPSHOT using Java 17.0.3 on 
DESKTOP-CH85E4K with PID 8268 (D:\code\weekly-practice\projects\pro001-dromara-liteflow\demo\target\demo-0.0.1-SNAPSHOT.jar started by aneasystone in D:\code\weekly-practice\projects\pro001-dromara-liteflow\demo)
2022-07-11 07:16:20.672  INFO 8268 --- [           main] com.example.demo.DemoApplication         : No active profile set, falling back to 1 default profile: "default"
2022-07-11 07:16:21.492  INFO 8268 --- [           main] trationDelegate$BeanPostProcessorChecker : Bean 'com.yomahub.liteflow.springboot.config.LiteflowMainAutoConfiguration' of type [com.yomahub.liteflow.springboot.config.LiteflowMainAutoConfiguration$$EnhancerBySpringCGLIB$$39c49e17] is not eligible for getting processed by all BeanPostProcessors (for example: not eligible for auto-proxying)
2022-07-11 07:16:21.505  INFO 8268 --- [           main] trationDelegate$BeanPostProcessorChecker : Bean 'com.yomahub.liteflow.springboot.config.LiteflowPropertyAutoConfiguration' of type [com.yomahub.liteflow.springboot.config.LiteflowPropertyAutoConfiguration$$EnhancerBySpringCGLIB$$99e57f7b] is not eligible for getting 
processed by all BeanPostProcessors (for example: not eligible for auto-proxying)
2022-07-11 07:16:21.566  INFO 8268 --- [           main] trationDelegate$BeanPostProcessorChecker : Bean 'liteflow-com.yomahub.liteflow.springboot.LiteflowProperty' of type [com.yomahub.liteflow.springboot.LiteflowProperty] is not eligible for getting processed by all BeanPostProcessors (for example: not eligible for auto-proxying)
2022-07-11 07:16:21.587  INFO 8268 --- [           main] trationDelegate$BeanPostProcessorChecker : Bean 'liteflow.monitor-com.yomahub.liteflow.springboot.LiteflowMonitorProperty' of type [com.yomahub.liteflow.springboot.LiteflowMonitorProperty] is not eligible for getting processed by all BeanPostProcessors (for example: 
not eligible for auto-proxying)
2022-07-11 07:16:21.626  INFO 8268 --- [           main] trationDelegate$BeanPostProcessorChecker : Bean 'liteflowConfig' of type [com.yomahub.liteflow.property.LiteflowConfig] is not eligible for getting processed by all BeanPostProcessors (for example: not eligible for auto-proxying)
2022-07-11 07:16:21.639  INFO 8268 --- [           main] com.yomahub.liteflow.util.LOGOPrinter    : 
================================================================================================
                 _     ___ _____ _____      _____ _     _____        __
                | |   |_ _|_   _| ____|    |  ___| |   / _ \ \      / /
                | |    | |  | | |  _| _____| |_  | |  | | | \ \ /\ / /
                | |___ | |  | | | |__|_____|  _| | |__| |_| |\ V  V /
                |_____|___| |_| |_____|    |_|   |_____\___/  \_/\_/

                Version: v2.8.1
                轻量且强大的规则引擎框架。
                Small but powerful rules engine.
================================================================================================

2022-07-11 07:16:21.668  INFO 8268 --- [           main] c.y.liteflow.spring.ComponentScanner     : component[a] has been found
2022-07-11 07:16:21.676  INFO 8268 --- [           main] c.y.liteflow.spring.ComponentScanner     : component[b] has been found
2022-07-11 07:16:21.679  INFO 8268 --- [           main] c.y.liteflow.spring.ComponentScanner     : component[c] has been found
2022-07-11 07:16:21.866  INFO 8268 --- [           main] com.yomahub.liteflow.core.FlowExecutor   : flow info loaded from local file,path=config/flow.el.xml,format type=el_xml
2022-07-11 07:16:22.214  INFO 8268 --- [           main] com.example.demo.DemoApplication         : Started DemoApplication in 2.274 seconds (JVM running for 3.238)
2022-07-11 07:16:22.225  INFO 8268 --- [           main] com.yomahub.liteflow.core.FlowExecutor   : slot[0] offered
2022-07-11 07:16:22.234  INFO 8268 --- [           main] com.yomahub.liteflow.core.FlowExecutor   : requestId[529fb3c749e14105859881455d47726f] has generated
2022-07-11 07:16:22.235  INFO 8268 --- [           main] com.yomahub.liteflow.flow.element.Node   : [529fb3c749e14105859881455d47726f]:[O]start component[a] execution
Processing A component...
2022-07-11 07:16:22.253  INFO 8268 --- [           main] com.yomahub.liteflow.flow.element.Node   : [529fb3c749e14105859881455d47726f]:[O]start component[b] execution
Processing B component...
2022-07-11 07:16:22.256  INFO 8268 --- [           main] com.yomahub.liteflow.flow.element.Node   : [529fb3c749e14105859881455d47726f]:[O]start component[c] execution
Processing C component...
2022-07-11 07:16:22.263  INFO 8268 --- [           main] com.yomahub.liteflow.slot.Slot           : [529fb3c749e14105859881455d47726f]:CHAIN_NAME[chain1]
a<11>==>b<0>==>c<0>
2022-07-11 07:16:22.263  INFO 8268 --- [           main] com.yomahub.liteflow.slot.DataBus        : [529fb3c749e14105859881455d47726f]:slot[0] released
RequestId = 529fb3c749e14105859881455d47726f
ExecutorStepStr = a==>b==>c
Message =
isSuccess = true
```

可以看出三个组件按顺序 `a==>b==>c` 被依次执行。

## 规则文件配置

`LiteFlow` 支持三种格式的配置文件：`xml`、`json` 和 `yaml`，并且原生支持两种配置源：本地配置和 ZooKeeper 配置，而且还提供了扩展点可以用户自定义配置源。

在上面的例子中我们使用的是本地 `xml` 配置，这一节我们来试试 ZooKeeper 配置。首先用 Docker 启动一个 ZooKeeper 进程：

```
> docker run -d -p 2181:2181 --name zookeeper zookeeper
```

然后进入容器连接 ZooKeeper：

```
> docker exec -it zookeeper bash
root@1f387d442e27:/apache-zookeeper-3.8.0-bin# ls
LICENSE.txt  NOTICE.txt  README.md  README_packaging.md  bin  conf  docs  lib
root@1f387d442e27:/apache-zookeeper-3.8.0-bin# cd bin/
root@1f387d442e27:/apache-zookeeper-3.8.0-bin/bin# ./zkCli.sh
```

在 ZooKeeper 上创建一个节点 `/liteflow`，并将 `json` 格式的配置保存到该节点：

```
[zk: localhost:2181(CONNECTED) 0] create /liteflow
[zk: localhost:2181(CONNECTED) 1] set /liteflow {"flow":{"chain":[{"name":"chain1","value":"THEN(a,b,c)"}]}}
[zk: localhost:2181(CONNECTED) 2] get /liteflow
{"flow":{"chain":[{"name":"chain1","value":"THEN(a,b,c)"}]}}
```

至此配置已经准备就绪，修改 `application.properties` 配置文件：

```
liteflow.rule-source=el_json:127.0.0.1:2181
liteflow.zk-node=/liteflow
```

并在 `pom.xml` 文件中加入依赖：

```
<dependency>
    <groupId>org.apache.curator</groupId>
    <artifactId>curator-framework</artifactId>
    <version>5.1.0</version>
</dependency>
<dependency>
    <groupId>org.apache.curator</groupId>
    <artifactId>curator-recipes</artifactId>
    <version>5.1.0</version>
</dependency>
```

重新运行程序，得到和上一节相同的结果。ZooKeeper 的最大优势是配置的自动热加载，应用程序会自动监听 ZooKeeper 节点内容的变化，可以在不重启服务的情况下，进行规则的重载，而且不会因为重载的过程而出现服务中断的现象。
