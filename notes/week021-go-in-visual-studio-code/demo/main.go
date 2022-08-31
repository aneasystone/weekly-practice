package main

import (
	"fmt"

	"example.com/demo/hello"
	"rsc.io/quote"
)

func main() {
	fmt.Println(hello.SayHello())
	fmt.Println(quote.Go())
}
