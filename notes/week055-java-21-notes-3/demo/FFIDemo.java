import java.lang.foreign.Arena;
import java.lang.foreign.FunctionDescriptor;
import java.lang.foreign.Linker;
import java.lang.foreign.MemorySegment;
import java.lang.foreign.SymbolLookup;
import java.lang.foreign.ValueLayout;
import java.lang.invoke.MethodHandle;

public class FFIDemo {
    public static void main(String[] args) throws Throwable {
        Linker linker = Linker.nativeLinker();
        SymbolLookup symbolLookup = linker.defaultLookup();
        MethodHandle printf = linker.downcallHandle(
            symbolLookup.find("printf").orElseThrow(), 
            FunctionDescriptor.of(ValueLayout.JAVA_LONG, ValueLayout.ADDRESS)
        );
        try (Arena arena = Arena.ofConfined()) {
            MemorySegment hello = arena.allocateUtf8String("Hello World!\n");
            printf.invoke(hello);
        }
    }
}
