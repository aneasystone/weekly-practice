package com.example.demo;

import reactor.core.publisher.Mono;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.reactive.function.client.WebClient;

@RestController
@SpringBootApplication
public class DemoApplication {

	private WebClient webClient = WebClient.create();

	public static void main(String[] args) {
		SpringApplication.run(DemoApplication.class, args);
	}

	@GetMapping
	public Mono<String> index() {
		return webClient.get().uri("http://k8s-workshop-name-service")
				.retrieve()
				.toEntity(String.class)
				.map(entity -> {
					String host = entity.getHeaders().get("k8s-host").get(0);
					return "Hello " + entity.getBody() + " from " + host;
				});
	}
}
