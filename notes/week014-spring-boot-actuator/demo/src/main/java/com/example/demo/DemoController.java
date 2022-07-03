package com.example.demo;

import java.util.ArrayList;
import java.util.List;

import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Tags;

@RestController
public class DemoController {

    private final MeterRegistry registry;
    private List<String> demoList = new ArrayList<>();
    
    public DemoController(MeterRegistry registry, List<String> demoList) {
        this.registry = registry;
        this.demoList = demoList;
    }

    @GetMapping("/hello")
    public String hello() {
        this.registry.counter("hello.counter", Tags.of("app", "demo")).increment();
        return "hello";
    }

    @GetMapping("/list")
    public List<String> list() {
        return demoList;
    }

    @PostMapping("/list/{item}")
    public List<String> add(@PathVariable String item) {
        demoList.add(item);
        return demoList;
    }

    @DeleteMapping("/list/{item}")
    public List<String> delete(@PathVariable String item) {
        demoList.remove(item);
        return demoList;
    }
}
