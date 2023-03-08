package main

import (
	"context"
	"io"
	"log"
	"time"

	"example.com/demo/proto"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

func main() {

	conn, err := grpc.Dial("localhost:8080", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("Connect grpc server failed: %v", err)
	}
	defer conn.Close()

	c := proto.NewHelloServiceClient(conn)
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	sayHello(ctx, c)

	split(ctx, c)

	sum(ctx, c)

	chat(ctx, c)
}

// Simple RPC
func sayHello(ctx context.Context, c proto.HelloServiceClient) {
	r, err := c.SayHello(ctx, &proto.HelloRequest{Name: "zhangsan"})
	if err != nil {
		log.Fatalf("Call SayHello failed: %v", err)
	}
	log.Printf("SayHello response: %s", r.GetMessage())
}

// Server-side streaming RPC
func split(ctx context.Context, c proto.HelloServiceClient) {
	stream, err := c.Split(ctx, &proto.SplitRequest{Sentence: "Hello World"})
	if err != nil {
		log.Fatalf("Call Split failed: %v", err)
	}
	for {
		r, err := stream.Recv()
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Fatalf("%v.Split(_) = _, %v", c, err)
		}
		log.Printf("Split response: %s", r.GetWord())
	}
}

// Client-side streaming RPC
func sum(ctx context.Context, c proto.HelloServiceClient) {
	stream, err := c.Sum(ctx)
	if err != nil {
		log.Fatalf("%v.Sum(_) = _, %v", c, err)
	}
	nums := []int32{1, 2, 3, 4, 5, 6, 7}
	for _, num := range nums {
		if err := stream.Send(&proto.SumRequest{Num: num}); err != nil {
			log.Fatalf("%v.Send(%v) = %v", stream, num, err)
		}
	}
	response, err := stream.CloseAndRecv()
	if err != nil {
		log.Fatalf("%v.CloseAndRecv() failed: %v", stream, err)
	}
	log.Printf("Sum response: %v", response.GetSum())
}

// Bidirectional streaming RPC
func chat(ctx context.Context, c proto.HelloServiceClient) {
	stream, err := c.Chat(ctx)
	if err != nil {
		log.Fatalf("%v.Chat(_) = _, %v", c, err)
	}
	waitc := make(chan struct{})
	go func() {
		for {
			in, err := stream.Recv()
			if err == io.EOF {
				close(waitc)
				return
			}
			if err != nil {
				log.Fatalf("Failed to receive: %v", err)
			}
			log.Printf("Chat response: %s", in.GetMessage())
		}
	}()

	messages := []string{"Hello", "How're you?", "Bye"}
	for _, message := range messages {
		if err := stream.Send(&proto.ChatRequest{Message: message}); err != nil {
			log.Fatalf("Failed to send: %v", err)
		}
	}
	stream.CloseSend()
	<-waitc
}
