package com.example.demo;

import org.springframework.boot.actuate.autoconfigure.security.servlet.EndpointRequest;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.SecurityFilterChain;
import static org.springframework.security.config.Customizer.withDefaults;

@Configuration
public class DemoSecurityConfiguration {
	
	@Bean
	public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
		http.requestMatcher(EndpointRequest.toAnyEndpoint());
		http.authorizeRequests((requests) -> requests.anyRequest().hasRole("ACTUATOR_ADMIN"));
		http.httpBasic(withDefaults());
		return http.build();
	}
}
