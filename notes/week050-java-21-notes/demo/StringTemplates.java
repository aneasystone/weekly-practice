public class StringTemplates {
    
    public static void main(String[] args) {
        // test_raw_templates();
        test_str_templates();
        // test_fmt_templates();
    }

    // private static void test_raw_templates() {
    //     String name = "zhangsan";
    //     int age = 18;
    //     String message = RAW."My name is \{name}, I'm \{age} years old.";
    //     System.out.println(message);
    // }

    private static void test_str_templates() {
        String name = "zhangsan";
        int age = 18;
        String message = STR."My name is \{name}, I'm \{age} years old.";
        System.out.println(message);

        int x = 1, y = 2;
        String s1 = STR."\{x} + \{y} = \{x + y}";
        System.out.println(s1);

        String s2 = STR."Java version is \{getVersion()}";
        System.out.println(s2);

        Person p = new Person(name, age);
        String s3 = STR."My name is \{p.name}, I'm \{p.age} years old.";
        System.out.println(s3);

        String s4 = STR."I'm \{age >= 18 ? "an adult" : "a child"}.";
        System.out.println(s4);

        String s5 = STR."I'm \{
            // check the age
            age >= 18 ? "an adult" : "a child"
        }.";
        System.out.println(s5);

        String json1 = "{\n" +
                       "  \"name\": \"zhangsan\",\n" +
                       "  \"age\": 18\n" +
                       "}\n";
        System.out.println(json1);

        String json2 = """
                       {
                         "name": "zhangsan",
                         "age": 18
                       }
                       """;
        System.out.println(json2);
    }

    private static String getVersion() {
        return "21";
    }

    static class Person {
        private String name;
        private int age;
        public Person(String name, int age) {
            this.name = name;
            this.age = age;
        }
    }

    // private static void test_fmt_templates() {
    //     String name = "zhangsan";
    //     int age = 18;
    //     String message = FMT."My name is %-12s\{name}, I'm %d\{age} years old.";
    //     System.out.println(message);
    // }
}
