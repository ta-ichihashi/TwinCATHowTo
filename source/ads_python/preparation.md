# 準備・設定

## 環境設定とインストール方法

python環境の構築方法

```{code} bash
pip install 'pyads>=3.5.1'
```

```{tip}
TwinCAT RT Linuxへの対応はpyadsの[バージョン3.5.1](https://github.com/stlehmann/pyads/commit/54c6c3bd98f493c19c6559959efe94ee57945357)以降が必要です。
```

## ADSルータ間の接続設定

{ref}`section_ads_routing` をご覧いただき、ADSルーティング設定を行ってください。pyadsのルーティング機能は次の二つの方式をサポートしています。

pyads提供のADSルータ利用
    : TwinCAT RT Linux以外のLinuxの場合、pyads内包のadslib.soによりルーティングを行います。`adslib.so` は pip によりビルド時にオブジェクトが生成されます。このため、`cmake` と `g++` のビルドツールのインストールがあらかじめ必要となります。TwinCAT RT Linuxであるかどうかを判定する方法は、`/usr/bin/TcSystemServiceUm` が存在するか否かで判定しています。したがって、Beckhoffのaptリポジトリを設定した上であらかじめ以下のコマンドでビルドツールをインストールしておいてください。
      ```{code} bash
      sudo apt install cmake g++
      ```

ネイティブADSルータの利用
    : TwinCAT RT Linuxを含む、Windows、または、TwinCAT / BSDのOSでは、ライブラリパスにBeckhoffが提供する TcAdsDll.dll または TcAdsDll.so が存在するとこのADSルータ機能を利用します。

      ````{tip}
      OSがLinuxの場合、pyads提供の`adslib.so`を使うか、Beckhoff製の`TcAdsDll.so`のどちらを使うかは、次のファイルの有無で判定します。
      ```{code} bash
      /usr/bin/TcSystemManagerUm
      ```      
      このファイルがあるとTwinCATがインストールされているものとみなされ、`TcAdsDll.so`を使用します。     
      たとえばコンテナなどでADS-over-MQTTを使用してADS通信する場合はネイティブADSルータが必要ですので、{numref}`code_install_tc31xar_docker`のとおりTwinCAT `tc31-xar-um` のインストールが必要となります。(参考 : {ref}`section_tc_container_build_image`)

      ```{code-block} DockerFile
      :caption: aptでTwinCATのルータ機能をインストールするDockerFileの抜粋
      :name: code_install_tc31xar_docker

      RUN --mount=type=secret,id=apt \
          apt-get -o "Dir::Etc::netrc=/run/secrets/apt" update \
          && apt-get -o "Dir::Etc::netrc=/run/secrets/apt" install --yes \
          tc31-xar-um \
          && rm -rf /var/lib/apt/lists/*
      ```
      ````