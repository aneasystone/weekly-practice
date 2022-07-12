package com.example.demo;

import javax.annotation.Resource;

import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import com.yomahub.liteflow.core.FlowExecutor;
import com.yomahub.liteflow.flow.LiteflowResponse;

@Component
public class DemoRunner implements CommandLineRunner {

	@Resource
    private FlowExecutor flowExecutor;
	
	@Override
	public void run(String... args) throws Exception {
		for (int i = 0; i < 10; i++) {
			LiteflowResponse response = flowExecutor.execute2Resp("chain1", "param");
			System.out.println(String.format("RequestId = %s\r\nExecutorStepStr = %s\r\nMessage = %s\r\nisSuccess = %s", 
				response.getRequestId(),
				response.getExecuteStepStr(),
				response.getMessage(),
				response.isSuccess()));
			Thread.sleep(10_000);
		}
	}
}
