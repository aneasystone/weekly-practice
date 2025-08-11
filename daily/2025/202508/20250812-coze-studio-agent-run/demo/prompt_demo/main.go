package main

import (
	"context"
	"os"

	"github.com/cloudwego/eino-ext/components/model/openai"
	"github.com/cloudwego/eino/components/prompt"
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

	// 使用模板生成消息
	messages, _ := template.Format(context.Background(), map[string]any{
		"from":     "中文",
		"to":       "法语",
		"question": "你好，世界！",
	})

	// 生成回复
	response, _ := model.Generate(ctx, messages)
	println(response.Content)
}
