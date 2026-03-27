(chapter_data_persistance)=
# データ永続化

TwinCAT上でのデータ永続化について説明します。データ永続化には次の要件を考慮する必要があります。

* 制御システム内の稼働中のデータを不揮発性のストレージへ保存し、制御システム再起動時にデータを再現できる機能
* 不意の電源ダウン時にバックアップ電源（UPS）を利用し、不揮発性のストレージへ確実に保存する機能

Beckhoff製のIPCに用意されているこれらの要件を満たす機能と、包括的なPLCプログラムコードをご紹介します。

```{admonition} 参考InfoSysサイト一覧
:class: note
* [1 second UPS](https://infosys.beckhoff.com/content/1033/tcplclib_tc2_sups/index.html?id=2087920595982685749)
* [UPS Software Components](https://infosys.beckhoff.com/content/1033/tcupsshellext/index.html?id=4330553038683935593)
* [WritePersistentData](https://infosys.beckhoff.com/content/1033/tcplclibutilities/11850907403.html?id=1644098846396023990)
```

```{toctree}
:caption: 目次

data_persistence
ups
plc_sample_code
```
