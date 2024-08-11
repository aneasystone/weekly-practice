import java.util.stream.IntStream;

import jdk.incubator.vector.*;

public class VectorSimpleDemo {

    public static void main(String[] args) {
        testVectorSimple();
        testVectorSimple2();
    }

    private static void testVectorSimple() {
        int[] a = new int[] {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        int[] b = new int[] {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        IntVector aVector = IntVector.fromArray(IntVector.SPECIES_128, a, 0);
        IntVector bVector = IntVector.fromArray(IntVector.SPECIES_128, b, 0);
        IntVector cVector = aVector.add(bVector);
        System.out.println(cVector);
    }

    private static void testVectorSimple2() {
        int[] a = new int[] {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        int[] b = new int[] {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        int[] c = new int[10];
        int lanes = IntVector.SPECIES_128.length();
        int loopBound = IntVector.SPECIES_128.loopBound(a.length);
        for (int i = 0; i < loopBound; i += lanes) {
            IntVector aVector = IntVector.fromArray(IntVector.SPECIES_128, a, i);
            IntVector bVector = IntVector.fromArray(IntVector.SPECIES_128, b, i);
            IntVector cVector = aVector.add(bVector);
            cVector.intoArray(c, i);
        }
        for (int i = loopBound; i < a.length; i++) {
            c[i] = a[i] + b[i];
        }
        IntStream.of(c).forEach(x -> System.out.println(x));
    }

    private static void testVectorSimple3() {
        // int[] a = new int[] {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        // int[] b = new int[] {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        // Int512Vector aVector = Int512Vector.fromArray(IntVector.SPECIES_512, a, 0);
        // Int512Vector bVector = Int512Vector.fromArray(IntVector.SPECIES_512, b, 0);
        // Int512Vector cVector = aVector.add(bVector);
        // System.out.println(cVector);
    }
}
