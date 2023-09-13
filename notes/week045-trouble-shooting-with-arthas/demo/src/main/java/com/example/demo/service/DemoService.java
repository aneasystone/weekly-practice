package com.example.demo.service;

import org.springframework.stereotype.Service;

import com.example.demo.config.DemoProperties;
import com.example.demo.model.DemoAdd;

import lombok.extern.slf4j.Slf4j;

@Slf4j
@Service
public class DemoService {
	
	private final DemoProperties demoProperties;
	public DemoService(DemoProperties demoProperties) {
		this.demoProperties = demoProperties;
	}

	public Integer add(DemoAdd demoAdd) {
		log.debug("x = {}, y = {}", demoAdd.getX(), demoAdd.getY());
		return demoAdd.getX() + demoAdd.getY();
	}

	public DemoProperties properties() {
		return this.demoProperties;
	}
}
