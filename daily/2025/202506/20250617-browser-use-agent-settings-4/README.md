# 详解 Browser Use 的 Agent 用法（四）

经过这几天的学习，总算把 Browser Use `Agent` 所有的配置参数都搞清楚了，我们今天先对这些参数做一个总结回顾，然后继续来研究下 `agent.run()` 方法，学习它的基本用法和生命周期钩子等概念。

## 配置参数回顾

下面这张表格概括了 `Agent` 所有的配置参数，以及它的默认值和功能说明，可以帮助大家快速理解和回顾之前学习的内容：

| 参数名                 | 默认值                     | 参数说明                                                                                      |
|----------------------|-------------------------|-------------------------------------------------------------------------------------------|
| `task`              | 必填                     | 表示智能体需要完成的任务，通常为自然语言描述。                                                          |
| `llm`               | 必填                     | 使用的大语言模型实例。支持 DeepSeek、GPT-4 等。                                                      |
| `page`              | `None`                  | Playwright 的 `Page` 对象，用于让智能体直接使用预初始化的网页。                                                   |
| `browser`           | `None`                  | Playwright 的 `Browser` 对象，用于指定浏览器实例。                                                       |
| `browser_context`   | `None`                  | Playwright 的 `BrowserContext` 对象，用于设置独立的浏览器上下文。                                                 |
| `browser_profile`   | `None`                  | Browser Use 内置的配置类，包括浏览器启动参数、连接参数和默认的视图信息。                                             |
| `browser_session`   | `None`                  | Browser Use 内置的会话类，表示活跃的浏览器会话（实例化后的浏览器进程）。                                                |
| `controller`        | `Controller()`          | 自定义工具管理类，可以通过装饰器 `@controller.action` 注册工具。升华智能体功能。                                          |
| `context`           | `None`                  | 任意用户自定义的上下文对象，例如数据库连接、文件句柄或运行时配置，仅透传给自定义工具。                                           |
| `override_system_message` | `None`           | 重写系统提示词的内容，用于替换默认的任务规划和工具调用提示词。                                                          |
| `extend_system_message`   | `None`           | 在默认提示词后追加内容，用于增强提示词，而不是完全替换。建议优先使用。                                                      |
| `max_actions_per_step`    | `10`              | 一次最多执行多少个大模型生成的动作，控制任务中模型生成动作的数目。                                                        |
| `message_context`         | `None`           | 附加的任务上下文描述，用于让模型更好地理解任务或场景。                                                         |
| `max_input_tokens`        | `128000`         | 最大支持输入 token 数，模型的上下文窗口大小（如 DeepSeek V3 为 64K，GPT-4 为 128K）。                                       |
| `tool_calling_method`     | `'auto'`         | 控制工具调用方式，可选 `function_calling`、`json_mode`、`raw`、`tools`、`auto`。                                      |
| `use_vision`              | `True`           | 是否开启视觉能力，表示是否将网页截图作为消息的一部分。禁用能降低 token 消耗。                                               |
| `planner_llm`                    | `None`                                                      | 用于规划任务的大语言模型实例，可以是一个比主模型更小或更便宜的模型。                       |
| `use_vision_for_planner`         | `False`                                                     | 是否为规划模型开启视觉能力，如果开启，会传递网页截图给模型。                                                         |
| `planner_interval`               | `1`                                                         | 控制每隔多少步规划一次任务，默认是每步都规划。                                                                |
| `is_planner_reasoning`           | `False`                                                     | 是否通过 `HumanMessage` 而不是 `SystemMessage` 传递规划提示词，适配不支持 `SystemMessage` 的推理模型。         |
| `extend_planner_system_message`  | `None`                                                      | 向默认规划提示词后附加额外内容，用于定制化任务分解的逻辑。                                                        |
| `page_extraction_llm`            | `None`                                                      | 用于页面内容提取的大语言模型实例，如果未配置，默认使用主模型。                                     |
| `initial_actions`                | `None`                                                      | 初始化时执行的固定动作（如打开某个页面），无需调用大模型，能节省 token。                                              |
| `save_conversation_path`         | `None`                                                      | 保存会话记录的目录路径，包含每一步的 Prompt 和模型响应结果，便于调试和分析。                                           |
| `save_conversation_path_encoding`| `'utf-8'`                                                  | 会话记录文件的编码格式，默认为 UTF-8。                                                             |
| `include_attributes`             | `title`, `type`, `name`, `role` 等                          | 保留关键网页元素的部分属性，用于节省 token（默认值包括 `title`, `type` 等带有语义信息的属性）。                        |
| `validate_output`                | `False`                                                     | 完成任务时开启输出校验，确保任务的最终结果准确信息。                                                         |
| `max_failures`                   | `3`                                                         | 遇到异常时的最大重试次数，可处理浏览器异常关闭、token 超限及接口限流等问题。                                           |
| `retry_delay`                    | `10`                                                        | 接口限流错误时延迟的时间（单位：秒），然后重试。                                                                |
| `generate_gif`                   | `False`                                                     | 运行结束后生成操作过程的 GIF 动画，包含任务、每一步目标和截屏记录。                                                 |
| `save_playwright_script_path`    | `None`                                                      | 保存 Playwright 脚本的路径，用于重放操作过程（最新版本已移除，但派生了 Workflow Use 项目）。                             |
| `register_new_step_callback`                                        | `None`                         | 每次调用大模型获取下一步动作之后触发的回调函数，访问当前浏览器状态和大模型输出。                                    |
| `register_done_callback`                                            | `None`                         | 整个任务完成后触发的回调函数，可访问智能体运行的所有历史数据。                                                     |
| `register_external_agent_status_raise_error_callback`               | `None`                         | 自定义是否在异常时触发 `InterruptedError` 的回调，如果返回 `True`，则触发。                                          |
| `injected_agent_state`                                              | `None`                         | 用于注入已保存的智能体状态，支持从中断的地方继续任务。                                                              |
| `enable_memory`                                                     | `True`                         | 是否开启智能体的程序性记忆功能。                                                                                   |
| `memory_config`                                                     | `None`                         | 配置程序性记忆的相关参数，例如间隔步数、嵌入模型、向量数据库等。                                                     |
| `available_file_paths`                                              | `None`                         | 指定智能体可以访问和操作的文件路径列表，会在系统提示语中通知大模型。                                                  |
| `sensitive_data`                                                    | `None`                         | 定义敏感数据及其对应的占位符，可防止敏感信息暴露给大模型。                                                          |
| `source`                                                            | `git` / `pip` / `unknown` | 告知 Browser Use 当前使用的来源场景，默认根据运行环境自动设置。                                                     |

## 生命周期钩子

关于 `Agent` 的配置参数就此告一段落，接下来我们来看看 `agent.run()` 方法的定义：

```python
async def run(
  self, 
  max_steps: int = 100, 
  on_step_start: AgentHookFunc | None = None, 
  on_step_end: AgentHookFunc | None = None
) -> AgentHistoryList:
```

它有三个参数：

* `max_steps` - 限制循环的最大步数，防止智能体陷入死循环，默认是 100 步；
* `on_step_start` - 在智能体处理当前状态并决定下一步行动之前执行；
* `on_step_end` - 在智能体执行完当前步骤的所有操作后执行；

后两个参数被称为 Browser Use 的 **生命周期钩子（Lifecycle Hooks）**，允许你在特定时刻执行自定义代码。我们可以在钩子函数中读取和修改智能体状态，实现自定义逻辑，改变配置，与外部应用程序集成等。

钩子函数类型如下：

```python
AgentHookFunc = Callable[['Agent'], Awaitable[None]]
```

可以看出，每个钩子函数都应该是一个可调用的 `async` 函数，接受 `agent` 实例作为唯一参数：

```python
async def on_step_start(agent: Agent):
  print(f"======== on_step_start {agent.state.n_steps} ========")

async def on_step_end(agent: Agent):
  print(f"======== on_step_end {agent.state.n_steps} ========")
```

我们知道，`Agent` 有一个配置参数 `register_new_step_callback` 用于注册回调，生命周期钩子和它的机制很相似。只不过注册的回调函数参数是 `BrowserStateSummary` 和 `AgentOutput`，可以在函数中访问当前的浏览器状态和大模型的输出，而钩子函数的参数为 `Agent`，可以在函数中访问整个智能体的状态和方法，使用起来更灵活。

## 钩子的访问点

下面是钩子函数中的一些有用的访问点：

* `agent.task` - 让你看到主要任务是什么，可以使用 `agent.add_new_task(...)` 新增一个新的任务；
* `agent.controller` - 用于访问 `Controller` 对象和 `Registry` 对象，包含可用的操作，比如在当前页面上执行某个动作：

```python
agent.controller.registry.execute_action(
  'click_element_by_index',
  {
    'index': 123
  },
  browser_session=agent.browser_session
)
```

* `agent.context` - 让你访问传递给 `Agent(context=...)` 的任何用户提供的上下文对象；
* `agent.sensitive_data` - 包含敏感数据字典，可以就地更新以添加/删除/修改其中的内容；
* `agent.settings` - 包含在初始化时传递给 `Agent(...)` 的所有配置选项；
* `agent.llm` - 直接访问主 LLM 对象 (例如 ChatOpenAI )；
* `agent.state` - 提供对大量内部状态的访问，包括智能体当前的推理、输出、行动等：

```python
# 模型的推理结果
model_thoughts = agent.state.history.model_thoughts()

# 模型的原始输出
model_outputs = agent.state.history.model_outputs()

# 智能体采取的行动
model_actions = agent.state.history.model_actions()

# 从网页提取的内容
extracted_content = agent.state.history.extracted_content()

# 智能体访问的 URL
urls = agent.state.history.urls()
```

* `agent.browser_session` - 直接访问 `BrowserSession` 和 `Playwright` 对象：

```python
# 获取当前的 Page 对象
current_page = agent.browser_session.get_current_page()

# 获取当前的 BrowserContext 对象
browser_context = agent.browser_session.browser_context

# 获取当前上下文中所有打开的标签页
pages = agent.browser_session.browser_context.pages

# 当前页面 HTML
html = agent.browser_session.get_page_html()

# 当前页面的截图
screenshot = agent.browser_session.take_screenshot()
```

更多内容参考官网的 Lifecycle Hooks 文档：

* https://docs.browser-use.com/customize/hooks

## 历史列表和结构化输出

`agent.run()` 方法的返回值是一个 `AgentHistoryList` 对象，其中包含完整的执行历史。这个历史对于调试、分析和创建可重现的脚本是非常有用。下面是该对象常用的一些方法：

```python
history.urls()              # List of visited URLs
history.screenshots()       # List of screenshot paths
history.model_thoughts()    # Get the agent’s reasoning process
history.model_actions()     # All actions with their parameters
history.action_names()      # Names of executed actions
history.action_results()    # Get results of all actions
history.extracted_content() # Content extracted during execution
history.is_done()           # Check if the agent completed successfully
history.has_errors()        # Check if any errors occurred
history.errors()            # Any errors that occurred
history.final_result()      # Get the final extracted content
```

其中 `history.final_result()` 是最常用的，用于输出文本格式的最终结果，不过我们也可以定义一个结构化的输出格式，以便后续处理。比如我们想从豆瓣读书上搜索关于 “大模型” 相关的书籍，并以结构化的形式展示出来，我们可以先定义书籍和书籍列表类型：

```python
from typing import List
from pydantic import BaseModel

class Book(BaseModel):
  book_title: str          # 书名
  author: str              # 作者
  brief_introduction: str  # 简介
  score: float             # 评分

class Books(BaseModel):
  books: List[Book]
```

然后将其绑定在 `Controller` 上：

```python
from browser_use import Controller

controller = Controller(output_model=Books)
```

将这个自定义的 `Controller` 传入 `Agent`，就可以通过 `Books.model_validate_json(...)` 从 `final_result` 中得到结构化结果：

```python
agent = Agent(
  task="进入豆瓣读书，搜索关于大模型相关的书籍，获取排名前三的书籍详情",
  llm=llm,
  controller=controller
)
history = await agent.run()
result = history.final_result()
parsed: Books = Books.model_validate_json(result)
for book in parsed.books:
  print('\n--------------------------------')
  print(f'书名:  {book.book_title}')
  print(f'作者:  {book.author}')
  print(f'简介:  {book.brief_introduction}')
  print(f'评分:  {book.score}')
```

输出结果如下：

```
--------------------------------
书名:  大模型算法：强化学习、微调与对齐
作者:  余昌叶
简介:  涉及强化学习、模型微调与对齐技术的前沿算法介绍。
评分:  9.6

--------------------------------
书名:  从零构建大模型
作者:  [美]塞巴斯蒂安·拉施卡 / 覃立波 / 冯骁骋
简介:  全面介绍大模型的构建方法和技术实践。
评分:  9.3

--------------------------------
书名:  解构大语言模型：从线性回归到通用人工智能
作者:  唐亘
简介:  探讨大语言模型从基础线性回归模型到通用人工智能的演变过程。
评分:  9.6
```

## 小结

到这里，Browser Use 的 Agent 用法基本上就讲解完了，不过之前在讲解浏览器相关的配置时还留了一个小尾巴。浏览器是一个很复杂的话题，比如如何自定义浏览器配置，如何使用 CDP 连接已有的浏览器实例，如何使用 Patchright 绕过浏览器自动化检测，等等等等，我们明天就来学习这些内容，完成 Browser Use 学习拼图中的最后一块。
