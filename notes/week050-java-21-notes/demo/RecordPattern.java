record Point(int x, int y) {
    boolean isOrigin() {
        return x == 0 && y == 0;
    }
}

record Address(String province, String city) {}
record Person(String name, Integer age, Address address) {}

public class RecordPattern {

    public static void main(String[] args) {
        test_records();
        test_instanceof_pattern_matching(100);
        test_record_pattern(new Point(10, 20));
        test_record_pattern_nested(new Person("Zhangsan", 18, new Address("Anhui", "Hefei")));
        test_record_pattern_nested(new Person("Lisi", 20, null));
    }

    private static void test_records() {
        Point p1 = new Point(10, 20);
        System.out.println("x = " + p1.x());
        System.out.println("y = " + p1.y());
        System.out.println("p1 is " + p1.toString());
        Point p2 = new Point(10, 20);
        System.out.println("p2 is " + p2);
        System.out.println("p1 " + (p1.equals(p2) ? "==" : "!=") + " p2");
        System.out.println(p1.isOrigin());
    }

    private static void test_instanceof_pattern_matching(Object obj) {
        if (obj instanceof Integer) {
            int intValue = ((Integer) obj).intValue();
            System.out.println(intValue);
        }
        if (obj instanceof Integer intValue) {
            System.out.println(intValue);
        }
    }

    private static void test_record_pattern(Object obj) {
        if (obj instanceof Point p) {
            int x = p.x();
            int y = p.y();
            System.out.println(x + y);
        }
        if (obj instanceof Point(int x, int y)) {
            System.out.println(x + y);
        }
    }

    private static void test_record_pattern_nested(Object obj) {
        if (obj instanceof Person(String name, Integer age, Address address)) {
            System.out.println("Name: " + name);
            System.out.println("Age: " + age);
        }
        if (obj instanceof Person(String name, Integer age, Address(String province, String city))) {
            System.out.println("Name: " + name);
            System.out.println("Age: " + age);
            System.out.println("Address: " + province + " " + city);
        }
    }
}
