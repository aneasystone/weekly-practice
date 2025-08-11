package main

import (
	"context"
	"os"

	"github.com/cloudwego/eino-ext/components/model/openai"
	"github.com/cloudwego/eino/components/prompt"
	"github.com/cloudwego/eino/compose"
	"github.com/cloudwego/eino/schema"
)

func main() {

	ctx := context.Background()

	// 初始化大模型
	model, _ := openai.NewChatModel(ctx, &openai.ChatModelConfig{
		BaseURL: os.Getenv("OPENAI_BASE_URL"),
		APIKey:  os.Getenv("OPENAI_API_KEY"),
		Model:   "gpt-4o",
	})

	// 创建模板，使用 FString 格式
	template := prompt.FromMessages(schema.FString,
		// 系统消息模板
		schema.SystemMessage("你是一个翻译专家，擅长{from}和{to}之间的互译，如果用户输入的是{from}将其翻译成{to}，如果用户输入的是{to}将其翻译成{from}"),
		// 用户消息模板
		schema.UserMessage("用户输入: {question}"),
	)

	// 构造图
	graph := compose.NewGraph[map[string]any, *schema.Message]()

	_ = graph.AddChatTemplateNode("template", template)
	_ = graph.AddChatModelNode("model", model)

	_ = graph.AddEdge(compose.START, "template")
	_ = graph.AddEdge("template", "model")
	_ = graph.AddEdge("model", compose.END)

	result, err := graph.Compile(ctx)
	if err != nil {
		panic(err)
	}

	// 调用图
	output, _ := result.Invoke(ctx, map[string]any{
		"from":     "中文",
		"to":       "法语",
		"question": "你好，世界！",
	})
	println(output.Content)
}
