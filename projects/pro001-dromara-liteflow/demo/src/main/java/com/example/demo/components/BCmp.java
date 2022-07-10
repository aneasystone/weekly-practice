package com.example.demo.components;

import org.springframework.stereotype.Component;

import com.yomahub.liteflow.core.NodeComponent;

@Component("b")
public class BCmp extends NodeComponent {

	@Override
	public void process() {
		System.out.println("Processing B component...");
	}
}
