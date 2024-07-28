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

**密钥封装（Key Encapsulation）** 是一种现代加密技术，它使用非对称或公钥加密来保护对称密钥。传统的做法是使用公钥加密随机生成的对称密钥，但这需要 *填充（Padding）* 并且难以证明安全，**密钥封装机制（Key Encapsulation Mechanism，KEM）** 另辟蹊径，使用公钥的属性来推导相关的对称密钥，不需要填充。

KEM 的概念是由 Crammer 和 Shoup 在 [Design and Analysis of Practical Public-Key Encryption Schemes Secure against Adaptive Chosen Ciphertext Attack](https://eprint.iacr.org/2001/108.pdf) 这篇论文中提出的，后来 Shoup 将其提议为 ISO 标准，并于 2006 年 5 月接受并发布为 [ISO 18033-2](https://www.iso.org/standard/37971.html)。

经过多年的发展，KEM 已经在多个密码学领域有所应用：

* 在 [混合公钥加密（Hybrid Public Key Encryption，HPKE）](https://www.rfc-editor.org/rfc/rfc9180) 中，KEM 是基本的构建模块，比如 RSA 密钥封装机制（RSA-KEM）、椭圆曲线集成加密方案（ECIES）等；
* 可以使用 KEM 替换传统的密钥交换协议，比如 [TLS 1.3 中的 Diffie-Hellman 密钥交换步骤](https://www.rfc-editor.org/rfc/rfc8446#section-4.1) 可以建模为 KEM，也就是 Diffie-Hellman KEM (DHKEM)；
* 在 [NIST 后量子密码（Post-Quantum Cryptography，PQC）标准化过程](https://csrc.nist.gov/News/2022/pqc-candidates-to-be-standardized-and-round-4) 中，明确要求对 KEM 和数字签名算法进行评估，作为下一代标准公钥密码算法的候选；KEM 将成为抵御量子攻击的重要工具；

Java 平台中现有的加密 API 都无法以自然的方式表示 KEM，第三方安全提供商的实施者已经表达了对标准 KEM API 的需求。于是，Java 21 引入了一种新的 KEM API，使应用程序能够自然且方便地使用 KEM 算法。

### 对称加密 vs. 非对称加密

https://thiscute.world/posts/practical-cryptography-basics-6-symmetric-key-ciphers/

对称加密是指，使用相同的密钥进行消息的加密与解密。因为这个特性，我们也称这个密钥为「共享密钥（Shared Secret Key）」。

现代密码学中广泛使用的对称加密算法有：AES（AES-128、AES-192、AES-256）、ChaCha20、Twofish、IDEA、Serpent、Camelia、RC6、CAST 等。

https://thiscute.world/posts/practical-cryptography-basics-7-asymmetric-key-ciphers/

非对称加密是一种使用两个不同密钥的加密方式，其中一个称为公钥，另一个称为私钥。公钥可以公开，任何人都可以使用它来加密消息，但只有私钥的持有者才能将其解密。

这种加密方式的主要优点是不需要预先协商密钥，因此非常适合在多方通信中使用。

常见的非对称加密算法包括RSA、ECC等。

### 混合公钥加密

https://thiscute.world/posts/practical-cryptography-basics-5-key-exchange/

### 密钥交换协议

https://blog.csdn.net/Leon_Jinhai_Sun/article/details/89919919

### 后量子密码学

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
