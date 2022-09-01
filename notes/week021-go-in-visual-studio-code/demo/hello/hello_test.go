package hello_test

import (
	"testing"

	"example.com/demo/hello"
)

func TestSayHello(t *testing.T) {
	if hello.SayHello() != "Hello world" {
		t.Fatal("Not good")
	}
}
