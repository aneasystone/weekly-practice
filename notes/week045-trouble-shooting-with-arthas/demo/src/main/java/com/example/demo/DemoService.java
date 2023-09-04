package com.example.demo;

import org.springframework.stereotype.Service;

import com.example.demo.model.DemoAdd;

@Service
public class DemoService {
	
	public Integer add(DemoAdd demoAdd) {
		return demoAdd.getX() + demoAdd.getY();
	}
}
