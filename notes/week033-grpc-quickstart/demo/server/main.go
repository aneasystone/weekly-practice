package main

import (
	"context"
	"log"
	"net"

	"example.com/demo/proto"
	"google.golang.org/grpc"
)

type server struct {
	proto.UnimplementedHelloServiceServer
}

func (s *server) SayHello(ctx context.Context, request *proto.HelloRequest) (*proto.HelloResponse, error) {
	log.Printf("Request recieved: %v\n", request.GetName())
	return &proto.HelloResponse{
		Message: "Hello " + request.GetName(),
	}, nil
}

func main() {

	lis, err := net.Listen("tcp", ":8080")
	if err != nil {
		log.Fatalf("Server listen failed!")
	}
	log.Printf("Server listening at: %s", lis.Addr())

	s := grpc.NewServer()
	proto.RegisterHelloServiceServer(s, &server{})
	if err := s.Serve(lis); err != nil {
		log.Fatalf("Server serve failed!")
	}
}
