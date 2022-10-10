package com.example.demo;

import java.util.Arrays;
import java.util.Comparator;
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
			Student.builder().name("张三").age(27).number(3L).interests("画画、篮球").build(),
			Student.builder().name("李四").age(29).number(2L).interests("篮球、足球").build(),
			Student.builder().name("王二").age(27).number(1L).interests("唱歌、跳舞、画画").build(),
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
	}

	@Test
	void mapToLongTest() {
		LongStream studentAges = students.mapToLong(s -> s.getAge());
		studentAges.forEach(System.out::println);
	}

	@Test
	void mapToLongTest2() {
		LongStream studentAges = students.mapToLong(Student::getAge);
		studentAges.forEach(System.out::println);
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

	@Test
	void distinctTest() {
		Stream<Integer> intStream = Stream.of(1, 2, 3, 2, 4, 3, 1, 2);
		intStream = intStream.distinct();
		intStream.forEach(System.out::println);
	}

	@Test
	void sortedTest() {
		Stream<Integer> intStream = Stream.of(1, 3, 2, 4);
		intStream = intStream.sorted();
		intStream.forEach(System.out::println);
	}

	@Test
	void sortComparatorTest() {

		students = students.sorted(new Comparator<Student>() {

			@Override
			public int compare(Student o1, Student o2) {
				return o1.getAge().compareTo(o2.getAge());
			}
			
		});
		students.forEach(System.out::println);
	}

	@Test
	void sortComparatorTest2() {
		students = students.sorted((o1, o2) -> o1.getAge().compareTo(o2.getAge()));
		students.forEach(System.out::println);
	}

	@Test
	void sortComparatorTest3() {
		// students = students.sorted(Comparator.comparing(Student::getAge));
		students = students.sorted(
			Comparator.comparing(Student::getAge).thenComparing(Student::getNumber)
		);
		students.forEach(System.out::println);
	}

	@Test
	void skipLimitTest() {
		Stream<Integer> intStream = Stream.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
		intStream = intStream.skip(3).limit(3);
		intStream.forEach(System.out::println);
	}

	@Test
	void dropTakeTest() {
		Stream<Integer> intStream = Stream.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
		intStream = intStream.dropWhile(x -> x <= 3).takeWhile(x -> x <= 6);
		intStream.forEach(System.out::println);
	}
}
