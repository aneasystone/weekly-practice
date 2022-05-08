package com.example.demo.service.mapper;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class FooMapperTest {

    private FooMapper fooMapper;

    @BeforeEach
    public void setUp() {
        fooMapper = new FooMapperImpl();
    }
}
