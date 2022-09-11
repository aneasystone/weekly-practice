package main

import (
	"context"
	"fmt"
	"time"

	"go.etcd.io/etcd/clientv3"
)

func main() {
	cli, err := clientv3.New(clientv3.Config{
		Endpoints:   []string{"localhost:2379"},
		DialTimeout: 5 * time.Second,
	})
	if err != nil {
		panic("Connect etcd server error")
	}
	defer cli.Close()

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)

	_, err = cli.Put(ctx, "hello", "world")
	if err != nil {
		panic("Put kv error")
	}

	resp, err := cli.Get(ctx, "hello")
	if err != nil {
		panic("Get kv error")
	}
	for _, kv := range resp.Kvs {
		fmt.Printf("%s: %s\n", kv.Key, kv.Value)
	}

	_, err = cli.Delete(ctx, "hello")
	if err != nil {
		panic("Delete kv error")
	}

	cancel()
}
