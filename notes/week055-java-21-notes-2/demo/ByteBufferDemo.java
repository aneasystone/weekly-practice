import java.lang.reflect.Field;
import java.nio.ByteBuffer;
import sun.misc.Unsafe;

public class ByteBufferDemo {
    
    public static void main(String[] args) throws Exception {
        
        testDirect();
        testUnsafe();
        
    }

    private static void testDirect() {
        ByteBuffer bb = ByteBuffer.allocateDirect(10);
        bb.putInt(0);
        bb.putInt(1);
        bb.put((byte)0);
        bb.put((byte)1);
        // bb.put((byte)1);

        bb.flip();

        System.out.println(bb.getInt());
        System.out.println(bb.getInt());
        System.out.println(bb.get());
        System.out.println(bb.get());
    }

    private static void testUnsafe() throws Exception {
        Field f = Unsafe.class.getDeclaredField("theUnsafe");
        f.setAccessible(true);
        Unsafe unsafe = (Unsafe) f.get(null);
        // Unsafe unsafe = Unsafe.getUnsafe();
        
        long address = unsafe.allocateMemory(10);
        unsafe.putInt(address, 0);
        unsafe.putInt(address+4, 1);
        unsafe.putByte(address+8, (byte)0);
        unsafe.putByte(address+9, (byte)1);
        System.out.println(unsafe.getInt(address));
        System.out.println(unsafe.getInt(address+4));
        System.out.println(unsafe.getByte(address+8));
        System.out.println(unsafe.getByte(address+9));
        unsafe.freeMemory(address);
    }
}
