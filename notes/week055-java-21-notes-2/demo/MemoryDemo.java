import java.lang.foreign.Arena;
import java.lang.foreign.MemorySegment;
import java.lang.foreign.ValueLayout;

public class MemoryDemo {
    
    public static void main(String[] args) {
        
        testAllocate();
        testAllocateString();
        testAllocateArray();
    }

    private static void testAllocate() {
        try (Arena offHeap = Arena.ofConfined()) {
            MemorySegment address = offHeap.allocate(8);
            address.setAtIndex(ValueLayout.JAVA_INT, 0, 1);
            address.setAtIndex(ValueLayout.JAVA_INT, 1, 0);
            System.out.println(address.getAtIndex(ValueLayout.JAVA_INT, 0));
            System.out.println(address.getAtIndex(ValueLayout.JAVA_INT, 1));
        }
    }

    private static void testAllocateString() {
        try (Arena offHeap = Arena.ofConfined()) {
            // MemorySegment str = offHeap.allocateFrom("hello");
            // System.out.println(str.getString(0));
            MemorySegment str = offHeap.allocateUtf8String("hello");
            System.out.println(str.getUtf8String(0));
        }
    }

    private static void testAllocateArray() {
        // try (Arena offHeap = Arena.ofConfined()) {
        //     MemorySegment pointers = offHeap.allocateArray(ValueLayout.ADDRESS, 2);
        //     pointers.setAtIndex(AddressLayout.ADDRESS, 0, offHeap.allocateUtf8String("hello"));
        //     pointers.setAtIndex(AddressLayout.ADDRESS, 1, offHeap.allocateUtf8String("world"));
        //     System.out.println(pointers.getAtIndex(AddressLayout.ADDRESS, 0).getUtf8String(0));
        //     System.out.println(pointers.getAtIndex(AddressLayout.ADDRESS, 1).getUtf8String(0));
        // }
        String[] javaStrings = { "mouse", "cat", "dog", "car" };
        try (Arena offHeap = Arena.ofConfined()) {
            MemorySegment pointers = offHeap.allocateArray(ValueLayout.ADDRESS, javaStrings.length);
            for (int i = 0; i < javaStrings.length; i++) {
                MemorySegment cString = offHeap.allocateUtf8String(javaStrings[i]);
                pointers.setAtIndex(ValueLayout.ADDRESS, i, cString);
            }   
            for (int i = 0; i < javaStrings.length; i++) {
                MemorySegment cString = pointers.getAtIndex(ValueLayout.ADDRESS, i);
                javaStrings[i] = cString.getUtf8String(0);
            }
        }
        System.out.println(javaStrings);
    }
}
