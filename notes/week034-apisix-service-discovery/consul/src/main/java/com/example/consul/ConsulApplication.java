package com.example.consul;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@EnableDiscoveryClient
@SpringBootApplication
@RestController
public class ConsulApplication {
	
	public static void main(String[] args) {
		SpringApplication.run(ConsulApplication.class, args);
	}

	@RequestMapping("/")
	public String home() {
		return String.format("Hello, I'm consul client.");
	}
}
