package com.example.nacos;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.alibaba.nacos.api.annotation.NacosInjected;
import com.alibaba.nacos.api.naming.NamingService;

@SpringBootApplication
@RestController
public class NacosApplication implements CommandLineRunner {

	@Value("${spring.application.name}")
	private String applicationName;

	@Value("${server.port}")
	private Integer serverPort;
	
	@NacosInjected
	private NamingService namingService;
	
	public static void main(String[] args) {
		SpringApplication.run(NacosApplication.class, args);
	}

	@Override
	public void run(String... args) throws Exception {
		namingService.registerInstance(applicationName, "192.168.1.40", serverPort);
	}

	@RequestMapping("/")
	public String home() {
		return String.format("Hello, I'm nacos client.");
	}
}
