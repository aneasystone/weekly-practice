package com.example.demo.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import com.example.demo.service.DemoService;
import com.example.demo.model.DemoAdd;

@RestController
public class DemoController {
	
	@Autowired
	private DemoService demoService;

	@PostMapping("/add")
	public String add(@RequestBody DemoAdd demoAdd) {
		try {
			Integer result = demoService.add(demoAdd);
			return String.valueOf(result);
		} catch (Exception e) {
			return "系统错误！";
		}
	}

	@GetMapping("/title")
	public String properties() {
		return demoService.properties().getTitle();
	}

	@GetMapping("/encoding")
	public String encoding() {
		return System.getProperty("file.encoding");
	}

	@GetMapping("/env")
	public String env() {
		return System.getenv("JAVA_HOME");
	}
}
