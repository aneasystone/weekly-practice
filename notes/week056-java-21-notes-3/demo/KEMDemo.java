import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.SecureRandom;
import java.security.Security;
import java.util.Base64;
import java.util.HexFormat;

import javax.crypto.Cipher;
import javax.crypto.KeyAgreement;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;
import javax.crypto.spec.PBEParameterSpec;
import javax.crypto.spec.SecretKeySpec;

import org.bouncycastle.jce.provider.BouncyCastleProvider;

import javax.crypto.KEM.Decapsulator;
import javax.crypto.KEM.Encapsulated;
import javax.crypto.KEM.Encapsulator;
import javax.crypto.KEM;

public class KEMDemo {
    
    public static void main(String[] args) throws Exception {
        
        testAES();
        testPBE();
        testKeyAgreement();
        testRSA();
        testRSA_AES();
        testKEM();
    }

    private static void testAES() throws Exception {

        // 1. 生成对称密钥
        // KeyGenerator keyGenerator = KeyGenerator.getInstance("AES");
        // keyGenerator.init(new SecureRandom());
        // Key secretKey =  keyGenerator.generateKey();

        // 1. 使用固定密钥：128 位密钥 = 16 字节
        SecretKey secretKey = new SecretKeySpec("1234567890abcdef".getBytes(), "AES");

        // 2. 加密
        Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, secretKey);
        byte[] encrypted = cipher.doFinal("hello".getBytes());

        // 3. 解密
        cipher.init(Cipher.DECRYPT_MODE, secretKey);
        byte[] decrypted = cipher.doFinal(encrypted);
        System.out.println(new String(decrypted));
    }

    private static void testPBE() throws Exception {

        // https://mvnrepository.com/artifact/org.bouncycastle/bcprov-jdk15on
        Security.addProvider(new BouncyCastleProvider());

        // 1. 使用密码，需要生成随机 salt 值
        String password = "123456";
        byte[] salt = SecureRandom.getInstanceStrong().generateSeed(16);

        // 2. 加密
        PBEKeySpec keySpec = new PBEKeySpec(password.toCharArray());
        SecretKeyFactory keyFactory = SecretKeyFactory.getInstance("PBEwithSHA1and128bitAES-CBC-BC");
        SecretKey secretKey = keyFactory.generateSecret(keySpec);
        PBEParameterSpec pbeps = new PBEParameterSpec(salt, 1000);
        Cipher cipher = Cipher.getInstance("PBEwithSHA1and128bitAES-CBC-BC");
        cipher.init(Cipher.ENCRYPT_MODE, secretKey, pbeps);
        byte[] encrypted = cipher.doFinal("hello".getBytes());

        // 3. 解密
        cipher.init(Cipher.DECRYPT_MODE, secretKey, pbeps);
        byte[] decrypted = cipher.doFinal(encrypted);
        System.out.println(new String(decrypted));
    }

    private static void testKeyAgreement() throws Exception {

        // 1. Alice 和 Bob 分别生成各自的密钥对
        KeyPairGenerator keyPairGen = KeyPairGenerator.getInstance("DH");
        keyPairGen.initialize(512);
        KeyPair keyPairAlice = keyPairGen.generateKeyPair();
        KeyPair keyPairBob = keyPairGen.generateKeyPair();

        // 2. Alice 根据 Bob 的公钥协商出对称密钥
        KeyAgreement keyAgreement = KeyAgreement.getInstance("DH");
        keyAgreement.init(keyPairAlice.getPrivate());
        keyAgreement.doPhase(keyPairBob.getPublic(), true);
        byte[] secretKey1 = keyAgreement.generateSecret();

        // 3. Bob 根据 Alice 的公钥协商出对称密钥
        keyAgreement.init(keyPairBob.getPrivate());
        keyAgreement.doPhase(keyPairAlice.getPublic(), true);
        byte[] secretKey2 = keyAgreement.generateSecret();

        // 4. 比较双方的密钥是否一致
        System.out.println("Alice Secret key: " + HexFormat.of().formatHex(secretKey1));
        System.out.println("Bob Secret key: " + HexFormat.of().formatHex(secretKey2));
    }

    private static void testRSA() throws Exception {

        // 1. Bob 生成密钥对
        KeyPairGenerator keyPairGen = KeyPairGenerator.getInstance("RSA");
        keyPairGen.initialize(2048);
        KeyPair keyPairBob = keyPairGen.generateKeyPair();

        // 2. Alice 使用 Bob 的公钥加密数据
        Cipher cipher1 = Cipher.getInstance("RSA");
        cipher1.init(Cipher.ENCRYPT_MODE, keyPairBob.getPublic());
        byte[] encrypted = cipher1.doFinal("hello".getBytes());

        // 3. Bob 使用自己的私钥解密数据
        Cipher cipher2 = Cipher.getInstance("RSA");
        cipher2.init(Cipher.DECRYPT_MODE, keyPairBob.getPrivate());
        byte[] decrypted = cipher2.doFinal(encrypted);

        System.out.println(new String(decrypted));
    }

    private static void testRSA_AES() throws Exception {

        // 1. Bob 生成密钥对
        KeyPairGenerator keyPairGen = KeyPairGenerator.getInstance("RSA");
        keyPairGen.initialize(2048);
        KeyPair keyPair = keyPairGen.generateKeyPair();

        // 2. Alice 生成一个对称密钥
        KeyGenerator keyGen = KeyGenerator.getInstance("AES");
        keyGen.init(256);
        SecretKey secretKey = keyGen.generateKey();

        // 3. Alice 使用 Bob 的公钥加密对称密钥
        Cipher cipher1 = Cipher.getInstance("RSA");
        cipher1.init(Cipher.ENCRYPT_MODE, keyPair.getPublic());
        byte[] secretKeyEncrypted = cipher1.doFinal(secretKey.getEncoded());

        // 4. Bob 使用自己的私钥解密出对称密钥
        Cipher cipher2 = Cipher.getInstance("RSA");
        cipher2.init(Cipher.DECRYPT_MODE, keyPair.getPrivate());
        byte[] secretKeyDecrypted = cipher2.doFinal(secretKeyEncrypted);

        // 5. 比较双方的密钥是否一致
        System.out.println("Alice Secret key: " + HexFormat.of().formatHex(secretKey.getEncoded()));
        System.out.println("Bob Secret key: " + HexFormat.of().formatHex(secretKeyDecrypted));
    }

    private static void testKEM() throws Exception {

        // 1. Bob 生成密钥对
        KeyPairGenerator keyPairGen = KeyPairGenerator.getInstance("X25519");
        KeyPair keyPair = keyPairGen.generateKeyPair();

        // 2. Alice 根据 Bob 的公钥生成一个 Encapsulated 对象，这个对象里包含了：
        //    * 共享密钥 shared secret
        //    * 密钥封装消息 key encapsulation message
        //    * 可选参数 optional parameters
        //    然后 Alice 将密钥封装消息发送给 Bob
        KEM kem1 = KEM.getInstance("DHKEM");
        Encapsulator sender = kem1.newEncapsulator(keyPair.getPublic());
        Encapsulated encapsulated = sender.encapsulate();
        SecretKey k1 = encapsulated.key();

        // 3. Bob 根据自己的私钥和 Alice 发过来的密钥封装消息，计算出共享密钥
        KEM kem2 = KEM.getInstance("DHKEM");
        Decapsulator receiver = kem2.newDecapsulator(keyPair.getPrivate());
        SecretKey k2 = receiver.decapsulate(encapsulated.encapsulation());

        // 4. 比较双方的密钥是否一致
        System.out.println(Base64.getEncoder().encodeToString(k1.getEncoded()));
        System.out.println(Base64.getEncoder().encodeToString(k2.getEncoded()));
    }
}
