# 準備・設定

## 環境設定とインストール方法

python環境の構築方法

```{code} bash
pip install pyads
```

## ADSルータ間の接続設定

{ref}`section_ads_routing` をご覧いただき、ADSルーティング設定を行ってください。pyadsのルーティング機能は次の二つの方式をサポートしています。

pyads提供のADSルータ利用
    : TwinCAT RT Linux以外のLinuxの場合、pyads内包のadslib.soによりルーティングを行います。adslib.soは pip によりビルド時にオブジェクトが生成されます。このため、`cmake` と `g++` のビルドツールのインストールがあらかじめ必要となります。TwinCAT RT Linuxであるかどうかを判定する方法は、`/usr/bin/TcSystemServiceUm` が存在するか否かで判定しています。したがって、Beckhoffのaptリポジトリを設定した上で

ネイティブADSルータの利用
    : TwinCAT RT Linuxを含む、Windows、または、TwinCAT / BSDのOSでは、ライブラリパスにBeckhoffが提供する TcAdsDll.dll または TcAdsDll.so が存在するとこのADSルータ機能を利用します。

