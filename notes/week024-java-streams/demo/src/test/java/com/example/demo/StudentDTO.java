package com.example.demo;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class StudentDTO {
	private String name;
	private Integer age;
}
