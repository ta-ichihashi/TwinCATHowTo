# CX82xxシリーズの利用方法

[Beckhoff RT Linuxの導入](https://infosys.beckhoff.com/content/1033/beckhoff_rt_linux/index.html?id=1171886970310160181)のドキュメントに従い、説明します。このドキュメントではOS無しのIPCに対してインストールする個所からの手順となっていますが、CX82xxにはあらかじめBeckhoff RT Linuxがインストール済みの状態で納入されます。ここからTwinCAT XAEで作成したプロジェクトを動作させるまでの手順を説明します。

## 設置と電源投入

[設置方法はこちら](https://infosys.beckhoff.com/content/1033/cx8290/17622065931.html?id=1102675642323851693)をごらんください。

```{admonition} SDカードの取扱いについて
:class: warning

* SDカードは故障時以外は抜かないでください。
* CX8190のWindowsCEのように、ファイルをコピーするだけでは起動可能なディスクとなりません。
* 故障が疑われる場合は、[こちらの手順](https://infosys.beckhoff.com/content/1033/beckhoff_rt_linux/18419873419.html?id=3406457076941507639) にてSDカードを初期化することができます。
```

電源の配線方法は[こちらのマニュアル](https://infosys.beckhoff.com/content/1033/cx8290/17622165387.html?id=3780875763547875918)をご覧ください。

![](https://infosys.beckhoff.com/content/1033/cx8290/Images/svg/9007216707358731__Web.svg){algin=center}

## 接続

1. 次図のとおりX001がリアルタイムではないEthernetポートです。こちらへXAEがインストールされたWindows PCを接続してください。

    ```{tip}
    X101やX102は、PROFINET (TF627x), EtherNet/IP (TF628x), BACnet/IP (TF8020) 、などのリアルタイムEthernetが使えるほか、通常のソケット通信（TF6310）やADS等にも使うことができます。
    ```

    ![](assets/2025-07-29-10-32-50.png){align=center}

2. IPC側に電源を供給するとSDカードからTwinCAT RT Linuxが起動します。この状態でXAEと接続したIPCのX001に割り当てられたIPアドレスを検索します。Windows側から次の通りPower shellからコマンドを入力して調べます。

    ```{code} powershell
    PS > Get-NetNeighbor -LinkLayerAddress 00-01-05* -AddressFamily IPv6
    ifIndex IPAddress                                          LinkLayerAddress      State       PolicyStore
    ------- ---------                                          ----------------      -----       -----------
    23      fe80::201:5ff:fea3:e942                            00-01-05-**-**-**     Stale       ActiveStore
    ```

3. 応答のあったIPAddress部分を参照して、次の通りSSHで接続を行います。

    初回接続時は自己署名証明書で接続するか確認されます。`yes` を入力して接続してください。

    ``` powershell
    PS > ssh Administrator@fe80::201:5ff:fea3:e942     <----- Administratorユーザで IPv6 のIPアドレスを指定してSSH接続
    The authenticity of host 'fe80::201:5ff:fea3:e942 (fe80::201:5ff:fea3:e942)' can't be established.
    ED25519 key fingerprint is SHA256:YMDaKiSiJ+Hs89lJ2X/Ewq5QCPqT9gWwAac+IqOfxgw.
    This host key is known by the following other names/addresses:
        C:\Users\Takashii/.ssh/known_hosts:9: 192.168.3.45
    Are you sure you want to continue connecting (yes/no/[fingerprint])?  <--- "yes" 
    ```

    つづいてAdministratorのパスワード入力を求められます。工場出荷時は `1` です。

    ``` bash
    Warning: Permanently added 'fe80::201:5ff:fea3:e942' (ED25519) to the list of known hosts.
    Administrator@fe80::201:5ff:fea3:e942's password: <----- 工場出荷パスワード "1" を入力
    Linux BTN-000tr9xa 6.14.9-rt3-bhf2 #1 SMP PREEMPT_RT Fri May 30 13:39:56 UTC 2025 aarch64

    The programs included with the Debian GNU/Linux system are free software;
    the exact distribution terms for each program are described in the
    individual files in /usr/share/doc/*/copyright.

    Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
    permitted by applicable law.
    Last login: Tue Jul 29 01:48:24 2025 from 192.168.3.23
    Administrator@BTN-000*****:~$
    ```

    IPアドレスが変わらない限り、次回からは自己署名証明書が保持されますので、パスワードを入力してログイン可能です。

    ``` powershell
    PS > ssh Administrator@fe80::201:5ff:fea3:e942
    Administrator@fe80::201:5ff:fea3:e942's password: <----- 工場出荷パスワード "1" を入力
    Linux BTN-000tr9xa 6.14.9-rt3-bhf2 #1 SMP PREEMPT_RT Fri May 30 13:39:56 UTC 2025 aarch64

    The programs included with the Debian GNU/Linux system are free software;
    the exact distribution terms for each program are described in the
    individual files in /usr/share/doc/*/copyright.

    Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
    permitted by applicable law.
    Last login: Tue Jul 29 01:48:24 2025 from 192.168.3.23
    Administrator@BTN-000*****:~$
    ```

    上記で接続ができましたので、bash上で様々な操作が可能です。

4. 接続を終えるときは、次のとおり `exit` コマンドを発行してください。

    ``` bash
    Administrator@BTN-000*****:~$ exit
    logout
    Connection to fe80::201:5ff:fea3:e942 closed.
    PS >
    ```

```{tip}
接続後は様々なテキスト形式の設定ファイルを編集してサーバの設定を行います。ターミナル上で利用可能なテキストエディタは、`vi` および、 `nano` です。使い方がより直感的なのは `nano`, キー操作を多用し、操作効率が高いエディタは `vi` です。本ドキュメントでは、主に `nano` を使った例でコマンド紹介します。
```

## パッケージマネージャの設定

Beckhoffの各種製品ソフトウェアは、事前にご登録いただきましたログイン名、およびパスワードを通して debian の apt パッケージマネージャを通じて取得できます。従いまして、事前に[my beckhoff](https://www.beckhoff.com/en-en/mybeckhoff-registration/index.aspx)からユーザアカウントを作成してください。その上でパッケージリスト、およびインストール済みパッケージを最新のものに更新します。

パッケージリストとは、取得可能なパッケージと、そのバージョンが定義されたデータベースです。以下に示す `/etc/apt/sources.list.d` に定義したサーバおよびそのリポジトリからインストール可能なパッケージの目録をダウンロードします。この上で、希望する個々のパッケージをインストールすることが可能になります。

まずは、パッケージのサーバ、およびリポジトリの設定を行います。

1. Beckhoffパッケージサーバへの認証ファイルの定義

    ```{code} bash
    $ sudo nano /etc/apt/auth.conf.d/bhf.conf
    ```

    次の2つのサーバそれぞれに、my beckhoff で作成したユーザ名とパスワードを定義します。

    ```{code} yaml
    machine deb.beckhoff.com
    login <my beckhoffのBeckhoff カウント>
    password <my beckhkoffのログインパスワード>

    machine deb-mirror.beckhoff.com
    login <my beckhoffのBeckhoff カウント>
    password <my beckhkoffのログインパスワード>
    ```

2. TwinCAT RT Linux ベータ版のリポジトリ設定

    現在、TwinCAT RT Linuxはベータ段階です。このため、パッケージマネージャのリポジトリサーバは、 `bookworm` ではなく、 `bookworm-unstable` に書き換える必要があります。`sources.list.d` 以下のファイルを編集します。

    ```{code} bash
    $ sudo nano /etc/apt/sources.list.d/bhf.list
    ```

    APTリポジトリを `bookworm` から `bookworm-unstable` へ書き換えます。

    ```{code} yaml
    # https://deb.beckhoff.com/debian bookworm main
    https://deb.beckhoff.com/debian bookworm-unstable main # add `-unstable`
    ```


```{admonition} これ以後の手順実施にはインターネットへの接続が必要です
:class: important

* 登録したサーバ、リポジトリへ接続する必要があるため、X001に接続したネットワークを通じてインターネットへの接続が必要です。
* インターネットへ接続するために固定IP、
```

上記を正しく設定した上で、パッケージリストを最新に更新します。

```{code} bash
$ sudo apt update
```

続いて次のコマンドによってインストール済みのパッケージを更新したパッケージリストに基づいて最新のものにインストールします。

```{code} bash
$ sudo apt upgrade
```

最後に、TwinCATランタイムをIPCにインストールします。ARMプロセッサ搭載のIPCとそれ以外でインストールする必須パッケージが異なります。ARM以外のアーキテクチャでは、 `libtcrte` もインストールしてください。

ARMプロセッサ向け（CX8290等）
    : ```{code} bash
      $ sudo apt install tc31-xar-um
      ```

それ以外
    : ```{code} bash
      $ sudo apt install tc31-xar-um libtcrte
      ```
## IPアドレスを設定する

前節までの手順でIPv6を通じたログインはできています。設定されているIPv4アドレスや、その他、全てのネットワークインターフェースカードのIPコンフィギュレーションを設定、調べる方法について説明します。

### 現在のIPアドレスを調べる

IP層を構成したり設定を調査するネットワークコマンドは、Windowsでは `ipconfig` コマンド、TwinCAT BSDでは、net-tools系の `ifconfig` コマンドですが、Linuxでは `iproute2` 系の `ip` コマンドが主流です。こちらも初期状態ではインストールされていませんので、次のとおりコマンドをインストールします。

```{code} bash
$ sudo apt install iproute2
```

インストールが終わるとipコマンドが使用できる状態となります。次のコマンドでネットワークのコンフィギュレーションを調べます。

```{code} bash
$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute
       valid_lft forever preferred_lft forever
2: end0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:01:05:a3:e9:42 brd ff:ff:ff:ff:ff:ff
    inet 192.168.3.45/24 metric 1024 brd 192.168.3.255 scope global dynamic end0
       valid_lft 67246sec preferred_lft 67246sec
    inet6 2400:2653:ca21:7800:201:5ff:fea3:e942/64 scope global dynamic mngtmpaddr noprefixroute
       valid_lft 14060sec preferred_lft 12260sec
    inet6 fe80::201:5ff:fea3:e942/64 scope link
       valid_lft forever preferred_lft forever
3: tctap0: <BROADCAST,MULTICAST> mtu 1500 qdisc fq_codel state DOWN group default qlen 1000
    link/ether 00:01:05:a4:d3:d6 brd ff:ff:ff:ff:ff:ff
```

上記のとおり、`192.168.3.45` であることがわかります。

### IPアドレスを設定する

IPアドレスに関する設定は `/etc/systemd/network` 以下にあります。初期状態ではこの下に `020-wired.network` があります。

```{code} toml
$ cat 020-wired.network
[Match]
Name=en* eth*

[Network]
DHCP=yes
LinkLocalAddressing=yes

[DHCPv4]
ClientIdentifier=mac
```

この後に上書き設定されるように、次のファイルを新規作成して編集します。

```{code} bash
$ sudo touch /etc/systemd/network/10-end0-static.network
$ sudo nano /etc/systemd/network/10-end0-static.network 
```

下記の通り、あらかじめ `ip a` コマンドで一覧させたネットワークカードの設定したい対象をNameに指定し、IPアドレスとネットワークアドレスセグメント、および、ゲートウェイアドレスを設定します。

```{code} toml
[Match]
Name=end0

[Network]
Address=192.168.3.45/24
Gateway=192.168.3.1
```

```{admonition} ネットワークアドレス表記
:class: tip

`/24` は、ネットワークアドレスを示すbit数を指定しています。`192.168.3.45` は、8bit x 4桁 でIPアドレスを表しますが、上位 24 bit がネットワークアドレス、つまり、`192.168.3` までとなります。また、それ以下の `.45` の部分はホストアドレスとなります。

上位 24bit が同一のIPアドレス同士であれば、Gatewayで指定したルータを経由せずとも直接通信することができます。
```

設定が完了したら、次のとおりネットワークサービスを再起動したら反映されます。SSH経由では一度ネットワークが切断されますので、再度接続を試みてください。

```{code} bash
$ sudo networkctl reload
```

## 新しいパッケージをインストールする

IPC納品時に含まれていないパッケージを追加するまでの手順をご説明します。ここでは `TF1810 PLC HMI Web`
 を追加インストールするまでの手順を例にご説明します。

まず、`tf1810` というキーワードから、パッケージ名を検索します。 `apt search` コマンドを用います。

```{code} bash
$ sudo apt search tf1810
Sorting... Done
Full Text Search... Done
tf1810-plc-hmi-web/bookworm-unstable,now 4.0.1.0-1 arm64 [installed]
  TF1810 | TC3 PLC HMI Web
```

上記から、パッケージ名は `tf1810-plc-hmi-web` であることが分かります。次の通りPLC HMI Webをインストールします。

```{code} bash
$ sudo apt install tf1810-plc-hmi-web
```

IPCを再起動して、tf1810が稼働しているかどうかを確認してみましょう。TF1810はWEBサーバを用いたPLC HMIソフトウェアです。したがって何等かのTCPポートでサービスを提供しているのか調べる必要があります。

インストールしたパッケージはどのディレクトリにどのようなファイルが追加されたかを一覧するには、次の通り`dpkg -L`コマンドを入力します。

```{code} bash
$ dpkg -L tf1810-plc-hmi-web
/.
/etc
/etc/TwinCAT
/etc/TwinCAT/3.1
/etc/TwinCAT/3.1/Components
/etc/TwinCAT/3.1/Components/Plc
/etc/TwinCAT/3.1/Components/Plc/Tc3PlcHmiWebService
/etc/TwinCAT/3.1/Components/Plc/Tc3PlcHmiWebService/Tc3PlcHmiWebService
/etc/TwinCAT/3.1/Target
/etc/TwinCAT/3.1/Target/StartManConfig
/etc/TwinCAT/3.1/Target/StartManConfig/tf1810-plc-hmi-web.xml
/usr
/usr/share
/usr/share/doc
/usr/share/doc/tf1810-plc-hmi-web
/usr/share/doc/tf1810-plc-hmi-web/changelog.Debian.gz
/usr/share/doc/tf1810-plc-hmi-web/copyright
```

この中で実行ファイルと思われるファイルは、`/etc/TwinCAT/3.1/Components/Plc/Tc3PlcHmiWebService/Tc3PlcHmiWebService` と思われます。（その他はテキストやディレクトリ）

次にこのプロセスが動作しているかどうか、と、そのプロセスIDを調べます。

```{code} bash
$ ps aux | head -n 1
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
$ ps aux | grep Tc3PlcHmiWebService
root         479  0.0  0.1   2324  1304 ?        S    Jul28   0:00 /bin/sh -c /etc/TwinCAT/3.1/Components/Plc/Tc3PlcHmiWebService/Tc3PlcHmiWebService -umRuntime=ux:/run/ams/tcsyssrv.ams.sock:32784
root         480  0.0  0.5 672364  5136 ?        Sl   Jul28   0:55 /etc/TwinCAT/3.1/Components/Plc/Tc3PlcHmiWebService/Tc3PlcHmiWebService -umRuntime=ux:/run/ams/tcsyssrv.ams.sock:32784
Adminis+   27762  0.0  0.1   3084  1356 pts/0    S+   02:46   0:00 grep Tc3PlcHmiWebService
```

root権限で実行されているのが非常に気になりますがプロセスIDは480であることがわかります。このプロセスが開いているファイルを一覧してみましょう。これを調べるコマンド `lsof` (LiSt Open Fileの略) がありますが、初期状態ではインストールされていませんのでインストールします。

```{code} bash
$ sudo apt install lsof
```

さっそく、このコマンドを使ってPID 480のプログラムが開いている全てのファイルを一覧してみましょう。

```{code}
$ sudo lsof -p 480
COMMAND   PID USER   FD      TYPE             DEVICE SIZE/OFF  NODE NAME
Tc3PlcHmi 480 root  cwd       DIR               0,28      122   256 /
Tc3PlcHmi 480 root  rtd       DIR               0,28      122   256 /
Tc3PlcHmi 480 root  txt       REG               0,28  1053688 27395 /etc/TwinCAT/3.1/Components/Plc/Tc3PlcHmiWebService/Tc3PlcHmiWebService
Tc3PlcHmi 480 root  mem       REG               0,27          27395 /etc/TwinCAT/3.1/Components/Plc/Tc3PlcHmiWebService/Tc3PlcHmiWebService (path dev=0,28)
Tc3PlcHmi 480 root  mem       REG               0,27           3271 /usr/lib/aarch64-linux-gnu/libmd.so.0.0.5 (path dev=0,28)
Tc3PlcHmi 480 root  mem       REG               0,27           3219 /usr/lib/aarch64-linux-gnu/libbsd.so.0.11.7 (path dev=0,28)
Tc3PlcHmi 480 root  mem       REG               0,27          19099 /usr/lib/aarch64-linux-gnu/libc.so.6 (path dev=0,28)
Tc3PlcHmi 480 root  mem       REG               0,27          19037 /usr/lib/aarch64-linux-gnu/libgcc_s.so.1 (path dev=0,28)
Tc3PlcHmi 480 root  mem       REG               0,27          19102 /usr/lib/aarch64-linux-gnu/libm.so.6 (path dev=0,28)
Tc3PlcHmi 480 root  mem       REG               0,27           4394 /usr/lib/llvm-14/lib/libc++abi.so.1.0 (path dev=0,28)
Tc3PlcHmi 480 root  mem       REG               0,27           4395 /usr/lib/llvm-14/lib/libunwind.so.1.0 (path dev=0,28)
Tc3PlcHmi 480 root  mem       REG               0,27           4393 /usr/lib/llvm-14/lib/libc++.so.1.0 (path dev=0,28)
Tc3PlcHmi 480 root  mem       REG               0,27          27231 /usr/lib/libTcSystemUm.so (path dev=0,28)
Tc3PlcHmi 480 root  mem       REG               0,27          27135 /usr/lib/libTcAdsDll.so (path dev=0,28)
Tc3PlcHmi 480 root  mem       REG               0,27           3328 /usr/lib/aarch64-linux-gnu/libuuid.so.1.3.0 (path dev=0,28)
Tc3PlcHmi 480 root  mem       REG               0,27          19096 /usr/lib/aarch64-linux-gnu/ld-linux-aarch64.so.1 (path dev=0,28)
Tc3PlcHmi 480 root    0r      CHR                1,3      0t0     4 /dev/null
Tc3PlcHmi 480 root    1u     unix 0x000000000058bd30      0t0  5565 type=STREAM (CONNECTED)
Tc3PlcHmi 480 root    2u     unix 0x000000000058bd30      0t0  5565 type=STREAM (CONNECTED)
Tc3PlcHmi 480 root    3u     unix 0x000000004619dfeb      0t0  5722 type=STREAM (CONNECTED)
Tc3PlcHmi 480 root    4u     unix 0x00000000f3c5e3ee      0t0  5725 type=STREAM (CONNECTED)
Tc3PlcHmi 480 root    5u  a_inode               0,15        0    32 [eventfd:0]
Tc3PlcHmi 480 root    6u  a_inode               0,15        0    32 [eventpoll:5,7,8]
Tc3PlcHmi 480 root    7u  a_inode               0,15        0    32 [timerfd]
Tc3PlcHmi 480 root    8u     IPv4               5728      0t0   TCP *:42341 (LISTEN)
```

さて、もう少し絞りこんで、開いているファイルのうち、ソケット待ち受け（LISTEN）しているものだけを抽出します。

```{code}
$ sudo lsof -p 480 | grep LISTEN
Tc3PlcHmi 480 root    8u     IPv4               5728      0t0   TCP *:42341 (LISTEN)
```

この通り、 **42341** ポートで待ち受けていることがわかります。

次に、このポートが外部からアクセスできるようにするにはファイヤウォールで受信を許可する必要があります。Linuxにおけるファイヤウォールは、 `nftables` と呼ばれています。設定は、`/etc/nftables.conf.d/` 以下に個々に`.conf` ファイルを作成し、ポートの許可、禁止設定を行います。

既に、次の通りポートが許可された設定になっています。

00-basic.conf
    : IPv6における ping の許可や、localhost に対する全てのアクセス、SSHポート22の外部からのアクセスが許可されています。

50-ipc-diagnostics.conf
    : ベータ版では未だ未実装ですが、デバイスマネージャのWEBサービスがSSL-http （ポート443）で提供される予定なので、443ポートが許可されています。

50-tcsystemservice.conf
    : XAEとの接続に使うADSポート（TCP 8016, UDP 48899）を許可しています。

以上に加えて、次のファイルを作成します。

```{code-block} nginx
:caption: 99-plchmiweb.conf
table inet filter {
  chain input {
    # accept IPC Diagnostics
    tcp dport 42341 accept
  }
}
```

さて、これからも未来永劫、42341ポートを使い続けるには幾つかの問題が生じます。
設定ファイルを保存したら一度IPCを再起動してください。

以上により、URL `http://192.168.3.45:42341/Tc3PlcHmiWeb/Port_851/Visu/webvisu.htm` にて外部からPLC HMI Webにアクセスすることができるようになりました。



また、tf1810パッケージに連動してインストールされる **依存パッケージ** は、次のコマンドで一覧できます。

```{code}
$ sudo apt-cache depends tf1810-plc-hmi-web
tf1810-plc-hmi-web
  Depends: libuuid1
  Depends: tc31-xar-um
```

