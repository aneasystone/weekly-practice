package com.example.demo;

import java.util.ArrayList;
import java.util.List;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import io.micrometer.core.instrument.Gauge;
import io.micrometer.core.instrument.binder.MeterBinder;

@Configuration
public class DemoListConfiguration {
    
    @Bean
    public List<String> demoList() {
        return new ArrayList<>();
    }

    @Bean
    public MeterBinder demoListSize(List<String> demoList) {
        return (registry) -> Gauge.builder("list.size", demoList::size).register(registry);
    }
}
