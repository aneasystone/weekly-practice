package com.example.demo;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.Arrays;
import java.util.List;
import java.util.Random;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.DoubleStream;
import java.util.stream.IntStream;
import java.util.stream.LongStream;
import java.util.stream.Stream;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class StreamCreateTests {

	@Test
	void createEmptyStream() {
		Stream<String> streamEmpty = Stream.empty();
		assertEquals(streamEmpty.count(), 0);
	}

	@Test
	void createStreamFromCollection() {
		List<String> collection = Arrays.asList("a", "b", "c");
		Stream<String> streamOfCollection = collection.stream();
		assertEquals(streamOfCollection.count(), 3);
	}

	@Test
	void createStreamFromArray() {
		String[] array = new String[]{"a", "b", "c"};
		Stream<String> streamOfArray = Arrays.stream(array);
		assertEquals(streamOfArray.count(), 3);

		Stream<String> streamOfArray2 = Stream.of(array);
		assertEquals(streamOfArray2.count(), 3);

		Stream<String> streamOfArray3 = Stream.of("a", "b", "c");
		assertEquals(streamOfArray3.count(), 3);
	}

	@Test
	void createStreamFromBuilder() {
		Stream<String> streamOfBuilder = Stream.<String>builder()
			.add("a")
			.add("b")
			.add("c")
			.build();
		assertEquals(streamOfBuilder.count(), 3);

		Stream.Builder<String> builder = Stream.<String>builder();
		builder.add("a");
		builder.add("b");
		builder.add("c");
		Stream<String> streamOfBuilder2 = builder.build();
		assertEquals(streamOfBuilder2.count(), 3);
	}

	@Test
	void createStreamFromGenerate() {
		Stream<String> streamOfGenerate = Stream.generate(() -> "hello").limit(3);
		assertEquals(streamOfGenerate.count(), 3);

		AtomicInteger num = new AtomicInteger(0);
		Stream<Integer> streamOfGenerate2 = Stream.generate(() -> num.incrementAndGet()).limit(3);
		streamOfGenerate2.forEach(System.out::println);
	}

	@Test
	void createStreamFromIterate() {
		Stream<Integer> streamOfIterate = Stream.iterate(1, n -> n + 1).limit(3);
		// assertEquals(streamOfIterate.count(), 3);
		streamOfIterate.forEach(System.out::println);
	}

	@Test
	void createStreamFromPrimitives() {
		IntStream intStream = IntStream.range(1, 4);
		assertEquals(intStream.count(), 3);		

		IntStream intStream2 = IntStream.rangeClosed(1, 3);
		assertEquals(intStream2.count(), 3);
	}

	@Test
	void createStreamFromRandom() {
		IntStream intStream = new Random().ints(3);
		intStream.forEach(System.out::println);

		LongStream longStream = new Random().longs(3);
		longStream.forEach(System.out::println);

		DoubleStream doubleStream = new Random().doubles(3);
		doubleStream.forEach(System.out::println);
	}
}
