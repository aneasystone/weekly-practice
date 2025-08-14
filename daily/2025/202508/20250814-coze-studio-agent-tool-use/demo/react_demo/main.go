package main

import (
	"context"
	"encoding/json"
	"os"

	"github.com/cloudwego/eino-ext/components/model/openai"
	"github.com/cloudwego/eino/components/tool"
	"github.com/cloudwego/eino/compose"
	"github.com/cloudwego/eino/flow/agent/react"
	"github.com/cloudwego/eino/schema"
)

type ToolGetWeather struct {
}

type ToolGetWeatherParam struct {
	City string `json:"city"`
	Date string `json:"date"`
}

func (t *ToolGetWeather) Info(ctx context.Context) (*schema.ToolInfo, error) {
	return &schema.ToolInfo{
		Name: "get_weather",
		Desc: "查询天气",
		ParamsOneOf: schema.NewParamsOneOfByParams(map[string]*schema.ParameterInfo{
			"city": {
				Type:     "string",
				Desc:     "城市名称",
				Required: true,
			},
			"date": {
				Type:     "string",
				Desc:     "日期",
				Required: true,
			},
		}),
	}, nil
}

func (t *ToolGetWeather) InvokableRun(ctx context.Context, argumentsInJSON string, opts ...tool.Option) (string, error) {

	// 解析参数
	p := &ToolGetWeatherParam{}
	err := json.Unmarshal([]byte(argumentsInJSON), p)
	if err != nil {
		return "", err
	}

	res := p.City + p.Date + "天气晴，气温30摄氏度"
	return res, nil
}

func main() {

	ctx := context.Background()

	// 初始化大模型
	model, _ := openai.NewChatModel(ctx, &openai.ChatModelConfig{
		BaseURL: os.Getenv("OPENAI_BASE_URL"),
		APIKey:  os.Getenv("OPENAI_API_KEY"),
		Model:   "gpt-4o",
	})

	// 初始化工具
	toolGetWeather := &ToolGetWeather{}

	// ReAct 智能体
	agent, _ := react.NewAgent(ctx, &react.AgentConfig{
		ToolCallingModel: model,
		ToolsConfig: compose.ToolsNodeConfig{
			Tools: []tool.BaseTool{toolGetWeather},
		},
	})

	r, _ := agent.Generate(ctx, []*schema.Message{
		{
			Role:    schema.User,
			Content: "北京明天的天气怎么样？",
		},
	})
	println(r.Content)

	// sr, _ := agent.Stream(ctx, []*schema.Message{
	// 	{
	// 		Role:    schema.User,
	// 		Content: "北京明天的天气怎么样？",
	// 	},
	// })

	// defer sr.Close()

	// println("\n\n===== start streaming =====\n\n")

	// for {
	// 	msg, err := sr.Recv()
	// 	if err != nil {
	// 		if errors.Is(err, io.EOF) {
	// 			break
	// 		}
	// 		print("failed to recv: %v", err)
	// 		return
	// 	}

	// 	// 打字机打印
	// 	print(msg.Content)
	// }

	// println("\n\n===== finished =====\n")
}
