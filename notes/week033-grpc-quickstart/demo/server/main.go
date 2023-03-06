package main

import (
	"context"
	"log"
	"net"
	"strings"

	"example.com/demo/proto"
	"google.golang.org/grpc"
	"google.golang.org/grpc/reflection"
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

func (s *server) Split(request *proto.SplitRequest, stream proto.HelloService_SplitServer) error {
	log.Printf("Request recieved: %v\n", request.GetSentence())
	words := strings.Split(request.GetSentence(), " ")
	for _, word := range words {
		if err := stream.Send(&proto.SplitResponse{Word: word}); err != nil {
			return err
		}
	}
	return nil
}

func main() {

	lis, err := net.Listen("tcp", ":8080")
	if err != nil {
		log.Fatalf("Server listen failed!")
	}
	log.Printf("Server listening at: %s", lis.Addr())

	s := grpc.NewServer()
	proto.RegisterHelloServiceServer(s, &server{})
	reflection.Register(s)
	if err := s.Serve(lis); err != nil {
		log.Fatalf("Server serve failed!")
	}
}
