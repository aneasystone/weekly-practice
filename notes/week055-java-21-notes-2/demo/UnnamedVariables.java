import java.util.Arrays;
import java.util.List;

public class UnnamedVariables {

    record Person(String name, Integer age) {
    }

    public static void main(String[] args) {
        test_unnamed_variables();
        test_unnamed_exception_variables("xx");
        test_unnamed_exception_variables("123");
        test_unnamed_patterns(new Person("Zhangsan", 18));
    }

    private static void test_unnamed_exception_variables(String s) {
        try { 
            int i = Integer.parseInt(s);
            System.out.println("Good number: " + i);
        } catch (NumberFormatException _) { 
            System.out.println("Bad number: " + s);
        }
    }

    private static void test_unnamed_variables() {
        int index = 0;
        List<Integer> list = Arrays.asList(1,2,3,4,5);
        for (Integer _ : list) {
            System.out.println(index++);
        }
    }

    private static void test_unnamed_patterns(Object obj) {
        // unnamed patterns
        if (obj instanceof Person(String name, _)) {
            System.out.println("Name: " + name);
        }

        // unnamed pattern variables
        if (obj instanceof Person(String name, Integer _)) {
            System.out.println("Name: " + name);
        }
    }
}
