package com.example.demo;

import com.fasterxml.jackson.annotation.JsonProperty;

public class Greeting {
	
	private long id;

	@JsonProperty(value = "content")
	private String greeting;

	public long getId() {
		return id;
	}
	public void setId(long id) {
		this.id = id;
	}
	public String getGreeting() {
		return greeting;
	}
	public void setGreeting(String greeting) {
		this.greeting = greeting;
	}

	@Override
	public String toString() {
		return "Greeting [greeting=" + greeting + ", id=" + id + "]";
	}
}
