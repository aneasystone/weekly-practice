package com.example.demo.domain;

import static org.assertj.core.api.Assertions.assertThat;

import com.example.demo.web.rest.TestUtil;
import org.junit.jupiter.api.Test;

class FooTest {

    @Test
    void equalsVerifier() throws Exception {
        TestUtil.equalsVerifier(Foo.class);
        Foo foo1 = new Foo();
        foo1.setId(1L);
        Foo foo2 = new Foo();
        foo2.setId(foo1.getId());
        assertThat(foo1).isEqualTo(foo2);
        foo2.setId(2L);
        assertThat(foo1).isNotEqualTo(foo2);
        foo1.setId(null);
        assertThat(foo1).isNotEqualTo(foo2);
    }
}
