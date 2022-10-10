package com.example.demo;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.LongStream;
import java.util.stream.Stream;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
public class IntermediateOperationTests {
	
	Stream<Student> students;

	@BeforeEach
	void setUp() {
		students = Stream.of(
			Student.builder().name("张三").age(27).number(1L).interests("画画、篮球").build(),
			Student.builder().name("李四").age(29).number(2L).interests("篮球、足球").build(),
			Student.builder().name("王二").age(27).number(3L).interests("唱歌、跳舞、画画").build(),
			Student.builder().name("麻子").age(31).number(4L).interests("篮球、羽毛球").build()
		);
	}

	@Test
	void filterTest() {
		students = students.filter(s -> s.getAge() > 30);
		students.forEach(System.out::println);
	}

	@Test
	void mapTest() {
		Stream<StudentDTO> studentDTOs = students.map(s -> {
			return StudentDTO.builder().name(s.getName()).age(s.getAge()).build();
		});
		studentDTOs.forEach(System.out::println);

		LongStream studentAges = students.mapToLong(s -> s.getAge());
		studentAges.forEach(System.out::println);

		LongStream studentAges2 = students.mapToLong(Student::getAge);
		studentAges2.forEach(System.out::println);
	}

	@Test
	void flatMapTest() {
		Stream<String> studentInterests = students.flatMap(s -> Arrays.stream(s.getInterests().split("、")));
		studentInterests.forEach(System.out::println);
	}

	@Test
	void peekTest() {
		Stream<String> studentNames = students.filter(s -> s.getAge() > 20)
			.peek(System.out::println)
			.map(Student::getName)
			.peek(System.out::println);
		// studentNames.forEach(System.out::println);
		System.out.println(studentNames.findFirst().get());
	}

	@Test
	void unorderedTest() {
		List<Integer> ints = Stream.of(1, 2, 3).unordered()
			.map(x -> x*2)
			.collect(Collectors.toList());
		System.out.println(ints);
	}
}
