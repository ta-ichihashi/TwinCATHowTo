(figure_persistent_value_with_ups)=
# 無停電電源装置（UPS）によるPERSISTENTデータの永続化

Persistent属性の変数値は、IPCの正常シャットダウン操作時にファイルへ書き出され、次の起動時にはファイルから値が再度ロードされる、いわゆる永続化されます。
しかし、不意な電源ダウン時にはファイルへ保存することができず、RUN中の活動により変動したPersistent変数の値の永続化ができません。

これを防ぐためには、UPS（無停電電源装置）を取り付け、電源供給が失われた事を検出して明示的な命令でPersistentデータをファイルへ保存する必要があります。

IPCに搭載可能なUPSには次の2タイプがあり、それぞれ実装方法が異なります。（{numref}`UPS_persistent_flow`）

[1 second UPS](https://infosys.beckhoff.com/content/1033/tcplclib_tc2_sups/index.html?id=2087920595982685749)

    : CXと呼ばれる組み込み型IPCに搭載される大容量キャパシタによる組み込み電源保持機構です。cFastメモリという特別な書き込み速度の速いストレージに変数を保持し、多くの機種でその最大容量は1Mbyteとなります。専用のファンクションブロック`FB_S_UPS_****`が用意され、RUN中は常時実行し続けることで、選択したモードにより不意の停電発生時には自動的にPERSISTENT変数の値をファイルへ永続化することができます。またPERSISTENTデータへの保存が完了したあと、`FB_NT_QuickShutdown` によりWindowsのシャットダウン処理を行う事ができます。


    : ```{admonition} FB_NT_QuickShutdown のシャットダウンについて
      :class: warning

      このFBによるシャットダウンは、アプリケーションのプロセス終了を待たずに行われるWindowsの強制シャットダウンです。稼働中のユーザアプリケーションが何等かのファイルシステムへの書き込みを実施している間にシャットダウンが行われると、最悪ファイルが破損するなどのリスクがあることをご承知おきください。次項でご紹介するUPS Software ComponentsによるWindowsシャットダウンの場合ですと、事前に30秒のアプリケーションシャットダウンの猶予時間が考慮されますのでより安全です。

      参考
        : [UPS Software Compnentsの動作仕様](https://infosys.beckhoff.com/content/1033/cu8110-0060/9317196811.html?id=8956306956757275690)

      ```


    : ```{admonition} TwinCAT/BSDやTwinCAT Real-time Linux について
      :class: tip

      この両OSが採用するZFSやBtrFSといったファイルシステムは、CoW（Copy on Write）という方式を採用しており、ファイルシステムへの書き込み命令に際していったん対象ファイルを別の領域にコピーしてからデータを書き換え、その後、メタデータを書き換え後のものに差し替える、といったプロセスを行っています。このため、もしアプリケーションがファイルシステムに対してデータを書き込みを行っている間に強制シャットダウンとなった場合においても、メタデータは書き換え前の完全な状態のファイル実体を指し示したままですので、ファイルが破損することが起こりえません。よって強制終了においてもファイル破損のリスクが存在しないより頑強なファイルシステムだと言えるでしょう。

      ただし、このようなケースでも実行中のトランザクションを最後まで実行させたい場合、やはりUPSを設置するのが良いでしょう。こうしたデータの永続性をどこまで担保させたいか、により適切なバックアップ設備をご選定ください。
      ```

[UPS Software Components（汎用UPS）](https://infosys.beckhoff.com/content/1033/tcupsshellext/index.html?id=4330553038683935593)

    : 1 second UPSの搭載が無いIPCや、Windows側のファイル破損が装置稼働に影響を与えるリスクがある場合は外付けUPSの設置が必要です。UPS Software Componentsは、この汎用UPSをWindowsでマネジメントするユーティリティソフトウェアです。UPSの残量やバッテリのみの駆動時間により自動的にWindowsシャットダウンを実施するところまで管理してくれるソフトウェアとなっています。PLCでは`FB_GetUPSStatus`によりUPSの稼働状態がモニタリングできますので、これにより `WritePersistentData` ファンクションブロックを実行し、PERSISTENT変数を永続化します。その後は、マネジメントソフトが自動的にシャットダウン処理まで行いますので、PLCからのシャットダウン処理は必要ありません。

    : 対応しているUPSはベッコフ製、APC製などがあります。ベッコフ製の場合はIPCとの間で電源線と通信線を共用するOCT（One Cable Technology）が採用されていますので、別途USBやシリアル通信ケーブルの設置が不要になります。次の通り容量別にラインナップされたコンパクトなUPSをご検討ください。
        * [CU8110-0060（0.3Wh）](https://www.beckhoff.com/ja-jp/products/ipc/embedded-pcs/accessories/cu8110-0060.html) 
        * [CU8110-0120（0.9Wh）](https://www.beckhoff.com/ja-jp/products/ipc/embedded-pcs/accessories/cu8110-0120.html?)
        * [CU8130-0120（15Wh）](https://www.beckhoff.com/ja-jp/products/ipc/embedded-pcs/accessories/cu8130-0120.html)
        * [CU8130-0240（30Wh）](https://www.beckhoff.com/ja-jp/products/ipc/embedded-pcs/accessories/cu8130-0240.html)
    

```{toctree}
:caption: 目次

install_ups_service
```