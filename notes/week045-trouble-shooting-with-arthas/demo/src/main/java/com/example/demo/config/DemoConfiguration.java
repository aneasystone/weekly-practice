package com.example.demo.config;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class DemoConfiguration {
	
	@Bean
	@ConfigurationProperties(prefix = "demo", ignoreUnknownFields = false)
	public DemoProperties demoProperties() {
		return new DemoProperties();
	}
}
