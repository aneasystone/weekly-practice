package com.example.demo;

import org.springframework.boot.autoconfigure.security.SecurityProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.annotation.Order;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
public class DemoConfiguration {
	
	// @Bean
    // @Order(SecurityProperties.BASIC_AUTH_ORDER - 10)
    // SecurityFilterChain demoSecurityFilterChain(HttpSecurity http) throws Exception {
	// 	http.antMatcher("/index");
    //     http.authorizeRequests().antMatchers("/index").permitAll();
    //     http.formLogin();
    //     http.httpBasic();
    //     return http.build();
    // }
}
