package hello;

import static org.hamcrest.CoreMatchers.containsString;
import static org.junit.Assert.*;

import org.junit.Test;

public class HelloWorldTest {
  
    private HelloWorld hello = new HelloWorld();

    @Test
    public void sayTest() {
        assertThat(hello.say(), containsString("Hello"));
    }
}