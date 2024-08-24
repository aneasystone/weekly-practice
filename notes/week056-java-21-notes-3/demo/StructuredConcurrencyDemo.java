import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.FutureTask;
import java.util.concurrent.StructuredTaskScope;
import java.util.concurrent.StructuredTaskScope.Subtask;

public class StructuredConcurrencyDemo {
    public static void main(String[] args) throws Exception {
        // testThread();
        // testTask();
        // testExecutorService();
        // testStructuredTaskScope();
        // testStructuredTaskScopeShutdownOnFailure();
        testStructuredTaskScopeShutdownOnSuccess();
    }

    private static void testThread() throws Exception {
        System.out.println("main thread start");
        Thread t1 = new Thread(() -> thread1(0));
        Thread t2 = new Thread(() -> thread2(1));
        t1.start();
        t2.start();
        t1.join();
        t2.join();
        System.out.println("main thread end");
    }

    private static void thread1(int code) {
        System.out.println("thread1 start");
        if (code != 0) {
            throw new RuntimeException("code is illegal");
        }
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println("thread1 end");
    }

    private static void thread2(int code) {
        System.out.println("thread2 start");
        if (code != 0) {
            throw new RuntimeException("code is illegal");
        }
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println("thread2 end");
    }

    private static void testTask() throws Exception {
        System.out.println("main thread start");
        FutureTask<Integer> f1 = new FutureTask<>(() -> task1(1));
        FutureTask<Integer> f2 = new FutureTask<>(() -> task2(0));
        Thread t1 = new Thread(f1);
        Thread t2 = new Thread(f2);
        t1.start();
        t2.start();
        // t1.join();
        // t2.join();
        // f1.run();
        // f2.run();
        System.out.println(f1.get());
        System.out.println(f2.get());
        System.out.println("main thread end");
    }

    private static Integer task1(int code) {
        System.out.println("task1 start");
        if (code != 0) {
            throw new RuntimeException("code is illegal");
        }
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println("task1 end");
        return 1;
    }

    private static Integer task2(int code) {
        System.out.println("task2 start");
        if (code != 0) {
            throw new RuntimeException("code is illegal");
        }
        try {
            Thread.sleep(3000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println("task2 end");
        return 2;
    }

    private static void testExecutorService() throws Exception {
        System.out.println("main thread start");
        ExecutorService executorService = Executors.newCachedThreadPool();
        Future<Integer> f1 = executorService.submit(() -> task1(1));
        Future<Integer> f2 = executorService.submit(() -> task2(0));
        System.out.println(f1.get());
        System.out.println(f2.get());
        System.out.println("main thread end");
        executorService.shutdown();
    }

    private static void testStructuredTaskScope() throws Exception {
        System.out.println("main thread start");
        try (var scope = new StructuredTaskScope<Object>()) {
            Subtask<Integer> t1 = scope.fork(() -> task1(1));
            Subtask<Integer> t2 = scope.fork(() -> task2(0));
            scope.join();
            if (t1.state() == Subtask.State.SUCCESS) {
                System.out.println(t1.get());
            } else {
                System.out.println("task1 error: " + t1.exception().getMessage());
            }
            System.out.println(t2.get());
        }
        System.out.println("main thread end");
    }

    private static void testStructuredTaskScopeShutdownOnFailure() throws Exception {
        System.out.println("main thread start");
        try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
            Subtask<Integer> t1 = scope.fork(() -> task1(1));
            Subtask<Integer> t2 = scope.fork(() -> task2(0));
            scope.join().throwIfFailed();
            System.out.println(t1.get());
            System.out.println(t2.get());
        }
        System.out.println("main thread end");
    }

    private static void testStructuredTaskScopeShutdownOnSuccess() throws Exception {
        System.out.println("main thread start");
        try (var scope = new StructuredTaskScope.ShutdownOnSuccess<Object>()) {
            scope.fork(() -> task1(0));
            scope.fork(() -> task2(0));
            scope.join();
            System.out.println(scope.result());
        }
        System.out.println("main thread end");
    }
}