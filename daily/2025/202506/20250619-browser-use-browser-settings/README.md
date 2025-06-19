# 详解 Browser Use 的浏览器配置

昨天我们学习了 Browser Use 启动或连接浏览器的几种方法，包括 `executable_path`、Playwright 对象、Browser Server、CDP 和 PID 等，这些方法有一个共同点，都是通过 `BrowserSession` 类来设置参数，而这个类也是 Browser Use 配置和操作浏览器的核心。

`BrowserSession` 的配置参数非常繁杂，不过可以将其大致分为两类，一类是 **会话相关参数（Session-Specific Parameters）**，包括浏览器连接参数和活动的 Playwright 对象实例，`BrowserSession` 通过这些参数连接浏览器并跟踪其活动；另一类是 **浏览器配置模版（Browser Profile）**，包括 Browser Use 特有的参数和 Playwright 相关的参数，这类参数的特点是静态的，可以通过 `BrowserProfile` 存储，方便 `BrowserSession` 复用。

我们今天就对照官方文档，对这些参数做个盘点。

## 会话相关参数

会话相关参数，包括浏览器连接参数和 Playwright 对象实例，这些参数和活动的会话相关，无法存储在 `BrowserProfile(...)` 模板中。

### 浏览器连接参数

这些参数分别对应不同的连接到现有浏览器的方式，在昨天的文章中我们已经详细学过这些内容：

| 参数名                        | 默认值             | 参数说明                                                                |
|------------------------------|--------------------|-----------------------------------------------------------------------|
| `wss_url`                    | `None`             | 连接到 Playwright 协议的浏览器服务器地址                                   |
| `cdp_url`                    | `None`             | 通过 CDP 协议连接到开启调试模式的 Chrome 浏览器                             |
| `browser_pid`                | `None`             | 根据 PID 连接到本地运行的浏览器进程                                         |

### Playwright 对象实例

我们知道，`Browser`、`BrowserContext` 和 `Page` 都是 Playwright 内置的对象，一般通过 `(await async_playwright().start())` 或 `(await async_patchright().start())` 以调试模式启动浏览器子进程，然后通过 CDP 将命令传递给浏览器。

我们可以将这些对象传递给 `BrowserSession`，让 Browser Use 连接并复用已有的浏览器实例：

| 参数名                        | 默认值             | 参数说明                                                                |
|------------------------------|--------------------|-----------------------------------------------------------------------|
| `playwright`                 | `None`             | 可选的 Playwright 或 Patchright API 客户端句柄                           |
| `browser`                    | `None`             | 可选的 Playwright Browser 对象                                          |
| `browser_context`            | `None`             | 可选的 Playwright BrowserContext 对象                                   |
| `page`                       | `None`             | 也可以写成 `agent_current_page`，表示智能体专注的前台页面                    |
| `human_current_page`         | `None`             | 人类专注的前台页面，不必手动设置                                            |
| `initialized`                | `False`            | 将 BrowserSession 标记为已初始化，跳过启动和连接（不推荐）                    |

## 浏览器配置模版

```python
browser_profile: BrowserProfile = BrowserProfile()
```

`BrowserSession` 可以接受一个可选的 `browser_profile` 参数，它是一个配置模板，可以包含一些配置默认值，用法如下：

```python
browser_profile = BrowserProfile(
  executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  user_data_dir='~/.config/browseruse/profiles/default',
)
browser_session = BrowserSession(    
  browser_profile=browser_profile
)
```

所有 `BrowserProfile` 中的参数都可以直接传给 `BrowserSession`，下面的写法和上面的代码没有区别：

```python
browser_session = BrowserSession(    
  executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  user_data_dir='~/.config/browseruse/profiles/default',
)
```

如果某个参数同时传给 `BrowserProfile` 和 `BrowserSession`，`BrowserSession` 中的参数值会覆盖 `BrowserProfile` 中的默认值。

尽管 `BrowserProfile` 是可选的，将参数传给 `BrowserProfile` 或者 `BrowserSession` 都可以，但使用 `BrowserProfile` 提供了一些额外的好处：

* 直接传给 `BrowserSession` 的 `**kwargs` 参数，是一个普通的 `dict` 字典，而传给 `BrowserProfile` 的参数具有明确的类型提示，在 IDE 中还能显示其 `pydantic` 字段描述；
* 传给 `BrowserProfile` 的参数在启动浏览器之前就可以快速验证；
* `BrowserProfile` 提供了一些辅助方法用来自动检测屏幕大小，设置本地路径，保存或加载配置为 json 等；

除此之外，`BrowserProfile` 更大的一个用处是将一些可重用的静态配置独立出来，保存到数据库中，用户对其查看和编辑，供用户的不同会话复用。一个用户常用的配置文件可能只有 2 到 3 个，但他创建的浏览器会话却可能多达成千上万个，将动态的浏览器连接信息和静态的可重用配置分开，可以极大的避免数据库空间的浪费。

`BrowserProfile` 的参数可以分为 **Browser Use 参数** 和 **Playwright 参数**，下面将分别介绍。

## Browser Use 参数

这些参数控制 Browser Use 的特定功能，区别于 Playwright 参数。它们可以传递给 `BrowserSession(...)` 或存储在 `BrowserProfile` 模板中。

```python
keep_alive: bool | None = None
```

如果该参数设置为 `True` ，则将在 `agent.run()` 结束后不关闭浏览器，这对于使用同一浏览器实例运行多个任务非常有用。如果将其保留为 `None` ，则根据 Browser Use 运行时是否启动浏览器来决定是否关闭：如果 Browser Use 启动了自己的浏览器，则完成任务后关闭浏览器，如果 Browser Use 连接到现有浏览器，则将保持其打开状态。

```python
stealth: bool = False
```

Browser Use 默认使用 Playwright 操作浏览器，但是很容易被当成机器人检测出来，[Patchright](https://github.com/Kaliiiiiiiiii-Vinyzu/patchright) 基于 Playwright 改造，使得浏览器操作可以绕过机器人检测。设置 `stealth=True` 表示使用 Patchright 操作浏览器。

```python
allowed_domains: list[str] | None = None
```

允许浏览器访问的域名列表，如果为 None，则允许所有域名，支持 GLOB 匹配模式：

* `['example.com']` - 仅会完全匹配 `https://example.com/*` ，不允许子域名。为确保安全性，请明确列出你希望授予访问权限的所有域名。
* `['*.example.com']` - 这将匹配 `https://example.com` 及其所有子域名，包括 `abc.example.com` , `def.example.com` , `admin.example.com` 等，你需要确保所有子域名的安全性！

```python
disable_security: bool = False
```

完全禁用所有基本的浏览器安全功能，比如允许和跨站点 iFrame 进行交互，但 **此选项非常不安全**，仅适用于小众用例，请慎用。

```python
deterministic_rendering: bool = False
```

通过禁用特定于操作系统的字体提示、抗锯齿、GPU 加速渲染，标准化 DPI，并设置特定的 JS 随机种子以尝试避免非确定性 JS，实现更确定性的渲染，以便在不同的主机操作系统和硬件上获得一致的屏幕截图。这个参数较少使用，而且更容易被视为机器人并偶尔触发一些故障行为，除非你知道需要它，否则不推荐使用。

```python
highlight_elements: bool = True
```

在屏幕上用彩色边框突出显示交互元素。

```python
viewport_expansion: int = 500
```

以像素为单位的视口扩展。通过此功能，可以控制在 LLM 的上下文中包含页面的多少部分：

* `-1` : 页面上的所有元素都将被包含，无论其可见性如何（最高的令牌使用量，但最完整）；
* `0` : 只有当前在视口中可见的元素会被包含；
* `500` (默认): 视口中的元素加上每个方向额外的 500 像素将被包含在内，从而在上下文和令牌使用之间提供平衡；

```python
include_dynamic_attributes: bool = True
```

在选择器中包含动态属性以更好地定位元素。

```python
minimum_wait_page_load_time: float = 0.25
```

捕获页面状态之前的最短等待时间。

```python
wait_for_network_idle_page_load_time: float = 0.5
```

等待网络活动停止的时间。对于较慢的网站，可以增加到 3-5 秒。注意，这只跟踪基本内容的加载，而不是视频等动态元素。

```python
maximum_wait_page_load_time: float = 5.0
```

最大等待页面加载的时间。

```python
wait_between_actions: float = 0.5
```

执行动作之间的等待时间。

```python
cookies_file: str | None = None
```

保存 cookies 的 JSON 文件路径，此选项已弃用，请改用 `storage_state` 参数。

```python
profile_directory: str = 'Default'
```

你在 `user_data_dir` 中的 Chrome 配置文件子目录名称（例如 `Default` 、 `Profile 1` 、 `Work` 等）。除非你在单个 `user_data_dir` 中设置了多个配置文件并需要使用特定的配置文件，否则无需设置此项。

```python
window_size: dict | None = None
```

有头模式的浏览器窗口大小，示例： `{"width": 1920, "height": 1080}`

```python
window_position: dict | None = {"width": 0, "height": 0}
```

窗口位置，从左上角开始。

## Playwright 参数

以下所有参数都是标准的 Playwright 参数，可以传递给 `BrowserSession` 或 `BrowserProfile` 来控制浏览器设置，由于数量众多，这里只作简单总结，不能一一详解。可以参考 Playwright 官方文档了解每个参数的详细用法。

### 启动选项

```python
headless: bool | None = None
```

是否开启无头模式，无头模式指的是在没有用户界面的情况下运行浏览器；默认为 `None`，根据显示可用性自动检测。设置 `headless=False` 可以提供最大的隐蔽性，也是人机协作所必需的。

如果在没有连接显示器的服务器上设置 `headless=False` ，浏览器将无法启动，可以使用 **xvfb + vnc** 为无头浏览器提供一个可以远程控制的虚拟显示。

```python
channel: BrowserChannel = 'chromium'
```

浏览器频道，可选值有：

* 'chromium' - 当 `stealth=False` 时为默认
* 'chrome' - 当 `stealth=True` 时为默认
* 'chrome-beta'
* 'chrome-dev'
* 'chrome-canary'
* 'msedge'
* 'msedge-beta'
* 'msedge-dev'
* 'msedge-canary'

对于列表中未列出的其他基于 Chromium 的浏览器也是支持的，例如 Brave，只要提供自己的 `executable_path` 参数，并将 `channel` 设置为 `chromium` 即可。

```python
executable_path: str | Path | None = None
```

用于启动用户自己安装的浏览器。

```python
user_data_dir: str | Path | None = '~/.config/browseruse/profiles/default'
```

浏览器配置文件数据的目录，设置为 `None` 表示使用临时配置文件，即隐身模式。注意，多个运行中的浏览器不能同时共享一个 `user_data_dir`，如果你需要同时运行多个浏览器，必须将其设置为 `None` 或为每个会话提供一个唯一的 `user_data_dir` 。

```python
args: list[str] = []
```

传递给浏览器的其他命令行参数，下面这个链接列出了 Chrome 所有可用的参数：

* https://gist.github.com/dodying/34ea4760a699b47825a766051f47d43b

```python
ignore_default_args: list[str] | bool = ['--enable-automation', '--disable-extensions']
```

Playwright 在启动 Chrome 时过滤掉列表中指定的参数，如果将其设置为 `True` 则禁用 Playwright 所有默认选项，只使用 `args` 中的参数（不推荐）。

```python
env: dict[str, str] = {}
```

启动浏览器时要设置的额外环境变量，例如，`{'DISPLAY': '1'}` 用于使用特定的 X11 显示。

```python
chromium_sandbox: bool = not IN_DOCKER
```

是否启用 Chromium 沙箱提高安全性，在 Docker 内部运行时，应该设为 `False`，因为 Docker 提供了自己的沙箱，可能与 Chrome 的沙箱冲突。

```python
devtools: bool = False
```

是否为每个标签页自动打开开发者工具面板，如果此选项为 `True`，则无头选项 `headless` 将设置为 `False`。

```python
slow_mo: float = 0
```

通过指定的毫秒数减慢 Playwright 操作，方便用户看清发生了什么。

```python
accept_downloads: bool = True
```

是否自动接受所有下载。

```python
downloads_path: str | Path | None = '~/.config/browseruse/downloads'
```

本地文件系统目录，用于保存浏览器下载的文件，该参数还有两个别名 `downloads_dir` 和 `save_downloads_path`，但是推荐使用标准的 `downloads_path`。

```python
base_url: str | None = None
```

当设置 `base_url` 之后，调用 `page.goto()`、`page.route()`、`page.wait_for_url()` 等操作时可以使用相对 URL 路径。

```python
proxy: dict | None = None
```

为浏览器设置代理，示例如下：

```python
{
  "server": "http://proxy.com:8080",
  "username": "user",
  "password": "pass"
}
```

```python
permissions: list[str] = ['clipboard-read', 'clipboard-write', 'notifications']
```

授予浏览器权限，点击下面的链接获取可用权限的完整列表：

* https://playwright.dev/python/docs/api/class-browsercontext#browser-context-grant-permissions

```python
storage_state: str | Path | dict | None = None
```

使用特定的浏览器存储状态，可以通过下面的命令生成存储状态文件：

```sh
$ playwright open https://example.com/ --save-storage=./storage_state.json
```

存储状态文件中包含 cookies 和 localStorage 等，然后通过下面的方式使用它（注意 `user_data_dir` 必须设置成 `None`）：

```python
session = BrowserSession(
  storage_state='./storage_state.json',
  user_data_dir=None
)
```

### 超时设置

| 参数名                        | 默认值             | 参数说明                                                                 |
|------------------------------|--------------------|-----------------------------------------------------------------------|
| `timeout`                    | `30000`             | 连接远程浏览器的默认超时时间（毫秒）                                       |
| `default_timeout`            | `None`             | Playwright 操作的默认超时时间（毫秒）                                      |
| `default_navigation_timeout` | `None`             | 页面导航的默认超时时间（毫秒）                                              |

### 视口选项

| 参数名               | 默认值             | 参数说明                                                                       |
|----------------------|--------------------|-----------------------------------------------------------------------------|
| `viewport`           | `None`             | 使用 width 和 height 的视口大小，示例： `{"width": 1280, "height": 720}`        |
| `no_viewport`        | `not headless`     | 禁用固定视口，内容将随窗口调整大小，注意，不要使用此参数                            |
| `device_scale_factor`| `None`             | 设备缩放因子（DPI），适用于高分辨率截图（设置为 `2`）                             |
| `screen`             | `None`             | 可供浏览器使用的屏幕大小，如果未指定，则自动检测                                  |
| `color_scheme`       | `'light'`          | 首选颜色方案： `'light'`， `'dark'`， `'no-preference'`                        |
| `contrast`           | `'no-preference'`  | 对比度偏好： `'no-preference'`， `'more'`， `'null'`                           |
| `reduced_motion`     | `'no-preference'`  | 减少运动偏好： `'reduce'`， `'no-preference'`， `'null'`                       |
| `forced_colors`      | `'none'`           | 强制颜色模式： `'active'`， `'none'`， `'null'`                                |

### 设备模拟

| 参数名       | 默认值 | 参数说明                                                                                                 |
|-------------|--------|---------------------------------------------------------------------------------------------------------|
| `offline`    | `False` | 模拟网络离线                                                                                           |
| `user_agent` | `None` | 为浏览器设置特定的 `User-Agent` 头                                                                         |
| `is_mobile`  | `False` | 是否考虑 `meta viewport` 标签并启用触摸事件                                                                |
| `has_touch`  | `False` | 指定视口是否支持触摸事件                                                                                  |
| `geolocation`| `None` | 地理位置坐标，示例： `{"latitude": 59.95, "longitude": 30.31667}`                                       |
| `locale`     | `None` | 指定用户区域设置，例如 `en-GB`、`de-DE` 等，区域设置将影响 `navigator.language` 值、`Accept-Language` 请求头值以及数字和日期格式规则 |
| `timezone_id`| `None` | 时区标识符（例如，`‘America/New_York’`）                                                                |

除此之外，还可以通过 `playwright.devices` 来模拟常见的设备：

```python
BrowserProfile(
    ...
    **playwright.devices['iPhone 13'],
)
```

支持接受所有标准的 Playwright 参数，参考这里：

* https://playwright.dev/python/docs/emulation

### 安全选项

| 参数名                | 默认值                     | 参数说明                                              |
|-----------------------|---------------------------|-----------------------------------------------------|
| `http_credentials`   | `None`                   | HTTP 身份验证的凭据                               |
| `extra_http_headers` | `{}`                     | 每个请求将发送的附加 HTTP 头                      |
| `ignore_https_errors`| `False`                  | 在发送网络请求时是否忽略 HTTPS 错误                |
| `bypass_csp`         | `False`                  | 是否绕过内容安全策略（Content-Security-Policy）    |
| `java_script_enabled`| `True`                   | 是否启用 JavaScript                      |
| `service_workers`    | `'allow'`                | 是否允许页面注册使用 Service Workers： `'allow'`， `'block'` |
| `strict_selectors`   | `False`                  | 如果为真，传递给 Playwright 方法的选择器将在匹配多个元素时抛出错误 |
| `client_certificates`| `[]`                     | 用于请求的客户端证书                              |

### 录制跟踪

| 参数名                   | 默认值                 | 参数说明                                               |
|--------------------------|-----------------------|------------------------------------------------------|
| `record_video_dir`     | `None`               | 别名 `save_recording_path`，保存 `.webm` 视频录制的目录 |
| `record_video_size`    | `None`               | 视频大小，示例：`{"width": 1280, "height": 720}`                                     |
| `record_har_path`      | `None`               | 别名 `save_har_path`，保存 `.har` 网络跟踪文件的路径     |
| `record_har_content`   | `'embed'`            | 如何持久化 HAR 内容：`'omit'`、`'embed'` 或 `'attach'`                                 |
| `record_har_mode`      | `'full'`             | HAR 录制模式：`'full'` 或 `'minimal'`                                                 |
| `record_har_omit_content` | `False`            | 是否从 HAR 中省略请求内容                                                            |
| `record_har_url_filter` | `None`              | HAR 录制的 URL 过滤器                                                                |
| `traces_dir`           | `None`               | 别名 `trace_path`，保存所有跟踪文件的目录，文件自动命名为 `{traces_dir}/{context_id}.zip`  |

### 信号处理

| 参数名                   | 默认值                 | 参数说明                                      |
|--------------------------|-----------------------|---------------------------------------------|
| `handle_sighup`        | `True`               | 是否让 Playwright 捕获 `SIGHUP` 信号并终止浏览器|
| `handle_sigint`        | `False`              | 是否让 Playwright 捕获 `SIGINT` 信号并终止浏览器，也就是 `Ctrl+C` 发送的信号 |
| `handle_sigterm`       | `False`              | 是否让 Playwright 捕获 `SIGTERM` 信号并终止浏览器，也就是 `kill` 默认发送的信号 |

## 小结

我们今天主要学习了 Browser Use 中关于浏览器的配置参数，鉴于浏览器的复杂性，相关参数也是非常的多，主要可以分为会话相关参数和浏览器配置模版；还学习了 `BrowserProfile` 和 `BrowserSession` 的区别和用途，可以将静态的浏览器配置存储在 `BrowserProfile` 里，供 `BrowserSession` 复用。更多细节可以参考 Browser Use 和 Playwright 的官方文档：

* https://docs.browser-use.com/customize/browser-settings
* https://playwright.dev/python/docs/api/class-browsertype
* https://playwright.dev/python/docs/api/class-browsercontext
