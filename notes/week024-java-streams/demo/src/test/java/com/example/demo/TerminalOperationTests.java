package com.example.demo;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.IntSummaryStatistics;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.OptionalDouble;
import java.util.OptionalInt;
import java.util.Set;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.Function;
import java.util.stream.Collectors;
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
			Student.builder().name("张三").gender("男").age(27).number(3L).interests("画画、篮球").build(),
			Student.builder().name("李四").gender("男").age(29).number(2L).interests("篮球、足球").build(),
			Student.builder().name("王二").gender("女").age(27).number(1L).interests("唱歌、跳舞、画画").build(),
			Student.builder().name("麻子").gender("女").age(31).number(4L).interests("篮球、羽毛球").build()
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

	@Test
	void forEachTest() {
		Stream<Integer> intStream = Stream.of(1, 3, 2, 4);
		// intStream.forEach(System.out::println);
		intStream.parallel().forEach(System.out::println);
	}

	@Test
	void forEachOrderedTest() {
		Stream<Integer> intStream = Stream.of(1, 3, 2, 4);
		// intStream.forEachOrdered(System.out::println);
		intStream.parallel().forEachOrdered(System.out::println);
	}

	@Test
	void toArrayTest() {
		Object[] array = students.toArray();
		for (Object o : array) {
			System.out.println(((Student)o).getName());
		}
	}

	@Test
	void toArrayTest2() {
		// Student[] array = students.toArray(x -> new Student[4]);
		Student[] array = students.toArray(Student[]::new);
		for (Student o : array) {
			System.out.println(o.getName());
		}
	}

	@Test
	void reduceTest() {
		
		// sum
		// Optional<Integer> result = students.map(Student::getAge).reduce((x, y) -> x + y);
        Optional<Integer> result = students.map(Student::getAge).reduce(Integer::sum);
		System.out.println(result.get());
	}

	@Test
	void reduceTest2() {

		// min
		// Optional<Integer> result = students.map(Student::getAge).reduce((x, y) -> x < y ? x : y);
        Optional<Integer> result = students.map(Student::getAge).reduce(Integer::min);
		System.out.println(result.get());
	}

	@Test
	void reduceTest3() {

		// max
		// Optional<Integer> result = students.map(Student::getAge).reduce((x, y) -> x > y ? x : y);
        Optional<Integer> result = students.map(Student::getAge).reduce(Integer::max);
		System.out.println(result.get());
	}

	@Test
	void reduceTest4() {

		// 求和
		Stream<Integer> intStream = Stream.of(1, 3, 2, 4, 2, 4, 2);
		Optional<Integer> result = intStream.reduce((x, y) -> x + y);
		System.out.println(result.get());

		// 带初始值求和
		Stream<Integer> intStream2 = Stream.of(1, 3, 2, 4, 2, 4, 2);
		Integer result2 = intStream2.reduce(100, (x, y) -> x + y);
		System.out.println(result2);

		// 统计元素个数
		Stream<Integer> intStream3 = Stream.of(1, 3, 2, 4, 2, 4, 2);
		Map<Integer, Integer> countMap = intStream3.reduce(new HashMap<>(), (x, y) -> {
			if (x.containsKey(y)) {
				x.put(y, x.get(y) + 1);
			} else {
				x.put(y, 1);
			}
			return x;
		}, (x, y) -> new HashMap<>());
		System.out.println(countMap);

		// 数组去重
		Stream<Integer> intStream4 = Stream.of(1, 3, 2, 4, 2, 4, 2);
		List<Integer> distinctMap = intStream4.reduce(new ArrayList<>(), (x, y) -> {
			if (!x.contains(y)) {
				x.add(y);
			}
			return x;
		}, (x, y) -> new ArrayList<>());
		System.out.println(distinctMap);
	}

	@Test
	void reduceTest5() {
		
		// 属性求和
		Integer totalAge = students.reduce(0, (x, y) -> x + y.getAge(), (x, y) -> 0);
		System.out.println(totalAge);
	}

	@Test
	void reduceTest6() {

		// list to map
		// Map<Long, Student> studentMap = students.reduce(new HashMap<Long, Student>(), (x, y) -> {
		// 	x.put(y.getNumber(), y);
		// 	return x;
		// }, (x, y) -> new HashMap<Long, Student>());
		// System.out.println(studentMap);

        Map<Long, Student> studentMap = students.parallel().reduce(new HashMap<Long, Student>(), (x, y) -> {
			x.put(y.getNumber(), y);
			return x;
		}, (x, y) -> {
            for (Map.Entry<Long, Student> entry : y.entrySet()) {
                x.put(entry.getKey(), entry.getValue());
            }
            return x;
        });
		System.out.println(studentMap);
	}

    @Test
	void reduceTest7() {

        // 并行流求和
        Stream<Integer> intStream = Stream.iterate(1, n -> n + 1).limit(100);
        Optional<Integer> result = intStream.reduce(Integer::sum);
        System.out.println(result.get());

        Stream<Integer> intStream2 = Stream.iterate(1, n -> n + 1).limit(100);
        Optional<Integer> result2 = intStream2.parallel().reduce(Integer::sum);
        System.out.println(result2.get());

        Stream<Integer> intStream3 = Stream.iterate(1, n -> n + 1).limit(100);
        Integer result3 = intStream3.parallel().reduce(0, Integer::sum);
        System.out.println(result3);

        Stream<Integer> intStream4 = Stream.iterate(1, n -> n + 1).limit(100);
        Integer result4 = intStream4.parallel().reduce(0, Integer::sum, Integer::sum);
        System.out.println(result4);
    }

    @Test
	void collectTest() {
		Stream<Integer> intStream = Stream.of(1, 3, 2, 4);
		AtomicInteger result = intStream.collect(
            () -> new AtomicInteger(),
            (a, b) -> a.addAndGet(b), 
            (a, b) -> {}
        );
        System.out.println(result);

        // Stream<Integer> intStream = Stream.of(1, 3, 2, 4);
		// AtomicInteger result = intStream.collect(
        //     AtomicInteger::new,
        //     AtomicInteger::addAndGet, 
        //     (a, b) -> {}
        // );
        // System.out.println(result);
	}

    @Test
	void collectTest2() {
        Stream<Integer> intStream = Stream.of(1, 3, 2, 4, 3, 2, 1);
		List<Integer> result = intStream.collect(Collectors.toList());
		System.out.println(result);
	}

    @Test
	void collectTest3() {
        Stream<Integer> intStream = Stream.of(1, 3, 2, 4, 3, 2, 1);
		Set<Integer> result = intStream.collect(Collectors.toSet());
		System.out.println(result);
	}

    @Test
	void collectTest4() {
        Stream<Integer> intStream = Stream.of(1, 3, 2, 4, 3, 2, 1);
		List<Integer> result = intStream.collect(Collectors.toCollection(ArrayList::new));
		System.out.println(result);
	}

    @Test
	void collectTest5() {
        Stream<Integer> intStream = Stream.of(1, 3, 2, 4, 3, 2, 1);
		Integer result = intStream.collect(Collectors.summingInt(Integer::valueOf));
		System.out.println(result);
	}

    @Test
	void collectTest6() {
        Stream<Integer> intStream = Stream.of(1, 3, 2, 4, 3, 2, 1);
		Optional<Integer> result = intStream.collect(Collectors.maxBy(Integer::compareTo));
		System.out.println(result);
	}

    @Test
	void collectTest7() {
		Map<Long, Student> result = students.collect(Collectors.toMap(Student::getNumber, Function.identity()));
		System.out.println(result);
	}

    @Test
	void collectTest8() {
        Stream<Integer> intStream = Stream.of(1, 3, 2, 4, 3, 2, 1);
        Map<Integer, Integer> result = intStream.collect(Collectors.toMap(i -> i, i -> i, (i, j) -> i));
		System.out.println(result.values());
	}

    @Test
	void collectTest9() {
        Stream<Integer> intStream = Stream.of(1, 3, 2, 4, 3, 2, 1);
        Map<Integer, Long> result = intStream.collect(Collectors.groupingBy(i -> i, Collectors.counting()));
		System.out.println(result);
	}

    @Test
	void collectTest10() {
        String result = students.map(Student::getName).collect(Collectors.joining("、"));
		System.out.println(result);
	}

    @Test
	void collectTest11() {
        Map<Integer, List<Student>> result = students.collect(Collectors.groupingBy(Student::getAge));
		System.out.println(result);
	}

    @Test
	void collectTest12() {
        Map<Boolean, List<Student>> result = students.collect(Collectors.partitioningBy(x -> x.getAge() > 30));
		System.out.println(result);
	}

    @Test
	void collectTest13() {
        Map<String, List<String>> result = students.collect(Collectors.groupingBy(
            Student::getGender, Collectors.mapping(
                Student::getName, Collectors.toList())));
		System.out.println(result);
	}

    @Test
	void collectTest14() {
        Map<String, Integer> result = students.collect(Collectors.groupingBy(
            Student::getGender, Collectors.reducing(
                0, Student::getAge, Integer::sum)));
        // Map<String, Integer> result = students.collect(Collectors.groupingBy(
        //     Student::getGender, Collectors.summingInt(Student::getAge)));
		System.out.println(result);
	}

	@Test
	void minTest() {
		OptionalInt minAge = students.mapToInt(Student::getAge).min();
		System.out.println(minAge.getAsInt());
	}

	@Test
	void maxTest() {
		// OptionalInt maxAge = students.mapToInt(Student::getAge).max();
		// System.out.println(maxAge.getAsInt());

        Optional<Student> maxAgeStudent = students.max(Comparator.comparingInt(Student::getAge));
        System.out.println(maxAgeStudent.get().getAge());
	}

	@Test
	void sumTest() {
		int sumAge = students.mapToInt(Student::getAge).sum();
		System.out.println(sumAge);
	}

    @Test
	void averageTest() {
		OptionalDouble averageAge = students.mapToInt(Student::getAge).average();
		System.out.println(averageAge);
	}

    @Test
	void summaryStatisticsTest() {
		IntSummaryStatistics summaryStatistics = students.mapToInt(Student::getAge).summaryStatistics();
        System.out.println("Max = " + summaryStatistics.getMax());
        System.out.println("Min = " + summaryStatistics.getMin());
        System.out.println("Sum = " + summaryStatistics.getSum());
        System.out.println("Count = " + summaryStatistics.getCount());
		System.out.println("Average = " + summaryStatistics.getAverage());
	}

    @Test
	void countTest() {
		long count = students.count();
		System.out.println(count);
	}
}
