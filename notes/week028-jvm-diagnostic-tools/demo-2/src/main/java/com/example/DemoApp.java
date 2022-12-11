package com.example;

import java.util.ArrayList;
import java.util.List;

public class DemoApp {
    public static void main(String[] args) throws Exception {
        List<Person> personList = new ArrayList<Person>();
        for (int i = 0; ; i++) {
            Person person = new Person();
            person.setAge(i);
            person.setName("zhangsan-" + i);
            personList.add(person);
            Thread.sleep(100);
        }
    }

    public static class Person {

        private String name;
        private int age;

        public String getName() {
            return name;
        }
        public void setName(String name) {
            this.name = name;
        }
        public int getAge() {
            return age;
        }
        public void setAge(int age) {
            this.age = age;
        }
    }
}
