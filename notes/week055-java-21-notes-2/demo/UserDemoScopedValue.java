import java.util.concurrent.StructuredTaskScope;
import java.util.function.Supplier;

public class UserDemoScopedValue {
    
    final static ScopedValue<String> USER = ScopedValue.newInstance();

    public static void main(String[] args) {
        // 从 request 中获取用户信息
        String userId = getUserFromRequest();
        ScopedValue.where(USER, userId)
                .run(() -> {
                    // 查询用户详情
                    String userInfo = new UserService().getUserInfo();
                    System.out.println(userInfo);
                });

        // Exception in thread "main" java.util.NoSuchElementException
        System.out.println(USER.get());

        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    private static String getUserFromRequest() {
        return "admin";
    }

    static class UserService {
        public String getUserInfo() {
            return new UserRepository().getUserInfo();
        }
    }

    static class UserRepository {
        public String getUserInfo() {
            String userId = USER.get();
            Thread.ofPlatform().start(() -> {
                // Exception in thread "Thread-0" java.util.NoSuchElementException
                System.out.println("thread: " + USER.get());
            });

            try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
                Supplier<String> user = scope.fork(() -> USER.get());
                scope.join().throwIfFailed();
                System.out.println("task scope: " + user.get());
            } catch (Exception ex) {
            }
            return String.format("%s:%s", userId, userId);
        }
    }
}
