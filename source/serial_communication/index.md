# シリアル通信

USBやシリアルポートといったハードウェアは、TF6340をお使いいただくことでPCのCOMポートにPLCから直接アクセスすることが可能です。

## シリアルポートデバイスの扱いとライブラリ準備

TwinCATでシリアル通信を行うには、次のように3つの方式のデバイスアクセスが可能です。（[参考InfoSys](https://infosys.beckhoff.com/content/1033/tf6340_tc3_serial_communication/84957579.html?id=826160511792033093)
）

![](https://infosys.beckhoff.com/content/1033/tf6340_tc3_serial_communication/Images/png/85954315__en-US__Web.png){align=center}

PC COMポート
    : OS側で容易されたシリアルデバイスにアクセスすることができます。

ELターミナル
    : EL60xxなどのバスターミナルを通じてEtherCAT経由でシリアル通信する方法です。

仮想シリアルポート
    : PCIに接続されたUARTデバイスではなく、USBシリアルデバイスなど、仮想的に作成されたOS上のシリアルデバイスにアクセスすることができます。

```{tip}
仮想シリアルポートを作成するためには、 [TF6340](https://www.beckhoff.com/ja-jp/products/automation/twincat/tfxxxx-twincat-3-functions/tf6xxx-connectivity/tf6340.html?) を別途インストールする必要があります。 
```

また、別途PLCライブラリをインストールすることでPLC上のIOデバイスとして取り扱うことができ、いったん、`ComBuffer` という通信データバッファ構造体を経由することで、3つのデバイス方式が違っていても同じPLCプログラムロジックでデータ送受信を行うことができます。

## 開発手順

1. まずはTwinCATでシリアルポートの受信データにアクセスする物理的なIOを作成します。 {bdg-link-info}`参考Infosys <https://infosys.beckhoff.com/content/1033/tf6340_tc3_serial_communication/85875723.html?id=6382383804496181965>`

    この物理IOにアクセスするには、TF6340パッケージを別途インストールしていただく必要があります。パッケージマネージャからTF6340を指定してインストールを実施してください。

2. インストール後、PLCプロジェクトにライブラリを追加し {bdg-link-info}`参考Infosys <https://infosys.beckhoff.com/content/1033/tf6340_tc3_serial_communication/396591499.html?id=2081309549300242125>`、IOとのリンクを行います。

    また、本ライブラリには、物理インターフェースに合わせたIOの型が用意されています。たとえばPC上のCOMポートでしたら`PcComInData`、`PcComOutData`、EL6001などでしたら、`EL6inData22B`、`EL6outData22B`　です。この型で宣言した変数に対してIOにリンクします。

3. `SerialLineControl` ファンクションブロックの実装

    ライブラリには、`ComBuffer` という構造体型が定義され、送受信それぞれでインスタンス化します。これがデータバッファとなりIOとの中継を行います。アプリケーションは `ComBuffer` からデータを入出力します。{bdg-link-info}`参考InfoSys <https://infosys.beckhoff.com/content/1033/tf6340_tc3_serial_communication/85865099.html?id=1229754603186087237>`

    `ComBuffer` とIOとのデータ入出力制御を行うため、 `SerialLineControl` というファンクションブロックを毎サイクル常時実行します。（{bdg-link-info}`参考Infosys <https://infosys.beckhoff.com/content/1033/tf6340_tc3_serial_communication/85871115.html?id=8195232895777850580>` のSerialLineControl参照）。このコード例では、ファンクションブロックのインスタンス `fbPcComCtrl`　の引数としてIOの変数のポインタを`pComIn`、`pComOut`にセットし、データ読み書きを行う `ComBuffer` 構造体を `RxBufferPcCom` 、`TxBufferPcCom` にそれぞれセットして常時実行しています。アプリケーション側はこの`ComBuffer`の変数を使ってデータの読み書きを行います。

    ```{note}
    `SerialLineControl` を実行するタスクサイクルはシリアルポートのIOストリームデータをComBufferに移動する制御を行います。この処理サイクルが低速で、通信相手からの受信データが多くなるとシリアルポートのIOストリームデータがオーバフローとなりデータが破損する可能性があります。独立した十分速いサイクルのタスクで実行していただくことをお勧めします。
    ```

4. Send/Receiveの実装
   
   アプリケーション側からは次のリンクで示されているファンクションブロック（Send*** や、Receive***）に`ComBuffer`を監視させることで、アプリケーション側から任意のバイトやテキストデータを送ったり受信データをパースする、という流れになります。

    [ファンクションブロックの実装方法](https://infosys.beckhoff.com/content/1033/tf6340_tc3_serial_communication/85884555.html?id=3522409791184920023)
