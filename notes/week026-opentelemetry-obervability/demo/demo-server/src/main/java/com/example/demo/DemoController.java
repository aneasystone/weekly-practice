package com.example.demo;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import io.opentelemetry.api.trace.Span;

@RestController
public class DemoController {

	@GetMapping("/greeting")
	public String greeting(@RequestParam(value = "name", defaultValue = "World") String name) {

		Span span = Span.current();
		span.setAttribute("user.name", name);

		return String.format("Hello, %s", name);
	}
}
