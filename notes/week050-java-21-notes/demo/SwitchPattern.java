import java.util.Date;

public class SwitchPattern {
    
    public static void main(String[] args) {
        
        test_switch("adult");
        test_switch("child");

        test_switch_expression("adult");
        test_switch_expression("child");

        test_if_else(123);
        test_if_else(123L);
        test_if_else(123.0);
        test_if_else("123");
        test_if_else(new Date());

        test_switch_pattern(123);
        test_switch_pattern(123L);
        test_switch_pattern(123.0);
        test_switch_pattern("123");
        test_switch_pattern(new Date());
    }

    private static void test_switch(String type) {
        int result = -1;
        switch (type) {
            case "child":
                result = 0;
                break;
            case "adult":
                result = 1;
                break;
            default:
                break;
        }
        System.out.println(result);
    }

    private static void test_switch_expression(String type) {
        int result = switch (type) {
            case "child" -> 0;
            case "adult" -> 1;
            default -> -1;
        };
        System.out.println(result);
    }

    private static void test_if_else(Object obj) {
        String formatted;
        if (obj instanceof Integer i) {
            formatted = String.format("int %d", i);
        } else if (obj instanceof Long l) {
            formatted = String.format("long %d", l);
        } else if (obj instanceof Double d) {
            formatted = String.format("double %f", d);
        } else if (obj instanceof String s) {
            formatted = String.format("string %s", s);
        } else {
            formatted = "unknown";
        }
        System.out.println(formatted);
    }

    private static void test_switch_pattern(Object obj) {
        String formatted = switch (obj) {
            case Integer i -> String.format("int %d", i);
            case Long l    -> String.format("long %d", l);
            case Double d  -> String.format("double %f", d);
            case String s  -> String.format("string %s", s);
            default        -> "unknown";
        };
        System.out.println(formatted);
    }
}
