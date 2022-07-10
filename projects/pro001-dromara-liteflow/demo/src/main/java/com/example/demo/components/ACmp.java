package com.example.demo.components;

import org.springframework.stereotype.Component;

import com.yomahub.liteflow.core.NodeComponent;

@Component("a")
public class ACmp extends NodeComponent {

	@Override
	public void process() {
		System.out.println("Processing A component...");
	}
}
