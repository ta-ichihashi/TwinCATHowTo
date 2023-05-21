% TwinCAT開発におけるプログラム標準化マニュアル documentation master file, created by
%  sphinx-quickstart on Tue Feb 21 11:50:42 2023.
%   You can adapt this file completely to your liking, but it should at least
%   contain the root `toctree` directive.

# TwinCAT におけるDevOps開発環境構築

特にクラウドコンピューティングにおいては、DevOpsという概念が注目されています。例えばソフトウェアの構成管理にGithubおよびそのマージシステムを用いて開発フローをIT上で完結させます。必要なプログラムコードが集まった後は、CI/CDと呼ばれるビルド・テスト・ターゲットマシンへのデプロイまでの開発工程を自動化する仕組みが提供されます。DevOpsはこれらを包括した概念です。これにより、開発者は開発に専念する事ができ、現場ニーズに適した機能を短期間で提供することが可能となり、生産性の向上に役立ちます。

産業用の制御ソフトウェアにおいてこの仕組みを活用するには、次の課題を克服する必要があります。

* モジュール開発フェーズ
    * ライブラリ管理システムとそれを活用する開発フローの標準化
    * GitやGithubなどを使ったマージシステム
    * 単体テスト（ファンクションやファンクションブロック単体でのテスト）の自動化
* 結合・デプロイフェーズ
    * ハードウェアのシミュレーション
    * 結合テスト（負荷を含めたアプリケーションとしてのテスト）の自動化
    * 自動デプロイシステム

この章では、これらを実現する方法について説明します。

```{toctree}
:maxdepth: 2
:caption: 目次

../version_control/index.md
../library/index.md
```

