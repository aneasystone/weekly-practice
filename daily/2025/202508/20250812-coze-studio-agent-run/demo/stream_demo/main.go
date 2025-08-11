package main

import (
	"context"
	"os"

	"github.com/cloudwego/eino-ext/components/model/openai"
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

	// 准备消息
	messages := []*schema.Message{
		schema.SystemMessage("你是一个翻译专家，擅长中文和英文之间的互译。"),
		schema.UserMessage("你好，世界！"),
	}

	// 流式读取消息
	reader, _ := model.Stream(ctx, messages)
	defer reader.Close()
	for {
		chunk, err := reader.Recv()
		if err != nil {
			break
		}
		print(chunk.Content)
	}
}
