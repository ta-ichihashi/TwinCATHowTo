(chapter_shared_memory)=
# バイトストリームや共有メモリによる通信

シリアル通信などのバイトストリームや、異なるシステム間でメモリを共有して行う通信などにおいては、次の二つの点を考慮しなければなりません。

エンディアン
    : コンピュータアーキテクチャにより、ワード語長（CPUが1サイクルで処理するデータ長）におけるメモリの配列の順序が異なります。リトルエンディアンでは、最後のアドレスから順にデータが配置され、終端が最も小さなアドレスとなります。ビッグエンディアンでは、逆に最後のアドレスが最も大きなアドレスとなります。バイト配列がどちらのエンディアンを基準とするかが一致していなければ、正しい情報の受け渡しができません。

メモリアライメント
    : 共有メモリで通信を行う場合、メモリ上に配置するデータの構造は様々なサイズ、型のものが組み合わさることがあります。このような構造体データをメモリイメージのまま受け渡す場合、メモリアライメントについて考慮する必要があります。

    : メモリアライメントとは、ワード語長を跨いだデータが発生しないように空きを作って構造体データを配置する仕組みです。TwinCAT3ではデフォルトで8Byteアライメントされたメモリイメージとなります。異なるシステムや、バイトストリームの場合、このままでは正しくマッピングできなくなりますので、注意が必要です。

本節では、EtherCATでバイト配列で共有されたIOを、構造体変数にマッピングすることを例に実例を説明します。

```{toctree}
:hidden:

byte_swapping
memory_alignment
address_mapping
```
