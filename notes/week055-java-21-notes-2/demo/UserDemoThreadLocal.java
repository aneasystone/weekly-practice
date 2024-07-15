public class UserDemoThreadLocal {
    
    // private final static ThreadLocal<String> USER = new ThreadLocal<>();
    private final static ThreadLocal<String> USER = new InheritableThreadLocal<>();
    
    public static void main(String[] args) {
        
        // 从 request 中获取用户信息
        String userId = getUserFromRequest();
        USER.set(userId);

        // 查询用户详情
        String userInfo = new UserService().getUserInfo();
        System.out.println(userInfo);

        // ok
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
                System.out.println("platform thread: " + USER.get());
            });
            Thread.ofVirtual().start(() -> {
                System.out.println("virtual thread: " + USER.get());
            });
            return String.format("%s:%s", userId, userId);
        }
    }
}
