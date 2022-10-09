package com.example.demo;

import java.util.stream.Stream;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
public class TerminalOperationTests {
	
	Stream<Student> students;

	@BeforeEach
	void setUp() {
		students = Stream.of(
			Student.builder().name("Zhangsan").age(27).number(1L).build(),
			Student.builder().name("Lisi").age(29).number(2L).build(),
			Student.builder().name("Wanger").age(27).number(3L).build(),
			Student.builder().name("Mazi").age(31).number(4L).build()
		);
	}

	@Test
	void filterTest() {
		students.filter(s -> s.getAge() > 30)
			.forEach(System.out::println);
	}
}
