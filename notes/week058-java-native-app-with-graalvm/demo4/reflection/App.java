public class App {
    
    public static void main( String[] args ) throws Exception {
        if (args.length != 4) {
            System.out.println("Usage: ./app clz method a b");
            return;
        }
        Integer result = callReflection(args[0], args[1], Integer.parseInt(args[2]), Integer.parseInt(args[3]));
        System.out.println(result);
    }

    public static Integer callReflection(String clz, String method, Integer a, Integer b) throws Exception {
        Class<?> clazz = Class.forName(clz);
        return (Integer) clazz.getMethod(method, Integer.class, Integer.class).invoke(null, a, b);
    }
}
