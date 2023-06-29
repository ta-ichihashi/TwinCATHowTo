# Advanced Homing 
##一般情報
- Advanced HomingライブラリのFBを使用することでユーザーが原点復帰の仕様、流れなどを定義できる。原点復帰する際下記の信号が参照できる：
  - リミットスイッチ信号
  - 物理的なオブジェクト
  - エンコーダーのZ相パルス
- 本資料は物理的なブロックオブジェクトを検出、原点復帰実行する方法との内容
- 動作の流れ：
##システム条件
- Advanced Homingライブラリ
  - TC3.1 4024.1以降
- サポートするドライブシリーズ
  - EL72xx
  - AX8xxx
  - AX5xxx
- 位置オフセットFB
  -EL72xxはSoftware Version19以降
##環境準備
###ライブラリ追加
PLCタブのReferencesを右クリック→Add library。必要なライブラリを名称で検索、選択→OKボタン
###ActTorqueのPDO追加（AX8xxx）
###ActTorqueのPDO追加（EL72xx）
###PDOマッピング状態の確認
- 追加したPDOのマッピング状態を確認する。論理軸にリンクがない場合、手動で１度論理軸とドライブのリンク外し、リンクし直す
##Function blockについて
