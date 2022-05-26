# 在 Docker 环境中开发 Spring Boot 项目

这篇教程介绍了如何构建一个 Docker 镜像来运行 Spring Boot 应用，我们首先创建一个基础的 Dockerfile 文件，然后试着做一些调整，最后还会介绍使用 Maven 插件来代替 `docker` 命令构建镜像。

开始教程之前，确保你的机器上已经安装了 Docker。

## 使用 Spring Initializr 创建一个项目

访问 [start.spring.io](https://start.spring.io/)，创建一个 Spring Boot 项目，或者直接访问这个链接（[pre-initialized project](https://start.spring.io/#!type=maven-project&language=java&platformVersion=2.7.0&packaging=jar&jvmVersion=11&groupId=com.example&artifactId=demo&name=demo&description=Demo%20project%20for%20Spring%20Boot&packageName=com.example.demo&dependencies=web)），点击 Generate 按钮下载项目初始代码。

## 设置 Spring Boot 应用

刚创建的项目入口类如下所示：

```
package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class DemoApplication {

  public static void main(String[] args) {
    SpringApplication.run(DemoApplication.class, args);
  }

}
```

此时我们可以直接 `mvn package` 将代码打成 jar 包并运行，不过这个应用现在还看不到什么用处。所以我们决定为其加一个 Web 首页：

```
package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class DemoApplication {

  @RequestMapping("/")
  public String home() {
    return "Hello Docker World";
  }

  public static void main(String[] args) {
    SpringApplication.run(DemoApplication.class, args);
  }

}
```

我们在 `Application` 类中添加一个 `home()` 方法，通过 `@RestController` 和 `@RequestMapping("/")` 将这个方法设置成 Web 首页。

打包并运行：

```
$ mvn clean package && java -jar .\target\demo-0.0.1-SNAPSHOT.jar
```

访问首页：

```
$ curl http://localhost:8080
Hello Docker World
```

## 构建第一个镜像

在项目根目录创建一个 Dockerfile 文件：

```
FROM openjdk:17-jdk-alpine
ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} app.jar
ENTRYPOINT ["java","-jar","/app.jar"]
```

然后运行如下的 `docker build` 命令：

```
# docker build -t springio/gs-spring-boot-docker .
```

这是一个非常简单的 Dockerfile，其中使用了 4 个指令：

* `FROM`：指定 `openjdk:17-jdk-alpine` 为基础镜像，基础镜像中包含了程序运行所需的环境；需要注意的是，本地编译打包所使用的 Java 版本最好和基础镜像中的版本一致，譬如我本地使用的是 JDK 17，基础镜像使用 JDK 8，运行时就会报错：

```
Exception in thread "main" java.lang.UnsupportedClassVersionError: com/example/demo/DemoApplication has been compiled by a more recent version of the Java Runtime (class file version 55.0), this version of the Java Runtime only recognizes class file versions up to 52.0
```

* `ARG`：定义一个 JAR_FILE 参数，可以在构建镜像时通过 `--build-arg` 设置参数值，譬如你如果是 Gradle 项目，打包后的 jar 文件在 build/libs 目录，而不是 target 目录，你就可以这样构建镜像：`docker build --build-arg JAR_FILE=build/libs/\*.jar -t springio/gs-spring-boot-docker .`；
* `COPY`：将 jar 文件拷贝到镜像中；
* `ENTRYPOINT`：指定容器启动后需要执行的命令。

通过上面的命令，我们构建了一个名为 `springio/gs-spring-boot-docker` 的镜像，可以通过下面的 `docker run` 命令运行它：

```
# docker run -p 8080:8080 springio/gs-spring-boot-docker
```

## 指定用户

从运行日志中，可以看到默认情况下，Docker 容器中的程序是以 root 用户运行的（started by root）：

```
2022-05-25 00:00:41.598  INFO 1 --- [           main] com.example.demo.DemoApplication         : Starting DemoApplication v0.0.1-SNAPSHOT using Java 17-ea on 0d5422937dda with PID 1 (/app.jar started by root in /)
```

使用 root 运行程序存在一定的安全风险，最好的做法是创建一个普通用户来运行容器中的程序，我们创建一个新的 Dockerfile_rootless 文件：

```
FROM openjdk:17-jdk-alpine
RUN addgroup -S spring && adduser -S spring -G spring
USER spring:spring
ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} app.jar
ENTRYPOINT ["java","-jar","/app.jar"]
```

我们新增了两个指令：

* `RUN`：在构建 Docker 镜像时执行的命令，执行结果是内置在镜像中的。在这里我们使用了 `addgroup` 添加了一个用户组 spring，并使用 `adduser` 将用户 spring 添加到该用户组；
* `USER`：指定了容器中的程序以 spring 用户来运行。

重新构建镜像并运行：

```
> docker build -t springio/gs-spring-boot-docker -f Dockerfile_rootless .
> docker run -p 8080:8080 springio/gs-spring-boot-docker
...
2022-05-25 00:11:51.096  INFO 1 --- [           main] com.example.demo.DemoApplication         : Starting DemoApplication v0.0.1-SNAPSHOT using Java 17-ea on 0e49a18ea22f with PID 1 (/app.jar started by spring in /)
...
```

从启动日志可以看出，程序是以 spring 用户运行的。

## 镜像分层

我们知道 Docker 的镜像是分层存储的，在 Dockerfile 中的每一行指令都会生成一个新的分层，在构建和运行时，相同的分层会通过缓存提高性能。在上面的 Dockerfile 中，我们通过 `COPY ${JAR_FILE} app.jar` 将打包后的 jar 文件拷贝到镜像中，这样会生成一个新的分层，而这个分层的大小取决于你这个 jar 文件的大小，一般来说 Spring Boot 项目打包后的文件是一个 fat jar，包含了程序的所有依赖，通常会比较大。

然而我们仔细想想，这个 jar 文件中包含的依赖或资源文件，在开发过程中，其实变动是很少的，经常变动的是我们的程序代码，如果我们能把程序依赖和程序代码分开来添加到镜像里，就可以充分使用 Docker 镜像的缓存机制，加快镜像构建的速度，也减少了多个镜像存储的空间。

我们使用 `jar -xf` 命令将 jar 文件解压：

```
# mkdir -p target/dependency && cd target/dependency
# jar -xf ../*.jar
```

查看解压后的目录，我们发现，实际上一个 jar 包里的内容大体可以分成三个部分：

* /BOOT-INF/lib
* /META-INF
* /BOOT-INF/classes

其中 `/BOOT-INF/lib` 和 `/META-INF` 都是变动不多的部分，变动最多的是 `/BOOT-INF/classes` 目录下的程序代码。我们稍微修改下 Dockerfile 文件，将 jar 文件中的内容分层添加：

```
FROM openjdk:17-jdk-alpine
RUN addgroup -S spring && adduser -S spring -G spring
USER spring:spring
ARG DEPENDENCY=target/dependency
COPY ${DEPENDENCY}/BOOT-INF/lib /app/lib
COPY ${DEPENDENCY}/META-INF /app/META-INF
COPY ${DEPENDENCY}/BOOT-INF/classes /app
ENTRYPOINT ["java", "-cp", "app:app/lib/*", "com.example.demo.DemoApplication"]
```

在这个 Dockerfile 里，引入了一个 `DEPENDENCY` 变量，表示 fat jar 解压后的位置，然后通过 `COPY` 指令将解压后的文件依次拷贝到镜像中，最后的启动命令也需要做一些修改：

```
$ java -cp app:app/lib/* com.example.demo.DemoApplication
```

> 直接使用主类来启动程序比 fat jar 启动速度更快。

重新构建镜像并运行：

```
> docker build -t springio/gs-spring-boot-docker -f Dockerfile_layer .
> docker run -p 8080:8080 springio/gs-spring-boot-docker
```

## 使用其他方式构建镜像

除了使用 `docker build` 来构建镜像外，我们还可以使用 Maven 或 Gradle 的插件来构建镜像，这样的插件有很多，比如 Spring Boot 官方提供的 [spring-boot-maven-plugin](https://docs.spring.io/spring-boot/docs/current/maven-plugin/reference/htmlsingle/#build-image)，还有 Google 提供的 [Jib](https://github.com/GoogleContainerTools/jib) 等等。使用这种方式构建镜像不需要 Dockerfile，甚至你的电脑上都不需要安装有 Docker 环境。

使用下面的命令通过 Spring Boot 插件来构建镜像：

```
$ mvn spring-boot:build-image -Dspring-boot.build-image.imageName=springio/gs-spring-boot-docker
[INFO] Scanning for projects...
[INFO]
[INFO] --------------------------< com.example:demo >--------------------------
[INFO] Building demo 0.0.1-SNAPSHOT
[INFO] --------------------------------[ jar ]---------------------------------
[INFO]
[INFO] >>> spring-boot-maven-plugin:2.7.0:build-image (default-cli) > package @ demo >>>
[INFO]
[INFO] --- maven-resources-plugin:3.2.0:resources (default-resources) @ demo ---
[INFO] Using 'UTF-8' encoding to copy filtered resources.
[INFO] Using 'UTF-8' encoding to copy filtered properties files.
[INFO] Copying 1 resource
[INFO] Copying 0 resource
[INFO] 
[INFO] --- maven-compiler-plugin:3.10.1:compile (default-compile) @ demo ---
[INFO] Nothing to compile - all classes are up to date
[INFO]
[INFO] --- maven-resources-plugin:3.2.0:testResources (default-testResources) @ demo ---
[INFO] Using 'UTF-8' encoding to copy filtered resources.
[INFO] Using 'UTF-8' encoding to copy filtered properties files.
[INFO] skip non existing resourceDirectory D:\code\weekly-practice\notes\week009-spring-guides\guides\gs\spring-boot-docker\demo\src\test\resources
[INFO]
[INFO] --- maven-compiler-plugin:3.10.1:testCompile (default-testCompile) @ demo ---
[INFO] Nothing to compile - all classes are up to date
[INFO]
[INFO] --- maven-surefire-plugin:2.22.2:test (default-test) @ demo ---
[INFO] 
[INFO] -------------------------------------------------------
[INFO]  T E S T S
[INFO] -------------------------------------------------------
[INFO] Running com.example.demo.DemoApplicationTests
07:35:40.466 [main] DEBUG org.springframework.test.context.BootstrapUtils - Instantiating CacheAwareContextLoaderDelegate from class [org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate]
07:35:40.488 [main] DEBUG org.springframework.test.context.BootstrapUtils - Instantiating BootstrapContext using constructor [public org.springframework.test.context.support.DefaultBootstrapContext(java.lang.Class,org.springframework.test.context.CacheAwareContextLoaderDelegate)]
07:35:40.578 [main] DEBUG org.springframework.test.context.BootstrapUtils - Instantiating TestContextBootstrapper for test class [com.example.demo.DemoApplicationTests] from class [org.springframework.boot.test.context.SpringBootTestContextBootstrapper]
07:35:40.592 [main] INFO org.springframework.boot.test.context.SpringBootTestContextBootstrapper - Neither @ContextConfiguration nor @ContextHierarchy found for test class [com.example.demo.DemoApplicationTests], using SpringBootContextLoader
07:35:40.599 [main] DEBUG org.springframework.test.context.support.AbstractContextLoader - Did not detect default resource location for test class [com.example.demo.DemoApplicationTests]: class path resource [com/example/demo/DemoApplicationTests-context.xml] does not exist
07:35:40.600 [main] DEBUG org.springframework.test.context.support.AbstractContextLoader - Did not detect default resource location for test class [com.example.demo.DemoApplicationTests]: class path resource [com/example/demo/DemoApplicationTestsContext.groovy] does not exist
07:35:40.601 [main] INFO org.springframework.test.context.support.AbstractContextLoader - Could not detect default resource locations for test class [com.example.demo.DemoApplicationTests]: no resource found for suffixes {-context.xml, Context.groovy}.
07:35:40.602 [main] INFO org.springframework.test.context.support.AnnotationConfigContextLoaderUtils - Could not detect default configuration classes for test class [com.example.demo.DemoApplicationTests]: DemoApplicationTests does not declare any static, non-private, non-final, nested classes annotated with @Configuration.
07:35:40.697 [main] DEBUG org.springframework.test.context.support.ActiveProfilesUtils - Could not find an 'annotation declaring class' for annotation type [org.springframework.test.context.ActiveProfiles] and class [com.example.demo.DemoApplicationTests]
07:35:40.792 [main] DEBUG org.springframework.context.annotation.ClassPathScanningCandidateComponentProvider - Identified candidate component class: file [D:\code\weekly-practice\notes\week009-spring-guides\guides\gs\spring-boot-docker\demo\target\classes\com\example\demo\DemoApplication.class]
07:35:40.793 [main] INFO org.springframework.boot.test.context.SpringBootTestContextBootstrapper - Found @SpringBootConfiguration com.example.demo.DemoApplication for test class com.example.demo.DemoApplicationTests
07:35:40.957 [main] DEBUG org.springframework.boot.test.context.SpringBootTestContextBootstrapper - @TestExecutionListeners is not present for class [com.example.demo.DemoApplicationTests]: using defaults.
07:35:40.957 [main] INFO org.springframework.boot.test.context.SpringBootTestContextBootstrapper - Loaded default TestExecutionListener class names from location 
[META-INF/spring.factories]: [org.springframework.boot.test.mock.mockito.MockitoTestExecutionListener, org.springframework.boot.test.mock.mockito.ResetMocksTestExecutionListener, org.springframework.boot.test.autoconfigure.restdocs.RestDocsTestExecutionListener, org.springframework.boot.test.autoconfigure.web.client.MockRestServiceServerResetTestExecutionListener, org.springframework.boot.test.autoconfigure.web.servlet.MockMvcPrintOnlyOnFailureTestExecutionListener, org.springframework.boot.test.autoconfigure.web.servlet.WebDriverTestExecutionListener, org.springframework.boot.test.autoconfigure.webservices.client.MockWebServiceServerTestExecutionListener, org.springframework.test.context.web.ServletTestExecutionListener, org.springframework.test.context.support.DirtiesContextBeforeModesTestExecutionListener, org.springframework.test.context.event.ApplicationEventsTestExecutionListener, org.springframework.test.context.support.DependencyInjectionTestExecutionListener, org.springframework.test.context.support.DirtiesContextTestExecutionListener, org.springframework.test.context.transaction.TransactionalTestExecutionListener, org.springframework.test.context.jdbc.SqlScriptsTestExecutionListener, org.springframework.test.context.event.EventPublishingTestExecutionListener]       
07:35:40.990 [main] DEBUG org.springframework.boot.test.context.SpringBootTestContextBootstrapper - Skipping candidate TestExecutionListener [org.springframework.test.context.transaction.TransactionalTestExecutionListener] due to a missing dependency. Specify custom listener classes or make the default listener classes and their required dependencies available. Offending class: [org/springframework/transaction/interceptor/TransactionAttributeSource]
07:35:40.992 [main] DEBUG org.springframework.boot.test.context.SpringBootTestContextBootstrapper - Skipping candidate TestExecutionListener [org.springframework.test.context.jdbc.SqlScriptsTestExecutionListener] due to a missing dependency. Specify custom listener classes or make the default listener classes and their required dependencies available. Offending class: [org/springframework/transaction/interceptor/TransactionAttribute]
07:35:40.994 [main] INFO org.springframework.boot.test.context.SpringBootTestContextBootstrapper - Using TestExecutionListeners: [org.springframework.test.context.web.ServletTestExecutionListener@4233e892, org.springframework.test.context.support.DirtiesContextBeforeModesTestExecutionListener@77d2e85, org.springframework.test.context.event.ApplicationEventsTestExecutionListener@3ecd267f, org.springframework.boot.test.mock.mockito.MockitoTestExecutionListener@58ffcbd7, org.springframework.boot.test.autoconfigure.SpringBootDependencyInjectionTestExecutionListener@555cf22, org.springframework.test.context.support.DirtiesContextTestExecutionListener@6bb2d00b, org.springframework.test.context.event.EventPublishingTestExecutionListener@3c9bfddc, org.springframework.boot.test.mock.mockito.ResetMocksTestExecutionListener@1a9c38eb, org.springframework.boot.test.autoconfigure.restdocs.RestDocsTestExecutionListener@319bc845, org.springframework.boot.test.autoconfigure.web.client.MockRestServiceServerResetTestExecutionListener@4c5474f5, org.springframework.boot.test.autoconfigure.web.servlet.MockMvcPrintOnlyOnFailureTestExecutionListener@2f4205be, org.springframework.boot.test.autoconfigure.web.servlet.WebDriverTestExecutionListener@54e22bdd, org.springframework.boot.test.autoconfigure.webservices.client.MockWebServiceServerTestExecutionListener@3bd418e4]
07:35:41.013 [main] DEBUG org.springframework.test.context.support.AbstractDirtiesContextTestExecutionListener - Before test class: context [DefaultTestContext@aafcffa testClass = DemoApplicationTests, testInstance = [null], testMethod = [null], testException = [null], mergedContextConfiguration = [WebMergedContextConfiguration@6955cb39 testClass = DemoApplicationTests, locations = '{}', classes = '{class com.example.demo.DemoApplication}', contextInitializerClasses = '[]', activeProfiles = '{}', propertySourceLocations = '{}', propertySourceProperties = '{org.springframework.boot.test.context.SpringBootTestContextBootstrapper=true}', contextCustomizers = set[org.springframework.boot.test.context.filter.ExcludeFilterContextCustomizer@3e62d773, org.springframework.boot.test.json.DuplicateJsonObjectContextCustomizerFactory$DuplicateJsonObjectContextCustomizer@3f1d2e23, org.springframework.boot.test.mock.mockito.MockitoContextCustomizer@0, org.springframework.boot.test.web.client.TestRestTemplateContextCustomizer@51bf5add, org.springframework.boot.test.autoconfigure.actuate.metrics.MetricsExportContextCustomizerFactory$DisableMetricExportContextCustomizer@2462cb01, org.springframework.boot.test.autoconfigure.properties.PropertyMappingContextCustomizer@0, org.springframework.boot.test.autoconfigure.web.servlet.WebDriverContextCustomizerFactory$Customizer@24c22fe, org.springframework.boot.test.context.SpringBootTestArgs@1, org.springframework.boot.test.context.SpringBootTestWebEnvironment@3d680b5a], resourceBasePath = 'src/main/webapp', contextLoader = 'org.springframework.boot.test.context.SpringBootContextLoader', parent = [null]], attributes = map['org.springframework.test.context.web.ServletTestExecutionListener.activateListener' -> true]], class annotated with @DirtiesContext [false] with mode [null].

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/
 :: Spring Boot ::                (v2.7.0)

2022-05-26 07:35:41.562  INFO 11392 --- [           main] com.example.demo.DemoApplicationTests    : Starting DemoApplicationTests using Java 11.0.8 on DESKTOP-CH85E4K with PID 11392 (started by aneasystone in D:\code\weekly-practice\notes\week009-spring-guides\guides\gs\spring-boot-docker\demo)
2022-05-26 07:35:41.566  INFO 11392 --- [           main] com.example.demo.DemoApplicationTests    : No active profile set, falling back to 1 default profile: "default"
2022-05-26 07:35:43.246  INFO 11392 --- [           main] com.example.demo.DemoApplicationTests    : Started DemoApplicationTests in 2.108 seconds (JVM running for 3.646)
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 3.336 s - in com.example.demo.DemoApplicationTests
[INFO] 
[INFO] Results:
[INFO]
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0
[INFO]
[INFO] 
[INFO] --- maven-jar-plugin:3.2.2:jar (default-jar) @ demo ---
[INFO] 
[INFO] --- spring-boot-maven-plugin:2.7.0:repackage (repackage) @ demo ---
[INFO] Replacing main artifact with repackaged archive
[INFO]
[INFO] <<< spring-boot-maven-plugin:2.7.0:build-image (default-cli) < package @ demo <<<
[INFO]
[INFO] 
[INFO] --- spring-boot-maven-plugin:2.7.0:build-image (default-cli) @ demo ---
[INFO] Building image 'docker.io/springio/gs-spring-boot-docker:latest'
[INFO]
[INFO]  > Pulling builder image 'docker.io/paketobuildpacks/builder:base' 100%
[INFO]  > Pulled builder image 'paketobuildpacks/builder@sha256:3c697980116634af29edc1835d07c7a7997ed94cf871a75c8e24734678e371a7'
[INFO]  > Pulling run image 'docker.io/paketobuildpacks/run:base-cnb' 100%
[INFO]  > Pulled run image 'paketobuildpacks/run@sha256:7a1375e604b79c068ad50b299b37a6b3e1289f8592feb5a466ce3c7935a4c4c9'
[INFO]  > Executing lifecycle version v0.14.0
[INFO]  > Using build cache volume 'pack-cache-8e3084d32c6c.build'
[INFO]
[INFO]  > Running creator
[INFO]     [creator]     ===> ANALYZING
[INFO]     [creator]     Previous image with name "docker.io/springio/gs-spring-boot-docker:latest" not found
[INFO]     [creator]     ===> DETECTING
[INFO]     [creator]     6 of 24 buildpacks participating
[INFO]     [creator]     paketo-buildpacks/ca-certificates   3.2.2
[INFO]     [creator]     paketo-buildpacks/bellsoft-liberica 9.3.4
[INFO]     [creator]     paketo-buildpacks/syft              1.11.1
[INFO]     [creator]     paketo-buildpacks/executable-jar    6.2.3
[INFO]     [creator]     paketo-buildpacks/dist-zip          5.2.3
[INFO]     [creator]     paketo-buildpacks/spring-boot       5.10.0
[INFO]     [creator]     ===> RESTORING
[INFO]     [creator]     ===> BUILDING
[INFO]     [creator]
[INFO]     [creator]     Paketo CA Certificates Buildpack 3.2.2
[INFO]     [creator]       https://github.com/paketo-buildpacks/ca-certificates
[INFO]     [creator]       Launch Helper: Contributing to layer
[INFO]     [creator]         Creating /layers/paketo-buildpacks_ca-certificates/helper/exec.d/ca-certificates-helper
[INFO]     [creator]     
[INFO]     [creator]     Paketo BellSoft Liberica Buildpack 9.3.4
[INFO]     [creator]       https://github.com/paketo-buildpacks/bellsoft-liberica
[INFO]     [creator]       Build Configuration:
[INFO]     [creator]         $BP_JVM_TYPE                 JRE             the JVM type - JDK or JRE
[INFO]     [creator]         $BP_JVM_VERSION              11.*            the Java version
[INFO]     [creator]       Launch Configuration:
[INFO]     [creator]         $BPL_DEBUG_ENABLED           false           enables Java remote debugging support
[INFO]     [creator]         $BPL_DEBUG_PORT              8000            configure the remote debugging port
[INFO]     [creator]         $BPL_DEBUG_SUSPEND           false           configure whether to suspend execution until a debugger has attached
[INFO]     [creator]         $BPL_HEAP_DUMP_PATH                          write heap dumps on error to this path
[INFO]     [creator]         $BPL_JAVA_NMT_ENABLED        true            enables Java Native Memory Tracking (NMT)
[INFO]     [creator]         $BPL_JAVA_NMT_LEVEL          summary         configure level of NMT, summary or detail
[INFO]     [creator]         $BPL_JFR_ARGS                                configure custom Java Flight Recording (JFR) arguments
[INFO]     [creator]         $BPL_JFR_ENABLED             false           enables Java Flight Recording (JFR)
[INFO]     [creator]         $BPL_JMX_ENABLED             false           enables Java Management Extensions (JMX)
[INFO]     [creator]         $BPL_JMX_PORT                5000            configure the JMX port
[INFO]     [creator]         $BPL_JVM_HEAD_ROOM           0               the headroom in memory calculation
[INFO]     [creator]         $BPL_JVM_LOADED_CLASS_COUNT  35% of classes  the number of loaded classes in memory calculation
[INFO]     [creator]         $BPL_JVM_THREAD_COUNT        250             the number of threads in memory calculation
[INFO]     [creator]         $JAVA_TOOL_OPTIONS                           the JVM launch flags
[INFO]     [creator]       BellSoft Liberica JRE 11.0.15: Contributing to layer
[INFO]     [creator]         Downloading from https://github.com/bell-sw/Liberica/releases/download/11.0.15+10/bellsoft-jre11.0.15+10-linux-amd64.tar.gz
[INFO]     [creator]         Verifying checksum
[INFO]     [creator]         Expanding to /layers/paketo-buildpacks_bellsoft-liberica/jre
[INFO]     [creator]         Adding 128 container CA certificates to JVM truststore
[INFO]     [creator]         Writing env.launch/BPI_APPLICATION_PATH.default
[INFO]     [creator]         Writing env.launch/BPI_JVM_CACERTS.default
[INFO]     [creator]         Writing env.launch/BPI_JVM_CLASS_COUNT.default
[INFO]     [creator]         Writing env.launch/BPI_JVM_SECURITY_PROVIDERS.default
[INFO]     [creator]         Writing env.launch/JAVA_HOME.default
[INFO]     [creator]         Writing env.launch/JAVA_TOOL_OPTIONS.append
[INFO]     [creator]         Writing env.launch/JAVA_TOOL_OPTIONS.delim
[INFO]     [creator]         Writing env.launch/MALLOC_ARENA_MAX.default
[INFO]     [creator]       Launch Helper: Contributing to layer
[INFO]     [creator]         Creating /layers/paketo-buildpacks_bellsoft-liberica/helper/exec.d/active-processor-count
[INFO]     [creator]         Creating /layers/paketo-buildpacks_bellsoft-liberica/helper/exec.d/java-opts
[INFO]     [creator]         Creating /layers/paketo-buildpacks_bellsoft-liberica/helper/exec.d/jvm-heap
[INFO]     [creator]         Creating /layers/paketo-buildpacks_bellsoft-liberica/helper/exec.d/link-local-dns
[INFO]     [creator]         Creating /layers/paketo-buildpacks_bellsoft-liberica/helper/exec.d/memory-calculator
[INFO]     [creator]         Creating /layers/paketo-buildpacks_bellsoft-liberica/helper/exec.d/security-providers-configurer
[INFO]     [creator]         Creating /layers/paketo-buildpacks_bellsoft-liberica/helper/exec.d/jmx
[INFO]     [creator]         Creating /layers/paketo-buildpacks_bellsoft-liberica/helper/exec.d/jfr
[INFO]     [creator]         Creating /layers/paketo-buildpacks_bellsoft-liberica/helper/exec.d/nmt
[INFO]     [creator]         Creating /layers/paketo-buildpacks_bellsoft-liberica/helper/exec.d/security-providers-classpath-9
[INFO]     [creator]         Creating /layers/paketo-buildpacks_bellsoft-liberica/helper/exec.d/debug-9
[INFO]     [creator]         Creating /layers/paketo-buildpacks_bellsoft-liberica/helper/exec.d/openssl-certificate-loader
[INFO]     [creator]       Java Security Properties: Contributing to layer
[INFO]     [creator]         Writing env.launch/JAVA_SECURITY_PROPERTIES.default
[INFO]     [creator]         Writing env.launch/JAVA_TOOL_OPTIONS.append
[INFO]     [creator]         Writing env.launch/JAVA_TOOL_OPTIONS.delim
[INFO]     [creator]     
[INFO]     [creator]     Paketo Syft Buildpack 1.11.1
[INFO]     [creator]       https://github.com/paketo-buildpacks/syft
[INFO]     [creator]         Downloading from https://github.com/anchore/syft/releases/download/v0.46.1/syft_0.46.1_linux_amd64.tar.gz
[INFO]     [creator]         Verifying checksum
[INFO]     [creator]         Writing env.build/SYFT_CHECK_FOR_APP_UPDATE.default
[INFO]     [creator]
[INFO]     [creator]     Paketo Executable JAR Buildpack 6.2.3
[INFO]     [creator]       https://github.com/paketo-buildpacks/executable-jar
[INFO]     [creator]       Class Path: Contributing to layer
[INFO]     [creator]         Writing env/CLASSPATH.delim
[INFO]     [creator]         Writing env/CLASSPATH.prepend
[INFO]     [creator]       Process types:
[INFO]     [creator]         executable-jar: java org.springframework.boot.loader.JarLauncher (direct)
[INFO]     [creator]         task:           java org.springframework.boot.loader.JarLauncher (direct)
[INFO]     [creator]         web:            java org.springframework.boot.loader.JarLauncher (direct)
[INFO]     [creator]     
[INFO]     [creator]     Paketo Spring Boot Buildpack 5.10.0
[INFO]     [creator]       https://github.com/paketo-buildpacks/spring-boot
[INFO]     [creator]       Build Configuration:
[INFO]     [creator]         $BP_SPRING_CLOUD_BINDINGS_DISABLED   false  whether to contribute Spring Boot cloud bindings support
[INFO]     [creator]       Launch Configuration:
[INFO]     [creator]         $BPL_SPRING_CLOUD_BINDINGS_DISABLED  false  whether to auto-configure Spring Boot environment properties from bindings
[INFO]     [creator]         $BPL_SPRING_CLOUD_BINDINGS_ENABLED   true   Deprecated - whether to auto-configure Spring Boot environment properties from bindings  
[INFO]     [creator]       Creating slices from layers index
[INFO]     [creator]         dependencies
[INFO]     [creator]         spring-boot-loader
[INFO]     [creator]         snapshot-dependencies
[INFO]     [creator]         application
[INFO]     [creator]       Launch Helper: Contributing to layer
[INFO]     [creator]         Creating /layers/paketo-buildpacks_spring-boot/helper/exec.d/spring-cloud-bindings
[INFO]     [creator]       Spring Cloud Bindings 1.9.0: Contributing to layer
[INFO]     [creator]         Downloading from https://repo.spring.io/release/org/springframework/cloud/spring-cloud-bindings/1.9.0/spring-cloud-bindings-1.9.0.jar[INFO]     [creator]         Verifying checksum
[INFO]     [creator]         Copying to /layers/paketo-buildpacks_spring-boot/spring-cloud-bindings
[INFO]     [creator]       Web Application Type: Contributing to layer
[INFO]     [creator]         Servlet web application detected
[INFO]     [creator]         Writing env.launch/BPL_JVM_THREAD_COUNT.default
[INFO]     [creator]       4 application slices
[INFO]     [creator]       Image labels:
[INFO]     [creator]         org.opencontainers.image.title
[INFO]     [creator]         org.opencontainers.image.version
[INFO]     [creator]         org.springframework.boot.version
[INFO]     [creator]     ===> EXPORTING
[INFO]     [creator]     Adding layer 'paketo-buildpacks/ca-certificates:helper'
[INFO]     [creator]     Adding layer 'paketo-buildpacks/bellsoft-liberica:helper'
[INFO]     [creator]     Adding layer 'paketo-buildpacks/bellsoft-liberica:java-security-properties'
[INFO]     [creator]     Adding layer 'paketo-buildpacks/bellsoft-liberica:jre'
[INFO]     [creator]     Adding layer 'paketo-buildpacks/executable-jar:classpath'
[INFO]     [creator]     Adding layer 'paketo-buildpacks/spring-boot:helper'
[INFO]     [creator]     Adding layer 'paketo-buildpacks/spring-boot:spring-cloud-bindings'
[INFO]     [creator]     Adding layer 'paketo-buildpacks/spring-boot:web-application-type'
[INFO]     [creator]     Adding layer 'launch.sbom'
[INFO]     [creator]     Adding 5/5 app layer(s)
[INFO]     [creator]     Adding layer 'launcher'
[INFO]     [creator]     Adding layer 'config'
[INFO]     [creator]     Adding layer 'process-types'
[INFO]     [creator]     Adding label 'io.buildpacks.lifecycle.metadata'
[INFO]     [creator]     Adding label 'io.buildpacks.build.metadata'
[INFO]     [creator]     Adding label 'io.buildpacks.project.metadata'
[INFO]     [creator]     Adding label 'org.opencontainers.image.title'
[INFO]     [creator]     Adding label 'org.opencontainers.image.version'
[INFO]     [creator]     Adding label 'org.springframework.boot.version'
[INFO]     [creator]     Setting default process type 'web'
[INFO]     [creator]     Saving docker.io/springio/gs-spring-boot-docker:latest...
[INFO]     [creator]     *** Images (455cf014fe9d):
[INFO]     [creator]           docker.io/springio/gs-spring-boot-docker:latest
[INFO]     [creator]     Adding cache layer 'paketo-buildpacks/syft:syft'
[INFO]     [creator]     Adding cache layer 'cache.sbom'
[INFO] 
[INFO] Successfully built image 'docker.io/springio/gs-spring-boot-docker:latest'
[INFO]
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  50.236 s
[INFO] Finished at: 2022-05-26T07:36:26+08:00
[INFO] ------------------------------------------------------------------------
```

从上面的日志可以看出 `spring-boot:build-image` 是通过 [Paketo Buildpacks](https://paketo.io/) 来构建镜像的。然后再次使用 `docker run` 运行：

```
$ docker run -p 8080:8080 springio/gs-spring-boot-docker
Setting Active Processor Count to 2
WARNING: Unable to convert memory limit "max" from path "/sys/fs/cgroup/memory.max" as int: memory size "max" does not match pattern "^([\\d]+)([kmgtKMGT]?)$"
Calculating JVM memory based on 994264K available memory
`For more information on this calculation, see https://paketo.io/docs/reference/java-reference/#memory-calculator
Calculated JVM Memory Configuration: -XX:MaxDirectMemorySize=10M -Xmx399558K -XX:MaxMetaspaceSize=82705K -XX:ReservedCodeCacheSize=240M -Xss1M (Total Memory: 994264K, Thread Count: 250, Loaded Class Count: 12188, Headroom: 0%)
Enabling Java Native Memory Tracking
Adding 128 container CA certificates to JVM truststore
Spring Cloud Bindings Enabled
Picked up JAVA_TOOL_OPTIONS: -Djava.security.properties=/layers/paketo-buildpacks_bellsoft-liberica/java-security-properties/java-security.properties -XX:+ExitOnOutOfMemoryError -XX:ActiveProcessorCount=2 -XX:MaxDirectMemorySize=10M -Xmx399558K -XX:MaxMetaspaceSize=82705K -XX:ReservedCodeCacheSize=240M -Xss1M -XX:+UnlockDiagnosticVMOptions -XX:NativeMemoryTracking=summary -XX:+PrintNMTStatistics -Dorg.springframework.cloud.bindings.boot.enable=true

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/
 :: Spring Boot ::                (v2.7.0)

2022-05-26 00:00:50.350  INFO 1 --- [           main] com.example.demo.DemoApplication         : Starting DemoApplication v0.0.1-SNAPSHOT using Java 11.0.15 on f5a936d191b1 with PID 1 (/workspace/BOOT-INF/classes started by cnb in /workspace)
2022-05-26 00:00:50.357  INFO 1 --- [           main] com.example.demo.DemoApplication         : No active profile set, falling back to 1 default profile: "default"
2022-05-26 00:00:51.537  INFO 1 --- [           main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat initialized with port(s): 8080 (http)
2022-05-26 00:00:51.555  INFO 1 --- [           main] o.apache.catalina.core.StandardService   : Starting service [Tomcat]
2022-05-26 00:00:51.556  INFO 1 --- [           main] org.apache.catalina.core.StandardEngine  : Starting Servlet engine: [Apache Tomcat/9.0.63]
2022-05-26 00:00:51.672  INFO 1 --- [           main] o.a.c.c.C.[Tomcat].[localhost].[/]       : Initializing Spring embedded WebApplicationContext
2022-05-26 00:00:51.672  INFO 1 --- [           main] w.s.c.ServletWebServerApplicationContext : Root WebApplicationContext: initialization completed in 1167 ms
2022-05-26 00:00:52.071  INFO 1 --- [           main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat started on port(s): 8080 (http) with context path ''
2022-05-26 00:00:52.098  INFO 1 --- [           main] com.example.demo.DemoApplication         : Started DemoApplication in 2.396 seconds (JVM running for 2.811)
```

> 从日志可以看到程序在启动时，使用 [Memory Calculator](https://paketo.io/docs/reference/java-reference/#memory-calculator) 来动态调整 JVM 内存参数。

## Spring Profiles

在运行上面的镜像时，还可以通过 `SPRING_PROFILES_ACTIVE` 环境变量来指定 Spring Profile：

```
$ docker run -e "SPRING_PROFILES_ACTIVE=prod" -p 8080:8080 springio/gs-spring-boot-docker
```

## 在容器中调试程序

我们可以使用 JPDA Transport 来远程调试一个 Java 程序。在运行上面的镜像时，通过在 `JAVA_TOOL_OPTIONS` 环境变量中添加一个 Java Agent 参数可以让程序以调试模式启动：

```
$ docker run -e "JAVA_TOOL_OPTIONS=-agentlib:jdwp=transport=dt_socket,address=5005,server=y,suspend=n" -p 8080:8080 -p 5005:5005 springio/gs-spring-boot-docker
```

这里使用了环境变量 `JAVA_TOOL_OPTIONS`，在有些应用中，我们不方便设置 JVM 参数，比如命令行应用、通过 JNI API 调用虚拟机的应用、脚本嵌入虚拟机中的应用等。这种情况下 `JAVA_TOOL_OPTIONS` 是非常有用的，它会被 JNI API 的 `JNI_CreateJavaVM` 函数使用，在启动应用的过程中，可以看到 "Picked up" 这样的提示信息。

我们偶尔还能遇到其他几个和 `JAVA_TOOL_OPTIONS` 类似的环境变量：`JAVA_OPTS` 常用于一些应用的配置，如 Tomcat，但它一般不作为环境变量，也不能被 JVM 识别，是那些应用的自定义配置；`_JAVA_OPTIONS` 也可以作为环境变量来替代命令行参数，但它是 JVM 厂家自定义的，可以覆盖 `JAVA_TOOL_OPTIONS`，但各厂家的不同，`_JAVA_OPTIONS` 是 Oracle 的 JVM，而 IBM 的则是用 `IBM_JAVA_OPTIONS`，不像 `JAVA_TOOL_OPTIONS` 是标准的，所有虚拟机都能识别。

在我们这个例子中，因为我们在 Dockerfile 的 `ENTRYPOINT` 中已经指定了启动命令：`java -jar /app.jar`，如果要改 JVM 参数，必须修改 Dockerfile 重新构建镜像：

```
FROM openjdk:17-jdk-alpine
ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} app.jar
ENTRYPOINT ["java","-agentlib:jdwp=transport=dt_socket,address=5005,server=y,suspend=n","-jar","/app.jar"]
```

这就很麻烦了。通过使用 `JAVA_TOOL_OPTIONS` 就不用修改 Dockerfile 了。

## 参考

1. [The JAVA_TOOL_OPTIONS Environment Variable](https://docs.oracle.com/javase/8/docs/technotes/guides/troubleshoot/envvars002.html)
1. [理解环境变量 JAVA_TOOL_OPTIONS](https://segmentfault.com/a/1190000008545160)

## 更多

1. [Spring Boot Maven Plugin Documentation](https://docs.spring.io/spring-boot/docs/current/maven-plugin/reference/htmlsingle/)
1. [Jib](https://github.com/GoogleContainerTools/jib)
1. [Paketo Buildpacks](https://paketo.io/)
1. [Cloud Native Buildpacks](https://buildpacks.io/)
