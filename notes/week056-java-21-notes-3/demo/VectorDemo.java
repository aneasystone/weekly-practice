import jdk.incubator.vector.*;
import java.util.stream.IntStream;

public class VectorDemo {
    
    static final VectorSpecies<Integer> SPECIES = IntVector.SPECIES_PREFERRED;

    public static void main(String[] args) {
        int[] a = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        int[] b = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        int[] c;

        c = new int[10];
        testScalar(a, b, c);

        c = new int[10];
        testVector(a, b, c);

        testScalarSimple();
        testScalarSimple2();
        testVectorSimple();
    }

    private static void testScalar(int[] a, int[] b, int[] c) {
        for (int i = 0; i < a.length; i++) {
            c[i] = a[i] * a[i] + b[i] * b[i];
        }
        IntStream.of(c).forEach(x -> System.out.println(x));
    }

    private static void testVector(int[] a, int[] b, int[] c) {
        int upperBound = SPECIES.loopBound(a.length);
        System.out.println(upperBound);
        int i = 0;
        for (; i < upperBound; i += SPECIES.length()) {
            var va = IntVector.fromArray(SPECIES, a, i);
            var vb = IntVector.fromArray(SPECIES, b, i);
            var vc = va.mul(va).add(vb.mul(vb));
            vc.intoArray(c, i);
        }
        for (; i < a.length; i++) {
            c[i] = a[i] * a[i] + b[i] * b[i];
        }
        IntStream.of(c).forEach(x -> System.out.println(x));
    }

    private static void testScalarSimple() {
        int[] a = new int[] {1, 2, 3, 4};
        int[] b = new int[] {1, 2, 3, 4};
        int[] c = new int[4];
        for (int i = 0; i < a.length; i++) {
            c[i] = a[i] + b[i];
        }
        IntStream.of(c).forEach(x -> System.out.println(x));
    }

    private static void testScalarSimple2() {
        int[] a = new int[] {1, 2, 3, 4};
        int[] b = new int[] {1, 2, 3, 4};
        int[] c = new int[4];
        IntStream.range(0, a.length)
            .parallel()
            .forEach(i -> c[i] = a[i] + b[i]);
        IntStream.of(c).forEach(x -> System.out.println(x));
    }

    private static void testVectorSimple() {
        // 数据类型      字节数
        // byte         1
        // boolean      1
        // short        2
        // char         2
        // int          4
        // float        4
        // long         8
        // double       8
        int[] a = new int[] {1, 2, 3, 4};
        int[] b = new int[] {1, 2, 3, 4};
        // 4 bytes * 4 = 32 bits * 4 = 128
        IntVector aVector = IntVector.fromArray(IntVector.SPECIES_128, a, 0);
        IntVector bVector = IntVector.fromArray(IntVector.SPECIES_128, b, 0);
        IntVector cVector = aVector.add(bVector);
        System.out.println(cVector);
    }
}
