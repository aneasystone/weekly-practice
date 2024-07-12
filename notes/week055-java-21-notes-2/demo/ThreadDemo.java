import java.lang.management.ManagementFactory;
import java.lang.management.ThreadInfo;
import java.lang.management.ThreadMXBean;
import java.time.Duration;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;
import java.util.stream.IntStream;

public class ThreadDemo {
    
    public static void main(String[] args) {
        monitorThread();
        // testThread();
        // testThreadPool();
        testVirtualThread();
    }

    private static void monitorThread() {
        ScheduledExecutorService scheduledExecutorService = Executors.newScheduledThreadPool(1);
        scheduledExecutorService.scheduleAtFixedRate(() -> {
            ThreadMXBean threadBean = ManagementFactory.getThreadMXBean();
            ThreadInfo[] threadInfo = threadBean.dumpAllThreads(false, false);
            System.out.println(threadInfo.length + " os thread");
        }, 1, 1, TimeUnit.SECONDS);
    }

    private static void testThread() {
        long l = System.currentTimeMillis();
        try(var executor = Executors.newCachedThreadPool()) {
            IntStream.range(0, 100000).forEach(i -> {
                executor.submit(() -> {
                    Thread.sleep(Duration.ofSeconds(1));
                    // System.out.println(i);
                    return i;
                });
            });
        }
        System.out.printf("elapsed time：%d ms", System.currentTimeMillis() - l);
    }

    private static void testThreadPool() {
        long l = System.currentTimeMillis();
        try(var executor = Executors.newFixedThreadPool(2000)) {
            IntStream.range(0, 100000).forEach(i -> {
                executor.submit(() -> {
                    Thread.sleep(Duration.ofSeconds(1));
                    // System.out.println(i);
                    return i;
                });
            });
        }
        System.out.printf("elapsed time：%d ms", System.currentTimeMillis() - l);
    }

    private static void testVirtualThread() {
        long l = System.currentTimeMillis();
        try(var executor = Executors.newVirtualThreadPerTaskExecutor()) {
            IntStream.range(0, 100000).forEach(i -> {
                executor.submit(() -> {
                    Thread.sleep(Duration.ofSeconds(1));
                    // System.out.println(i);
                    return i;
                });
            });
        }
        System.out.printf("elapsed time：%d ms", System.currentTimeMillis() - l);
    }
}
