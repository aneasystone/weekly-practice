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

	r, err := c.SayHello(ctx, &proto.HelloRequest{Name: "zhangsan"})
	if err != nil {
		log.Fatalf("Call SayHello failed: %v", err)
	}
	log.Printf("SayHello response: %s", r.GetMessage())

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
			log.Fatalf("%v.ListFeatures(_) = _, %v", c, err)
		}
		log.Printf("Split response: %s", r.GetWord())
	}
}
