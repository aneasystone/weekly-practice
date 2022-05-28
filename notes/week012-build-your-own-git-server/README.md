# WEEK012 搭建自己的 Git 服务器

根据 [RhodeCode][1] 在 2016 年做过的一项分析报告 [Version Control Systems Popularity in 2016][2]，在如今的 VCS（版本控制系统）领域，Git 几乎已经一统江山，在选择自己的 VCS 时，有 87% 的人会选择使用 Git，排在第二名的 SVN 只占 6%，无论是从 Google Trends，还是在 Stack Overflow 上的提问，都可以看到 Git 的爆发式增长。另外，根据 Eclipse 的社区调查 （Eclipse Community Survey），在 2010 年前后，SVN 的使用率都远超其他几款 VCS，从 2010 年开始，SVN 的使用率开始快速下滑，相应的，Git 的使用率快速上升，并在 2014 年超过了 SVN。

![](./images/vcs-popularity-eclipse-community.jpg)

现在，Git 已经成为了程序员的必备技能，越来越多的企业开始采用 Git。在开源的世界里，Github 是程序员聚集的狂欢之地，但这并不适合企业的私有项目，虽然 Github 也支持创建私有项目，但是搭建一个自己的 Git 服务器在很多时候可能是更好的选择，这篇博客将介绍并学习几种搭建 Git 服务器的方法。

Git 支持四种不同的传输协议：本地协议（Local）、HTTP(S) 协议、SSH（Secure Shell）协议以及 Git 协议，这四种协议在不同的场合有不同的用途，并且各有利弊，可以根据实际情况来选择。

## 一、本地协议

本地协议是 Git 最基本的协议，当我们想在本地做一些 Git 实验时，这将非常有用。我们首先建立两个目录：`/git/repo` 和 `~/working`，前者作为远程版本库，后者作为本地工作目录。

```
aneasystone@little-stone:~$ sudo mkdir -p /git/repo
aneasystone@little-stone:~$ sudo git init --bare /git/repo/test.git
已初始化空的 Git 仓库于 /git/repo/test.git/
```

我们在 `/git/repo` 目录通过 `git init --bare` 命令创建一个裸仓库（bare repository，即一个不包含当前工作目录的仓库），只要这一步，我们就可以开始使用了。接着我们在工作目录 `clone` 这个版本库：

```
aneasystone@little-stone:~$ cd ~/working/
aneasystone@little-stone:~/working$ git clone /git/repo/test.git
正克隆到 'test'...
warning: 您似乎克隆了一个空仓库。
完成。
```

然后我们可以使用 `pull`、`push` 就像操作其他的版本库一样。

```
aneasystone@little-stone:~/working$ cd test/
aneasystone@little-stone:~/working/test$ touch 1
aneasystone@little-stone:~/working/test$ touch 2
aneasystone@little-stone:~/working/test$ git add .
aneasystone@little-stone:~/working/test$ git commit -m 'first commit'
[master （根提交） 4983f84] first commit
 2 files changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 1
 create mode 100644 2
aneasystone@little-stone:~/working/test$ sudo git push
[sudo] aneasystone 的密码： 
对象计数中: 3, 完成.
Delta compression using up to 8 threads.
压缩对象中: 100% (2/2), 完成.
写入对象中: 100% (3/3), 205 bytes | 205.00 KiB/s, 完成.
Total 3 (delta 0), reused 0 (delta 0)
To /git/repo/test.git
 * [new branch]      master -> master
```

本地协议不仅在做 Git 实验时很有用，如果你的团队有一个共享文件系统，可以在这个共享文件系统上创建一个远程版本库，团队成员把这个共享文件系统挂在本地，就可以直接使用本地协议进行协作开发，完全不需要搭建一台专门的 Git 服务器。

## 二、SSH 协议

本地协议虽然简单，但是一般来说并不适用，因为你无法控制用户对共享文件系统的操作，用户拥有 push 权限也就意味着用户对远程目录拥有完整的 Shell 权限，他们有可能会无意甚至有意的修改或删除 Git 内部文件，损坏 Git 仓库。

更安全的做法是使用专门的 Git 服务器，如果你有一台可以使用 SSH 连接的服务器，搭建 Git 服务将会非常简单。首先我们要确保服务器上运行着 SSH 服务（`sshd`），大多数 Linux 服务器版本都默认包含了该服务，如果没有，可以先安装 `openssh-server`。然后在服务器上创建 Git 远程版本库：

```
root@myserver:~# mkdir -p /git/repo
root@myserver:~# git init --bare /git/repo/test.git
已初始化空的 Git 仓库于 /git/repo/test.git/
```

然后在本地 `clone` 这个版本库：

```
aneasystone@little-stone:~/working$ git clone ssh://root@myserver/git/repo/test.git
正克隆到 'test'...
root@myserver's password: 
warning: 您似乎克隆了一个空仓库。
```

可以看到和使用本地协议几乎一样，不同的地方在于，在 clone 的时候需要在 URL 前面加上 `ssh://root@myserver`，你也可以使用 scp 式的写法：

```
$ git clone root@myserver:/git/repo/test.git
```

另外一点不同的地方是，每次 `pull`、`push` 的时候都需要输入远程服务器的 root 密码。很显然，让每个 Git 用户都使用 root 来访问服务器是一种很不安全的做法，有几种方法可以解决这个问题：

* 最显而易见的方法是为每个 Git 用户创建一个独立的账号，并分别为他们分配对仓库的读写权限，这种方法行的通，但是对账号的管理非常麻烦，在团队人员不是很多的时候可以尝试，但是并不推荐；
* 另一种方法是配置 SSH 服务器使用某个已有的认证系统来管理用户，比如 [LDAP][4]，这在很多企业中是很常见的，这样可以省去用 `adduser` 手工管理服务器账号的麻烦；
* 还有一种方法是只创建一个账号，比如叫做 git，他对仓库具有读写权限，大家都使用这个账号来访问仓库。这种方法的好处是用户管理起来比较简单，而且可以使用后面介绍的 `authorized_keys` 文件对用户的公钥进行管理；

下面我们尝试下第三种方法。首先在服务器上创建一个名叫 git 的账号：

```
root@myserver:~# adduser git
Adding user `git' ...
Adding new group `git' (1000) ...
Adding new user `git' (1000) with group `git' ...
Creating home directory `/home/git' ...
Copying files from `/etc/skel' ...
Enter new UNIX password: 
Retype new UNIX password: 
passwd: password updated successfully
Changing the user information for git
Enter the new value, or press ENTER for the default
	Full Name []: git
	Room Number []:   
	Work Phone []: 
	Home Phone []: 
	Other []: 
Is the information correct? [Y/n] Y
```

再设置一下 git 仓库的权限（默认情况下，git 仓库的权限为 `rwxr-xr-x`，只有创建者 root 有写的权限，也就意味着使用 git 账号只能 `clone` `pull`，不能 `push`）：

```
# chmod a+w -R /git/repo/test.git
```

我们这里非常粗暴的使用 `chmod a+w` 将 git 仓库设置为对所有人可写，这里可以想一想，如果我们希望设置某些用户对仓库具有只读的权限，该怎么做呢？

然后就可以在本地愉快的进行 git 操作了：

```
$ git clone git@myserver:/git/repo/test.git
```

到这里似乎一切都很正常，但是几次实操之后你就会发现，每次 git 操作都要输入一次密码，这也太麻烦了，能不能“免密提交代码”呢？首先我们要知道，只要能通过 SSH 登陆到服务器，我们就能操作 git，所以如果 SSH 能支持免密登陆，我们就可以“免密提交代码”。还好，SSH 支持公钥认证，这种认证方式无需密码登陆。在 Linux 操作系统中，每个用户都可以拥有自己的一个或多个密钥对（公钥和私钥成对出现），这些密钥一般情况会保存在 `~/.ssh` 目录下，在开始之前，我们先确认下自己是否已经生成过公钥了，可以看下这个目录下是否有 `id_dsa.pub` 或 `id_rsa.pub` 这样的文件，如果没有，我们通过 `ssh-keygen` 来生成：

```
aneasystone@little-stone:~/.ssh$ ssh-keygen
Generating public/private rsa key pair.
Enter file in which to save the key (/home/aneasystone/.ssh/id_rsa): 
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/aneasystone/.ssh/id_rsa.
Your public key has been saved in /home/aneasystone/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:4Ulpufuhs/AgDMb0VXnqMUTw6bD/HrAOI2z9c1cod9I aneasystone@little-stone
The key's randomart image is:
+---[RSA 2048]----+
|      .oo.       |
|       oo+.      |
|  .   o.Oo       |
| o . . B++       |
|  + . ..So   o   |
| . + . ..+. + E  |
|    * * + oo +   |
|   . o Oo+.o.    |
|        **+.     |
+----[SHA256]-----+
```

这样我们在 `~/.ssh` 目录生成了两个文件，`id_rsa` 是你的私钥，`id_rsa.pub` 是你的公钥。关于私钥和公钥的原理以及 RSA 加密算法等内容可以参考我之前写过的一篇介绍 [HTTPS 和证书][5] 的文章。

我们假设你的 Git 服务器是由专门的服务器管理员负责维护和管理，当你生成你的公钥之后，就可以给服务器管理员发送一封申请 Git 服务的邮件，并附上你的公钥。服务器管理员在收到你的申请之后，如果同意了，就可以进行下面的操作：

首先将公钥文件拷贝到服务器上：

```
# scp id_rsa.pub root@myserver:/home/git
```

将公钥文件的内容追加到 git 账户的 authorized_keys 文件中（要注意的是，如果是第一次操作，/home/git 目录下是没有 .ssh 目录的，需要手工创建 .ssh 目录和 authorized_keys 文件）：

```
root@myserver:/home/git# cat id_rsa.pub >> /home/git/.ssh/authorized_keys
```

后续如果有其他的用户申请 Git 服务，都可以按照这个步骤操作。一旦完成这个操作，服务器管理员将会回复你的邮件，通知你 Git 服务已经开通，这个时候你再进行 git 操作就可以不用输入密码了。关于 SSH 的使用，更详细的步骤可以参考 Github 上的这篇指南：[Connecting to GitHub with SSH][6]。

作为服务器管理员，关于 SSH 还有一点需要考虑，那就是 SSH 的安全问题。在上面介绍本地协议时，我们说这种方式无法控制用户对 Git 仓库的操作，无法防止用户有意或无意的损坏 Git 仓库，使用 SSH 协议一样存在这样的问题，用户能通过 SSH 拉取和提交代码，也就意味着用户可以通过 SSH 连接到服务器，对 Git 仓库进行任何操作，这是一件很让人担心的事情。

因此，我们还需要对 git 账号做一些限制。默认情况下，我们新建账号的登陆 shell 是 `/bin/bash`，这个配置在 `/etc/passwd` 文件中：

```
git:x:1000:1000:git,,,:/home/git:/bin/bash
```

可以使用 `chsh` 命令修改用户的登陆 shell，让他不能通过 SSH 访问服务器，怎么修改呢？我们可以看一下 `/etc/shells` 文件，这里定义了所有可以使用的登陆 shell，你可以将 `/bin/bash` 改成这里的任何一个：

```
root@myserver:~# cat /etc/shells 
# /etc/shells: valid login shells
/bin/sh
/bin/dash
/bin/bash
/bin/rbash
```

很显然，这些 shell 并不是我们想要的，有没有一个 shell 只允许用户进行 git 操作，而不允许其他操作呢？还好，Git 的软件包提供了一个名叫 [`git-shell` 的登陆 shell][7]，我们可以把他加进去，一般情况下位于 `/usr/bin/git-shell`。我们使用 `chsh` 修改 git 的登陆 shell：

```
root@myserver:~# chsh git
Changing the login shell for git
Enter the new value, or press ENTER for the default
	Login Shell [/bin/bash]: /usr/bin/git-shell
```

这样当用户 git 通过 SSH 连接服务器时，就会直接被拒绝了。

## 三、Git 协议

SSH 协议解决了用户直接操作 Git 仓库的权限问题，但是如果我们希望对除仓库维护者之外的所有人都开放 Git 仓库的只读权限，这在开源项目中和企业内部往往是很常见的，任何人都可以去查看仓库的代码，这时管理员需要给每一个用户配置 SSH 密钥是非常麻烦的。虽然也可以使用变通的方法来达到这个效果，但是很繁琐，下面是具体的步骤：

* 使用 `g+w` 设置 Git 仓库的权限，让仓库创建者所在的用户组具有写权限，而不是所有人都有写权限（这一步通常也可以在 `git init` 的时候加上 `--shared` 参数）；
* 然后将 git 账号加到仓库创建者的用户组；
* 再创建一个 git_ro 账户，这个账户对仓库只有只读权限；
* 最后为 git_ro 账户创建一个密钥对，把 git_ro 的私钥公开出来供所有人使用。

可以看到使用 SSH 协议最终都逃不过授权这一步，而且公开私钥的做法也不是很优雅。实际上，Git 提供了另一种方式来让这个操作更简单，那就是 Git 协议。使用 Git 协议必须要在服务器上运行 Git 守护进程，git 命令自带了一个 `daemon` 参数：

```
root@myserver:~# git daemon --reuseaddr --base-path=/git/repo/ /git/repo/
```

上面的各个参数可以 [参考 git-daemon 的文档][8]。git-daemon 会监听 9418 端口，如果你的服务器有防火墙，需要将该端口添加到白名单，如果你使用的是阿里云服务器，需要像下面这样添加一个安全组规则：

![](./images/security-group.jpg)

为了让所有的用户都可以访问我们的仓库，还需要在仓库目录下创建一个名为 `git-daemon-export-ok` 的文件：

```
root@myserver:~# cd /git/repo/test.git/
root@myserver:/git/repo/test.git/# touch git-daemon-export-ok
```

至此，所有人都可以通过 Git 协议来克隆或拉取项目源码了（注意上面指定了 `base-path` 参数为 `/git/repo/`，所以 URL 可以直接写 `git://myserver/test.git`）：

```
aneasystone@little-stone:~/working$ git clone git://myserver/test.git
```

一般情况下，服务器管理员还会做一些其他的配置，譬如在服务器重启时让 Git 守护进程自动启动，这有很多种方式可以实现，可以参考《Pro Git》 [Git 守护进程][10] 这一节的内容。

## 四、HTTP(S) 协议

我们一般通过 Git 协议进行无授权访问，通过 SSH 协议进行授权访问，如果你的项目是内部项目，只针对部分授权用户，那使用 SSH 协议就足够了，但是如果既需要授权访问也需要无授权访问，可能需要 SSH 协议和 Git 协议搭配使用，这在维护上成本很高。这时就到了我们的压轴戏 —— HTTP 协议出场的时候了，它同时支持上面两种访问方式。

通过 HTTP 协议访问 Git 服务是目前使用最广泛的方式，它支持两种模式：旧版本的 `Dumb HTTP` 和 新版本的 `Smart HTTP`，Dumb HTTP 一般很少使用，下面除非特殊说明，所说的 HTTP 协议都是 Smart HTTP。使用 HTTP 协议的好处是可以使用各种 HTTP 认证机制，比如用户名/密码，这比配置 SSH 密钥要简单的多，对普通用户来说也更能接受。如果担心数据传输安全，也可以配置 HTTPS 协议，这和普通的 Web 服务是一样的。

下面我们就来尝试搭建一个基于 HTTP 协议的 Git 服务器。《Pro Git》上提供了一个[基于 Apache 的配置示例][11]，如果你是使用 Apache 作为 Web 服务器，可以参考之，我们这里使用 Nginx 来作为 Web 服务器，其原理本质上是一样的，都是通过 Web 服务器接受 HTTP 请求，并将请求转发到 Git 自带的一个名为 [`git-http-backend` 的 CGI 脚本][12]。

首先我们安装所需的软件：

```
# apt-get install -y git-core nginx fcgiwrap apache2-utils
```

其中，Nginx 作为 Web 服务器，本身是不能执行外部 CGI 脚本的，需要通过 [fcgiwrap][13] 来中转，就像使用 php-fpm 来执行 PHP 脚本一样。apache2-utils 是 Apache 提供的一个 Web 服务器的工具集，包含了一些有用的小工具，譬如下面我们会用到的 htpasswd 可以生成 Basic 认证文件。

启动 nginx 和 fcgiwrap，并访问 `http://myserver` 测试 Web 服务器是否能正常访问：

```
# service nginx start
# service fcgiwrap start
```

然后我们打开并编辑 Nginx 的配置文件（`/etc/nginx/sites-available/default`）:

```
location / {
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME /usr/lib/git-core/git-http-backend;
        fastcgi_param GIT_HTTP_EXPORT_ALL "";
        fastcgi_param GIT_PROJECT_ROOT /git/repo;
        fastcgi_param PATH_INFO $uri;
        fastcgi_param REMOTE_USER $remote_user;
        fastcgi_pass unix:/var/run/fcgiwrap.socket;
}
```

这里通过 `fastcgi_param` 设置了一堆的 FastCGI 参数，如下：

* SCRIPT_FILENAME：指定 CGI 脚本 `git-http-backend` 的位置，表示每次 HTTP 请求会被转发到该 CGI 脚本；
* GIT_HTTP_EXPORT_ALL：`git-http-backend` 默认只能访问目录下有 `git-daemon-export-ok` 文件的 Git 仓库，和上面介绍的 Git 协议是一样的，如果指定了 GIT_HTTP_EXPORT_ALL，表示允许访问所有仓库；
* GIT_PROJECT_ROOT：Git 仓库的根目录；
* REMOTE_USER：如果有认证，将认证的用户信息传到 CGI 脚本；

改完之后我们重启 Nginx，并通过 HTTP 协议 `clone` 仓库：

```
aneasystone@little-stone:~/working$ git clone http://myserver/test.git
```

### 4.1 开启身份认证

到这里一切 OK，但是当我们 `push` 代码的时候，却会报下面的 403 错误：

```
aneasystone@little-stone:~/working/test$ git push origin master
fatal: unable to access 'http://myserver/test.git/': The requested URL returned error: 403
```

为了解决这个错误，我们可以在 [git-http-backend 的官网文档][14] 上找到这样的一段描述：

> By default, only the `upload-pack` service is enabled, which serves *git fetch-pack* and *git ls-remote* clients, which are invoked from *git fetch*, *git pull*, and *git clone*. If the client is authenticated, the `receive-pack` service is enabled, which serves *git send-pack* clients, which is invoked from *git push*.

第一次读这段话可能会有些不知所云，这是因为我们对这里提到的 `upload-pack`、`fetch-pack`、`receive-pack`、`send-pack` 这几个概念还没有什么认识。但是我们大抵可以猜出来，默认情况下，只有认证的用户才可以 push 代码，如果某个 Git 仓库希望所有用户都有权限 push 代码，可以为相应的仓库设置 `http.receivepack`：

```
root@myserver:/# cd /git/repo/test.git/
root@myserver:/git/repo/test.git# git config http.receivepack true
```

当然最好的做法还是对 push 操作开启认证，官网文档上有一个 [lighttpd 的配置][15] 我们可以借鉴：

```
$HTTP["querystring"] =~ "service=git-receive-pack" {
	include "git-auth.conf"
}
$HTTP["url"] =~ "^/git/.*/git-receive-pack$" {
	include "git-auth.conf"
}
```

这个配置看上去非常简单，但是想要理解为什么这样配置，就必须去了解下 Git 的内部原理。正如上面 git-http-backend 文档上的那段描述，当 Git 客户端执行 *git fetch*, *git pull*, and *git clone* 时，会调用 `upload-pack` 服务，当执行 *git push* 时，会调用 `receive-pack` 服务，为了更清楚的说明这一点，我们来看看 Nginx 的访问日志。

执行 `git clone`：

```
[27/Nov/2018:22:18:00] "GET /test.git/info/refs?service=git-upload-pack HTTP/1.1" 200 363 "-" "git/1.9.1"
[27/Nov/2018:22:18:00] "POST /test.git/git-upload-pack HTTP/1.1" 200 306 "-" "git/1.9.1"
```

执行 `git pull`：

```
[27/Nov/2018:22:20:25] "GET /test.git/info/refs?service=git-upload-pack HTTP/1.1" 200 363 "-" "git/1.9.1"
[27/Nov/2018:22:20:25] "POST /test.git/git-upload-pack HTTP/1.1" 200 551 "-" "git/1.9.1"
```

执行 `git push`：

```
[27/Nov/2018:22:19:33] "GET /test.git/info/refs?service=git-receive-pack HTTP/1.1" 401 204 "-" "git/1.9.1"
admin [27/Nov/2018:22:19:33] "GET /test.git/info/refs?service=git-receive-pack HTTP/1.1" 200 193 "-" "git/1.9.1"
admin [27/Nov/2018:22:19:33] "POST /test.git/git-receive-pack HTTP/1.1" 200 63 "-" "git/1.9.1"
```

可以看到执行 clone 和 pull 请求的接口是一样的，先请求 `/info/refs?service=git-upload-pack`，然后再请求 `/git-upload-pack`；而 push 是先请求 `/info/refs?service=git-receive-pack`，然后再请求 `/git-receive-pack`，所以在上面的 lighttpd 的配置中我们看到了两条记录，如果要对 push 做访问控制，那么对这两个请求都要限制。关于 Git 传输的原理可以参考 《Pro Git》的 [Git 内部原理 - 传输协议][16] 这一节。

我们依葫芦画瓢，Nginx 配置文件如下：

```
location @auth {
        auth_basic "Git Server";
        auth_basic_user_file /etc/nginx/passwd;

        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME /usr/lib/git-core/git-http-backend;
        fastcgi_param GIT_HTTP_EXPORT_ALL "";
        fastcgi_param GIT_PROJECT_ROOT /git/repo;
        fastcgi_param PATH_INFO $uri;
        fastcgi_param REMOTE_USER $remote_user;
        fastcgi_pass unix:/var/run/fcgiwrap.socket;
}

location / {
        error_page 418 = @auth;
        if ( $query_string = "service=git-receive-pack" ) {  return 418; }
        if ( $uri ~ "git-receive-pack$" ) { return 418; }

        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME /usr/lib/git-core/git-http-backend;
        fastcgi_param GIT_HTTP_EXPORT_ALL "";
        fastcgi_param GIT_PROJECT_ROOT /git/repo;
        fastcgi_param PATH_INFO $uri;
        fastcgi_param REMOTE_USER $remote_user;
        fastcgi_pass unix:/var/run/fcgiwrap.socket;
}
```

其中相同的配置我们也可以用 `include` 指令放在一个共用的配置文件里，这样我们就实现了在 push 的时候需要填写用户名和密码了。我们通过 Nginx 的 `auth_basic_user_file` 指令来做身份认证，用户名和密码保存在 `/etc/nginx/passwd` 文件中，这个文件可以使用上面提到的 apache2-utils 包里的 htpasswd 来生成：

```
root@myserver:/# htpasswd -cb /etc/nginx/passwd admin 123456
```

另外，在 push 的时候，有时候可能会遇到 `unpack failed: unable to create temporary object directory` 这样的提示错误：

```
aneasystone@little-stone:~/working/test$ git push origin master
Counting objects: 3, done.
Writing objects: 100% (3/3), 193 bytes | 0 bytes/s, done.
Total 3 (delta 0), reused 0 (delta 0)
error: unpack failed: unable to create temporary object directory
To http://myserver/test.git
 ! [remote rejected] master -> master (unpacker error)
error: failed to push some refs to 'http://myserver/test.git'
```

这一般情况下都是由于 Git 仓库目录的权限问题导致的，在这里 Git 仓库的根目录 `/git/repo` 是 root 创建的，而运行 nginx 和 fcgiwrap 的用户都是 www-data，我们可以把 Git 仓库目录设置成对所有人可读可写，也可以像下面这样将它的拥有者设置成 www-data 用户：

```
root@myserver:/# chown -R www-data:www-data /git/repo
```

### 4.2 凭证管理

上面我们站在管理员的角度解决了用户身份认证的问题，但是站在用户的角度，每次提交代码都要输入用户名和密码是一件很痛苦的事情。在上面介绍 SSH 协议时，我们可以使用 SSH 协议自带的公钥认证机制来省去输入密码的麻烦，那么在 HTTP 协议中是否存在类似的方法呢？答案是肯定的，那就是 Git 的凭证存储工具：`credential.helper`。

譬如像下面这样，将用户名和密码信息保存在缓存中：

```
$ git config --global credential.helper cache
```

这种方式默认只保留 15 分钟，如果要改变保留的时间，可以通过 `--timeout` 参数设置，或者像下面这样，将密码保存在文件中：

```
$ git config --global credential.helper store
```

这种方式虽然可以保证密码不过期，但是要记住的是，这种方式密码是以明文的方式保存在你的 home 目录下的。可以借鉴操作系统自带的凭证管理工具来解决这个问题， 比如 OSX Keychain 或者 [Git Credential Manager for Windows][17]。更多的内容可以参考[《Pro Git》凭证存储][18] 这一节。

除此之外，还有一种更简单粗暴的方式：

```
aneasystone@little-stone:~/working$ git clone http://admin:123456@myserver/test.git
```

## 五、综合对比

这一节对 Git 的四大协议做一个综合对比。

* 本地协议
  * 优点：架设简单，不依赖外部服务，直接使用现有文件和网络权限，常用于共享文件系统
  * 缺点：共享文件系统的配置和使用不方便，且无法保护仓库被意外损坏，传输性能较低
* SSH 协议
  * 优点：架设简单，所有数据经过授权加密，数据传输很安全，传输性能很高
  * 缺点：不支持匿名访问，配置 SSH 的密钥对小白用户有一定的门槛
* Git 协议
  * 优点：对开放的项目很适用，无需授权，传输性能最高
  * 缺点：缺乏授权机制，架设较麻烦，企业一般不会默认开放 9418 端口需要另行添加
* HTTP/S 协议
  * 优点：同时支持授权访问和无授权访问，传输性能较高，配合 HTTPS 也可以实现数据安全
  * 缺点：架设 HTTP 服务较麻烦，认证凭证不好管理

## 六、更高级的工具

上面介绍的是搭建 Git 服务器最基本的方法，如果你只是希望能找一个版本控制系统来替代现有的 SVN，这也许就足够了。但如果你希望你的版本控制系统能拥有一个更友好的 UI 界面，能更好的管理你的用户和权限，能支持更现代的 Pull Request 功能以及能和 CI/CD 系统更紧密的联系起来，你就需要一个更高级的工具，你可以试试 [GitWeb][19]、[Gitolite][20]、[Gitlab][21]、[Gogs][22]、[Gitea][23]，当然，如果你愿意，你也可以把代码放在那些流行的代码托管平台上，比如 [Github][24]、[Bitbucket][25] 等等。

## 参考

1. [Version Control Systems Popularity in 2016][26]
1. [Pro Git 第二版][27]
1. [git-http-backend 的官网文档][28]
1. [Connecting to GitHub with SSH][29]
1. [nginx fastcgi 配置][30]
1. [Git远程推送时记住用户名和密码][31]
1. [搭建Git服务器 - 廖雪峰的官方网站][32]
1. [在 Ubuntu 系统上配置 Nginx Git 服务器- 张志敏的技术专栏][33]
1. [Git 服务器基于nginx配置http(s)协议 | Yvanの平行时空][34]


  [1]: https://rhodecode.com/
  [2]: https://rhodecode.com/insights/version-control-systems-2016
  [4]: https://zh.wikipedia.org/wiki/%E8%BD%BB%E5%9E%8B%E7%9B%AE%E5%BD%95%E8%AE%BF%E9%97%AE%E5%8D%8F%E8%AE%AE
  [5]: https://www.aneasystone.com/archives/2016/04/java-and-https.html
  [6]: https://help.github.com/articles/connecting-to-github-with-ssh/
  [7]: https://git-scm.com/docs/git-shell
  [8]: https://git-scm.com/docs/git-daemon
  [10]: https://git-scm.com/book/zh/v2/%E6%9C%8D%E5%8A%A1%E5%99%A8%E4%B8%8A%E7%9A%84-Git-Git-%E5%AE%88%E6%8A%A4%E8%BF%9B%E7%A8%8B
  [11]: https://git-scm.com/book/zh/v2/%E6%9C%8D%E5%8A%A1%E5%99%A8%E4%B8%8A%E7%9A%84-Git-Smart-HTTP
  [12]: https://git-scm.com/docs/git-http-backend/
  [13]: https://github.com/gnosek/fcgiwrap
  [14]: https://git-scm.com/docs/git-http-backend/
  [15]: https://git-scm.com/docs/git-http-backend/#git-http-backend-Lighttpd
  [16]: https://git-scm.com/book/zh/v2/Git-%E5%86%85%E9%83%A8%E5%8E%9F%E7%90%86-%E4%BC%A0%E8%BE%93%E5%8D%8F%E8%AE%AE
  [17]: https://github.com/Microsoft/Git-Credential-Manager-for-Windows
  [18]: https://git-scm.com/book/zh/v2/Git-%E5%B7%A5%E5%85%B7-%E5%87%AD%E8%AF%81%E5%AD%98%E5%82%A8
  [19]: https://git-scm.com/book/zh/v2/%E6%9C%8D%E5%8A%A1%E5%99%A8%E4%B8%8A%E7%9A%84-Git-GitWeb
  [20]: http://gitolite.com/gitolite/
  [21]: https://about.gitlab.com/
  [22]: https://gogs.io/
  [23]: https://gitea.io/zh-cn/
  [24]: https://github.com/
  [25]: https://bitbucket.org/
  [26]: https://rhodecode.com/insights/version-control-systems-2016
  [27]: https://git-scm.com/book/zh/v2
  [28]: https://git-scm.com/docs/git-http-backend/
  [29]: https://help.github.com/articles/connecting-to-github-with-ssh/
  [30]: https://www.zfl9.com/nginx-fcgi.html
  [31]: https://yanyinhong.github.io/2017/05/03/Avoid-typing-password-when-git-push-remote/
  [32]: https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000/00137583770360579bc4b458f044ce7afed3df579123eca000
  [33]: https://beginor.github.io/2016/03/12/http-git-server-on-nginx.html
  [34]: https://www.yvanz.com/2016/06/01/Git-server-with-http(s)-protocol.html
  