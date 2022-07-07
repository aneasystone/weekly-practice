package com.example.demo;

import java.util.List;

import org.springframework.boot.actuate.endpoint.annotation.Endpoint;
import org.springframework.boot.actuate.endpoint.annotation.ReadOperation;
import org.springframework.context.annotation.Configuration;

@Endpoint(id = "test")
@Configuration
public class TestEndpoint {
	
	private final List<String> demoList;
	public TestEndpoint(List<String> demoList) {
		this.demoList = demoList;
	}

	@ReadOperation
	public List<String> getDemoList() {
		return this.demoList;
	}
}
