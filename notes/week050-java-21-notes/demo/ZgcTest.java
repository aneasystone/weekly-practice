public class ZgcTest {

    private byte[] bytes = new byte[1024 * 1024]; // 1MB

    public static void main(String[] args) {
        ZgcTest zgcTest = new ZgcTest();
        zgcTest = null;
        System.gc();
    }
}
