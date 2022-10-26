package main

import (
    "syscall/js"
)

func addFunction(this js.Value, p []js.Value) interface{} {
    sum := p[0].Int() + p[1].Int()
    return js.ValueOf(sum)
}

func hello(this js.Value, args []js.Value) interface{} {
    doc := js.Global().Get("document")
    h1 := doc.Call("createElement", "h1")
    h1.Set("innerText", "Hello World")
    doc.Get("body").Call("append", h1)
    return nil
}

func main() {
    js.Global().Set("add", js.FuncOf(addFunction))
    js.Global().Set("hello", js.FuncOf(hello))
    select {} // block the main thread forever
}

