public class UserDemo {
    
    public static void main(String[] args) {

        // 从 request 中获取用户信息
        String userId = getUserFromRequest();
        
        // 查询用户详情
        String userInfo = new UserService().getUserInfo(userId);
        System.out.println(userInfo);
    }

    private static String getUserFromRequest() {
        return "admin";
    }

    static class UserService {
        public String getUserInfo(String userId) {
            return new UserRepository().getUserInfo(userId);
        }
    }

    static class UserRepository {
        public String getUserInfo(String userId) {
            return String.format("%s:%s", userId, userId);
        }
    }
}
