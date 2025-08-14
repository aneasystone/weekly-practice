package main

import (
	"context"

	"github.com/cloudwego/eino/compose"
)

type AddParam struct {
	A int
	B int
}

func add(ctx context.Context, param AddParam) (int, error) {
	return param.A + param.B, nil
}

type Request struct {
	X int
	Y int
	Z int
}

func main() {

	// 创建工作流
	wf := compose.NewWorkflow[Request, int]()

	// 第一个 add 节点
	wf.AddLambdaNode("add1", compose.InvokableLambda(add)).
		AddInput(
			compose.START,
			compose.MapFields("X", "A"),
			compose.MapFields("Y", "B"),
		)

		// 第二个 add 节点
	wf.AddLambdaNode("add2", compose.InvokableLambda(add)).
		AddInput(compose.START, compose.MapFields("Z", "A")).
		AddInput("add1", compose.ToField("B"))

	wf.End().AddInput("add2")

	// 编译工作流
	run, err := wf.Compile(context.Background())
	if err != nil {
		panic(err)
	}

	// 调用工作流
	result, _ := run.Invoke(context.Background(), Request{
		X: 1,
		Y: 2,
		Z: 3,
	})
	println(result)
}
