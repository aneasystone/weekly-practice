public class JNIDemo {
    static {
        System.loadLibrary("JNIDemo");
    }

    public static void main(String[] args) {
        new JNIDemo().sayHello();
    }

    private native void sayHello();
}
