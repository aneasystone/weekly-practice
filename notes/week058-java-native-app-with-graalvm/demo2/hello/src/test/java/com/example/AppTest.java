package com.example;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.*;

public class AppTest
{
    @Test
    public void testApp()
    {
        assertEquals( "hello".length(), 5 );
    }
}
