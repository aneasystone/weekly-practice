package com.example.demo;

import org.springframework.stereotype.Service;

import com.example.demo.model.DemoAdd;

import lombok.extern.slf4j.Slf4j;

@Slf4j
@Service
public class DemoService {
	
	public Integer add(DemoAdd demoAdd) {
		log.debug("x = {}, y = {}", demoAdd.getX(), demoAdd.getY());
		return demoAdd.getX() + demoAdd.getY();
	}
}
