package com.example.demo;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.Optional;
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
			Student.builder().name("张三").age(27).number(3L).interests("画画、篮球").build(),
			Student.builder().name("李四").age(29).number(2L).interests("篮球、足球").build(),
			Student.builder().name("王二").age(27).number(1L).interests("唱歌、跳舞、画画").build(),
			Student.builder().name("麻子").age(31).number(4L).interests("篮球、羽毛球").build()
		);
	}

	@Test
	void anyMatchTest() {
		boolean hasAgeGreaterThan30 = students.anyMatch(s -> s.getAge() > 30);
		assertTrue(hasAgeGreaterThan30);
	}

	@Test
	void allMatchTest() {
		boolean allAgeGreaterThan20 = students.allMatch(s -> s.getAge() > 20);
		assertTrue(allAgeGreaterThan20);
	}

	@Test
	void noneMatchTest() {
		boolean noAgeGreaterThan40 = students.noneMatch(s -> s.getAge() > 40);
		assertTrue(noAgeGreaterThan40);
	}

	@Test
	void findFirstTest() {
		Optional<Student> student = students.filter(s -> s.getAge() > 28).findFirst();
		assertTrue(student.isPresent());
		assertEquals(student.get().getName(), "李四");
	}

	@Test
	void findAnyTest() {
		Optional<Student> student = students.filter(s -> s.getAge() > 28).findAny();
		assertTrue(student.isPresent());
		assertEquals(student.get().getName(), "李四");
	}

	@Test
	void findAnyTest2() {
		Optional<Student> student = students.parallel().filter(s -> s.getAge() > 28).findAny();
		assertTrue(student.isPresent());
		// assertEquals(student.get().getName(), "李四");
	}
}
