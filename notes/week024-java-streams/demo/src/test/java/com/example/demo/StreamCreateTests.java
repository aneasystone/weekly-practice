package com.example.demo;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.Arrays;
import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;
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
}
