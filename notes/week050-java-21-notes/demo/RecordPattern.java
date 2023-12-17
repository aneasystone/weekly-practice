record Point(int x, int y) {
    boolean isOrigin() {
        return x == 0 && y == 0;
    }
}

public class RecordPattern {

    public static void main(String[] args) {
        test_records();
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
}
