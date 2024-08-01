# WEEK056 - Java 21 初体验（三）

在 [上一篇笔记](../week055-java-21-notes-2/README.md) 和 [上上一篇笔记](../week050-java-21-notes/README.md) 中，我们学习了 Java 21 中前 10 个重要特性：

* 430: [String Templates (Preview)](https://openjdk.org/jeps/430)
* 431: [Sequenced Collections](https://openjdk.org/jeps/431)
* 439: [Generational ZGC](https://openjdk.org/jeps/439)
* 440: [Record Patterns](https://openjdk.org/jeps/440)
* 441: [Pattern Matching for `switch`](https://openjdk.org/jeps/441)
* 442: [Foreign Function & Memory API (Third Preview)](https://openjdk.org/jeps/442)
* 443: [Unnamed Patterns and Variables (Preview)](https://openjdk.org/jeps/443)
* 444: [Virtual Threads](https://openjdk.org/jeps/444)
* 445: [Unnamed Classes and Instance Main Methods (Preview)](https://openjdk.org/jeps/445)
* 446: [Scoped Values (Preview)](https://openjdk.org/jeps/446)

接下来，我们将继续学习最后 5 个特性：

* 448: [Vector API (Sixth Incubator)](https://openjdk.org/jeps/448)
* 449: [Deprecate the Windows 32-bit x86 Port for Removal](https://openjdk.org/jeps/449)
* 451: [Prepare to Disallow the Dynamic Loading of Agents](https://openjdk.org/jeps/451)
* 452: [Key Encapsulation Mechanism API](https://openjdk.org/jeps/452)
* 453: [Structured Concurrency (Preview)](https://openjdk.org/jeps/453)

## 向量 API（第六次孵化）

https://openjdk.org/jeps/448

## 弃用 Windows 32-bit x86 移植，为删除做准备

https://openjdk.org/jeps/449

## 准备禁用代理的动态加载

https://openjdk.org/jeps/451

## 密钥封装机制 API

**密钥封装（Key Encapsulation）** 是一种现代加密技术，它使用非对称或公钥加密来保护对称密钥。传统的做法是使用公钥加密随机生成的对称密钥，但这需要 *填充（Paddings）* 并且难以证明安全，**密钥封装机制（Key Encapsulation Mechanism，KEM）** 另辟蹊径，使用公钥的属性来推导相关的对称密钥，不需要填充。

KEM 的概念是由 Crammer 和 Shoup 在 [Design and Analysis of Practical Public-Key Encryption Schemes Secure against Adaptive Chosen Ciphertext Attack](https://eprint.iacr.org/2001/108.pdf) 这篇论文中提出的，后来 Shoup 将其提议为 ISO 标准，并于 2006 年 5 月接受并发布为 [ISO 18033-2](https://www.iso.org/standard/37971.html)。

经过多年的发展，KEM 已经在多个密码学领域有所应用：

* 在 [混合公钥加密（Hybrid Public Key Encryption，HPKE）](https://www.rfc-editor.org/rfc/rfc9180) 中，KEM 是基本的构建模块，比如 RSA 密钥封装机制（RSA-KEM）、椭圆曲线集成加密方案（ECIES）等；
* 可以使用 KEM 替换传统的密钥交换协议，比如 [TLS 1.3 中的 Diffie-Hellman 密钥交换步骤](https://www.rfc-editor.org/rfc/rfc8446#section-4.1) 可以建模为 KEM，也就是 Diffie-Hellman KEM (DHKEM)；
* 在 [NIST 后量子密码（Post-Quantum Cryptography，PQC）标准化过程](https://csrc.nist.gov/News/2022/pqc-candidates-to-be-standardized-and-round-4) 中，明确要求对 KEM 和数字签名算法进行评估，作为下一代标准公钥密码算法的候选；KEM 将成为抵御量子攻击的重要工具；

Java 平台中现有的加密 API 都无法以自然的方式表示 KEM，第三方安全提供商的实施者已经表达了对标准 KEM API 的需求。于是，Java 21 引入了一种新的 KEM API，使应用程序能够自然且方便地使用 KEM 算法。

### 对称加密

上面对 KEM 的描述中涉及大量现代密码学的概念，为了对 KEM 有一个更直观的认识，我们不妨快速浏览一遍密码学的发展历史。

我们经常会在各种讲述一二战的谍战片中看到破译电报的片段，当时使用的密码算法在现在看来是非常简单的，几乎所有的密码系统使用的都是 **对称加密（Symmetric Cryptography）** 算法，也就是说使用相同的密钥进行消息的加密与解密，因为这个特性，我们也称这个密钥为 **共享密钥（Shared Secret Key）**。

![](./images/symmetric-crypto.png)

常见的对称加密算法有：[DES](https://zh.wikipedia.org/wiki/%E8%B3%87%E6%96%99%E5%8A%A0%E5%AF%86%E6%A8%99%E6%BA%96)、[3DES](https://zh.wikipedia.org/wiki/3DES)、[AES](https://zh.wikipedia.org/wiki/%E9%AB%98%E7%BA%A7%E5%8A%A0%E5%AF%86%E6%A0%87%E5%87%86)、[Salsa20 / ChaCha20](https://zh.wikipedia.org/wiki/Salsa20)、[Blowfish](https://zh.wikipedia.org/wiki/Blowfish)、[RC6](https://zh.wikipedia.org/wiki/RC6)、[Camelia](https://zh.wikipedia.org/wiki/Camellia) 等。

其中绝大多数都是 **块密码算法（Block Cipher）** 或者叫 **分组密码算法**，这种算法一次只能加密固定大小的块（例如 128 位）；少部分是 **流密码算法（Stream Cipher）**，流密码算法将数据逐字节地加密为密文流。为了实现加密任意长度的数据，我们通常需要将分组密码算法转换为流密码算法，这被称为 **分组密码的工作模式**，常用的工作模式有：ECB（电子密码本）、CBC（密码块链接）、CTR（计数器）、CFB（密文反馈模式）、OFB（输出反馈模式）、GCM（伽罗瓦/计数器模式）） 等。

分组密码的工作模式其背后的主要思想是把明文分成多个长度固定的组，再在这些分组上重复应用分组密码算法，以实现安全地加密或解密任意长度的数据。某些分组模式（如 CBC）要求将输入拆分为分组，并使用填充算法（例如添加特殊填充字符）将最末尾的分组填充到块大小，也有些分组模式（如 CTR、CFB、OFB、CCM、EAX 和 GCM）根本不需要填充，因为它们在每个步骤中，都直接在明文部分和内部密码状态之间执行异或（XOR）运算。

因此我们在使用对称加密时，往往要指定 *工作模式（Modes）* 和 *填充模式（Paddings）* 这两个参数，下面是使用 Java 标准库提供的接口实现 AES 加密和解密的示例：

```
private static void testAES() throws Exception {

    // 1. 生成对称密钥
    KeyGenerator keyGenerator = KeyGenerator.getInstance("AES");
    keyGenerator.init(new SecureRandom());
    Key secretKey =  keyGenerator.generateKey();

    // 1. 使用固定密钥：128 位密钥 = 16 字节
    // SecretKey secretKey = new SecretKeySpec("1234567890abcdef".getBytes(), "AES");

    // 2. 加密
    Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
    cipher.init(Cipher.ENCRYPT_MODE, secretKey);
    byte[] encrypted = cipher.doFinal("hello".getBytes());

    // 3. 解密
    cipher.init(Cipher.DECRYPT_MODE, secretKey);
    byte[] decrypted = cipher.doFinal(encrypted);
    System.out.println(new String(decrypted));
}
```

我们首先通过 `KeyGenerator` 生成一个对称密钥（也可以直接使用 `SecretKeySpec` 来定义一个固定的密钥，但是要注意密钥的长度），然后通过 `算法名称/工作模式/填充模式` 来获取一个 `Cipher` 实例，这里使用的是 AES 算法，ECB 分组模式以及 PKCS5Padding 填充模式，关于其他算法和模式可参考 [Java Security Standard Algorithm Names](https://docs.oracle.com/en/java/javase/11/docs/specs/security/standard-names.html)。得到 `Cipher` 实例后，就可以对数据进行加密和解密，可以看到，这里加密和解密使用的是同一个密钥。

对称加密算法的问题有两点：

* 需要安全的通道进行密钥交换，早期最常见的是面对面交换密钥，一旦密钥泄露，数据将完全暴露；
* 每个点对点通信都需要使用不同的密钥，密钥的管理会变得很困难，如果你需要跟 100 个朋友安全通信，你就要维护 100 个不同的对称密钥；

综上，对称加密会导致巨大的 **密钥交换** 跟 **密钥保存与管理** 的成本。

### 密钥交换协议

为了解决对称加密存在的两大问题，密码学家们前仆后继，想出了各种各样的算法，其中最关键的一个是 Whitfield Diffie 和 Martin Hellman [在 1976 年公开发表的一种算法](https://ee.stanford.edu/%7Ehellman/publications/24.pdf)，也就是现在广为人知的 **Diffie–Hellman 密钥交换（Diffie–Hellman Key Exchange，DHKE）** 算法。

![](./images/dhke.png)

上图是经典 DHKE 协议的整个过程，其基本原理涉及到数学中的 **模幂（Modular Exponentiations）** 和 **离散对数（Discrete Logarithms）** 的知识。

模幂是指求 `g` 的 `a` 次幂模 `p` 的值，其中 `g` `a` `p` 均为整数，公式如下：

```
A = (g^a) mod p
```

而离散对数是指在已知 `g` `p` 和模幂值 `A` 的情况下，求幂指数 `a` 的逆过程。

我们通过将 `p` 设置为一个非常大的质数，使用计算机计算上述模幂的值是非常快的，但是求离散对数却非常困难，这也就是所谓的 **离散对数难题（Discrete Logarithm Problem，DLP）**。

在 DHKE 协议中，Alice 和 Bob 首先约定好两个常数 `g` 和 `p`，这两个数所有人都可见。然后他们分别生成各自的私钥 `a` 和 `b`，这两个值各自保存，不对外公开。他们再分别使用各自的私钥计算出模幂 `A` 和 `B`，这两个值就是他们的公钥：

```
A = (g^a) mod p
B = (g^b) mod p
```

接着，Alice 将 `A` 发送给 Bob，Bob 将 `B` 发送给 Alice，接受到彼此的公钥之后，他们使用自己的私钥来计算模幂：

```
S1 = (B^a) mod p
S2 = (A^b) mod p
```

根据模幂的数学性质，我们可以得知 `S1` 和 `S2` 是相等的！

```
S1 = (B^a) mod p = (g^b)^a mod p = ( g^(b*a) ) mod p
S2 = (A^b) mod p = (g^a)^b mod p = ( g^(a*b) ) mod p
```

至此 Alice 和 Bob 就协商出了一个共享密钥，这个密钥可以在后续的通讯中作为对称密钥来加密通讯内容。可以看到，尽管整个密钥交换过程是公开的，但是任何窃听者都无法根据公开信息推算出密钥，这就是密钥交换协议的巧妙之处。

下面的代码演示了如何在 Java 中实现标准的 DHKE 协议：

```
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
```

这里首先通过 `KeyPairGenerator` 为 Alice 和 Bob 分别生成密钥对（密钥对中包含了一个私钥和一个公钥，也就是上文中的 `a/b` 和 `A/B`），然后使用 `KeyAgreement.getInstance("DH")` 获取一个 `KeyAgreement` 实例，用于密钥协商，Alice 根据 Bob 的公钥协商出对称密钥 `S1`，Bob 根据 Alice 的公钥协商出对称密钥 `S2`，根据输出结果可以看到 `S1` 和 `S2` 是相等的。

### 非对称加密

从第一次世界大战、第二次世界大战到 1976 年这段时期密码的发展阶段，被称为 **近代密码阶段**。1976 年是密码学的一个分水岭，自 DHKE 算法被提出之后，**公钥密码学（Public-key Cryptography）** 的概念开始深入人心。这是密码学领域一项划时代的发明，它宣告了近代密码阶段的终结，是现代密码学的起点。

https://blog.csdn.net/Leon_Jinhai_Sun/article/details/89919919

https://thiscute.world/posts/practical-cryptography-basics-7-asymmetric-key-ciphers/

非对称加密是一种使用两个不同密钥的加密方式，其中一个称为公钥，另一个称为私钥。公钥可以公开，任何人都可以使用它来加密消息，但只有私钥的持有者才能将其解密。

这种加密方式的主要优点是不需要预先协商密钥，因此非常适合在多方通信中使用。

常见的非对称加密算法包括RSA、ECC等。

### 混合公钥加密

https://thiscute.world/posts/practical-cryptography-basics-5-key-exchange/

### 后量子密码学

如果攻击者拥有大型量子计算机，那么他可以使用秀尔算法解决离散对数问题，从而破解私钥和共享秘密。目前的估算认为：破解256位素数域上的椭圆曲线，需要2330个量子比特与1260亿个托佛利门。相比之下，使用秀尔算法破解2048位的RSA则需要4098个量子比特与5.2万亿个托佛利门。因此，椭圆曲线会更先遭到量子计算机的破解。目前还不存在建造如此大型量子计算机的科学技术，因此椭圆曲线密码学至少在未来十年（或更久）依然是安全的。但是密码学家已经积极展开了后量子密码学的研究。其中，超奇异椭圆曲线同源密钥交换（SIDH）有望取代当前的常规椭圆曲线密钥交换（ECDH）。

https://xueqiu.com/8483208408/287316931

### 密钥封装机制

密钥封装机制（Key Encapsulation Mechanism, KEM）是一种基于非对称加密的密钥交换技术。其主要目的是在不直接暴露私钥的情况下安全地传输会话密钥。

在KEM中，发起方运行一个封装算法产生一个会话密钥以及与之对应的密文，随后将会话密钥封装发送给接收方。

接收方收到密文后，使用自己的私钥进行解封，从而获得相同的会话密钥。

https://openjdk.org/jeps/452

https://www.panziye.com/back/10595.html

https://www.zhihu.com/question/443779639

https://www.javatpoint.com/key-encapsulation-mechanism-api-in-java-21

https://juejin.cn/post/7281633636818190388

https://www.geeksforgeeks.org/introduction-to-key-encapsulation-mechanism-api-in-java/

## 结构化并发（预览版本）

https://openjdk.org/jeps/453

## 参考

* [Java 9 - 21：新特性解读](https://www.didispace.com/java-features/)
* [Java 21 新特性概览](https://javaguide.cn/java/new-features/java21.html)
* [深入剖析Java新特性](https://learn.lianglianglee.com/%E4%B8%93%E6%A0%8F/%E6%B7%B1%E5%85%A5%E5%89%96%E6%9E%90Java%E6%96%B0%E7%89%B9%E6%80%A7/)
* [Java21新特性教程](https://www.panziye.com/back/10563.html)
* [结构化并发 | 楚权的世界](http://chuquan.me/2023/03/11/structured-concurrency/)
* [聊一聊Java 21，虚拟线程、结构化并发和作用域值](https://cloud.tencent.com/developer/article/2355577)
* [写给开发人员的实用密码学（五）—— 密钥交换 DHKE 与完美前向保密 PFS](https://thiscute.world/posts/practical-cryptography-basics-5-key-exchange/)
* [写给开发人员的实用密码学（六）—— 对称密钥加密算法](https://thiscute.world/posts/practical-cryptography-basics-6-symmetric-key-ciphers/)
* [写给开发人员的实用密码学（七）—— 非对称密钥加密算法 RSA/ECC](https://thiscute.world/posts/practical-cryptography-basics-7-asymmetric-key-ciphers/)
