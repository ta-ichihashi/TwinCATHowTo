# パラメータ

CNCを扱う上で、パラメータ設定は非常に重要です。  
本項では、各パラメータの機能を解説します。  

## パラメータの設定方法

パラメータは「Param List」タブで変更します。

```{figure} assets/02_parameter_001.png
:name: figure_param_axis
パラメータの設定（軸）
```

チャンネルのパラメータも同じ「Param List」タブから設定できます。  
キネマティクス、相対座標、座標オフセット(絶対座標)などのパラメータ群をタブによって切り替えます。

```{figure} assets/02_parameter_002.png
:name: figure_param_chan
パラメータの設定（チャンネル）
```

パラメータリストの基本的な使用方法を紹介します。  
{numref}`figure_param_operation`の赤枠の「Find」でパラメータ番号の検索が可能です。  
{numref}`figure_param_operation`の緑枠の「Download」でRunモード中のCNCに変更した一部のパラメータを反映させることが可能です。  
{numref}`figure_param_operation`の青枠の「Export/Import」でパラメータリストの入出力が可能です。

```{figure} assets/02_parameter_003.png
:name: figure_param_operation
パラメータリストの操作
```

ここまでの内容は「Parameter」タブからでも可能です。  
{numref}`figure_param_tab`の緑枠の「Notepad...」から、{numref}`figure_param_notepad`のようにNotepadで直接パラメータを編集することが可能です。  
ここで標準で用意されていないパラメータを追加・編集します。  
Notepadでのパラメータ編集中は、開発環境は操作できないのでご注意ください。

```{figure} assets/02_parameter_004.png
:name: figure_param_tab
パラメータタブ
```

```{figure} assets/02_parameter_005.png
:name: figure_param_notepad
パラメータ編集
```

## 軸パラメータ

各軸におけるパラメータを解説します。

***

(p-axis-00014)=
### [P-AXIS-00014](https://infosys.beckhoff.com/english.php?content=../content/1033/tf5200_axis_parameter/117772299.html&id=7287240913738401586)

CNC起動時の軸の絶対位置が有効か無効を指定する軸パラメータ
  
```{csv-table} P-AXIS-00014
:header: 値, 内容
:name: param-axis-00014

0, "デフォルト設定  
CNC起動時点で軸の実位置が無効   
「インクリメンタルエンコーダ軸」、「CNCが起動時点で機械座標を確定できない軸」が該当  
原点復帰処理が必要"
1, "CNC起動時点で軸の実位置が有効  
原点復帰は不要"
```

***

(p-axis-00234)=
### [P-AXIS-00234](https://infosys.beckhoff.com/english.php?content=../content/1033/tf5200_axis_parameter/125765771.html&id=3092732739521937372)

[P-AXIS-00233](p-axis-0233)で定義した移動量に対する総パルス数

***

(p-axis-00233)=
### [P-AXIS-00233](https://infosys.beckhoff.com/english.php?content=../content/1033/tf5200_axis_parameter/117770763.html&id=4588379831171296484)

[P-AXIS-00234](p-axis-00234)で定義した総パルス数に対する移動量

***

(p-axis-00403)=
### [P-AXIS-00403](https://infosys.beckhoff.com/english.php?content=../content/1033/tf5200_axis_parameter/117927819.html&id=6722892972436649103)

エンコーダ(ドライブ)から取得した位置をオフセットするパラメータ  
「P_cnc = P_drive + P-AXIS-00403」でCNCの機械座標(P_cnc)を定義

***

(p-axis-00177)=
### [P-AXIS-00177](https://infosys.beckhoff.com/english.php?content=../content/1033/tf5200_axis_parameter/117313035.html&id=8033121886424612323)

ソフトリミットの下限  
軸の実位置が有効であることが条件

***

(p-axis-00178)=
### [P-AXIS-00178](https://infosys.beckhoff.com/english.php?content=../content/1033/tf5200_axis_parameter/117311499.html&id=4852352789875022842)

ソフトリミットの上限  
軸の実位置が有効であることが条件

***

(p-axis-00018)=
### [P-AXIS-00018](https://infosys.beckhoff.com/english.php?content=../content/1033/tf5200_axis_parameter/117186955.html&id=3496575245767783562)

軸の直動・回転を定義するパラメータ

```{csv-table} P-AXIS-00018
:header: 値, 内容
:name: param-axis-00018

0x0001, 直線軸
0x0002, 回転軸
0x0004, スピンドル軸
```

***

(p-axis-00015)=
### [P-AXIS-00015](https://infosys.beckhoff.com/english.php?content=../content/1033/tf5200_axis_parameter/117192331.html&id=6143626661888388599)

軸の動作特性・機能属性を指定するパラメータ  
  
```{csv-table} P-AXIS-00015
:header: 値, 内容
:name: param-axis-00015

0x00000001, 非Modulo軸(直線軸)
0x00000004, Modulo軸
0x00000040, 旋削の端面方向軸
0x00000080, 旋削の長手方向軸
0x00000100, 主軸位置決め前の自動原点復帰を抑制
0x00000200, C軸変換用の軸
0x00000400, 直線座標単位を使用するModulo軸
0x00000800, PLCによる機械クランプを許可
0x00001000, 回転ワークテーブルを搭載する軸
0x00008000, 軸衝突監視
0x00010000, ガントリマスタ軸
0x00020000, ガントリスレーブ軸
0x00040000, PLC制御主軸
0x00080000, 外部位置指令の入力軸
0x00100000, エンコーダ専用軸
0x00200000, G194用の先導軸
0x00400000, 運転開始後の分解能変更を許可
0x00800000, 軸別の経路依存動特性重み付け
0x02000000, TCP軌跡長用の経路軸
0x04000000, 輪郭経路長用の経路軸
0x08000000, 経路補間用の仮想先導軸
0x10000000, エッジバンディングの加圧ローラ軸
```

:::
#### 構成
:::

P-AXIS-00015  
│  
├─ 基本動作  
│    ├─ 非Modulo  
│    └─ Modulo  
│  
└─ オプション機能  
     ├─ ガントリマスタ  
     ├─ ガントリスレーブ  
     ├─ 衝突監視  
     ├─ ロータリテーブル  
     ├─ エンコーダ軸  
     └─ その他  

***

(p-axis-00212)=
### [P-AXIS-00212](https://infosys.beckhoff.com/english.php?content=../content/1033/tf5200_axis_parameter/117640715.html&id=1779750362957551460)

***

(p-axis-00209)=
### [P-AXIS-00209](https://infosys.beckhoff.com/english.php?content=../content/1033/tf5200_axis_parameter/117631627.html&id=5422389209692171767)

***

(p-axis-00008)=
### [P-AXIS-00008](https://infosys.beckhoff.com/english.php?content=../content/1033/tf5200_axis_parameter/117642251.html&id=7369219159060421252)

***

(p-axis-00003)=
### [P-AXIS-00003](https://infosys.beckhoff.com/english.php?content=../content/1033/tf5200_axis_parameter/117643787.html&id=5065213811480140874)

***

(p-axis-00201)=
### [P-AXIS-00201](https://infosys.beckhoff.com/english.php?content=../content/1033/tf5200_axis_parameter/117645323.html&id=5004262408645091730)

***

(p-axis-00199)=
### [P-AXIS-00199](https://infosys.beckhoff.com/english.php?content=../content/1033/tf5200_axis_parameter/117646859.html&id=8803354316139842074)

***

(p-axis-00213)=
### [P-AXIS-00213](https://infosys.beckhoff.com/english.php?content=../content/1033/tf5200_axis_parameter/118150411.html&id=8397862084423760682)

***

(p-axis-00009)=
### [P-AXIS-00009](https://infosys.beckhoff.com/english.php?content=../content/1033/tf5200_axis_parameter/118151947.html&id=3240389770478077025)

***

(p-axis-00001)=
### [P-AXIS-00001](https://infosys.beckhoff.com/content/1033/tf5200_axis_parameter/117614731.html?id=212097720499606852)

***

(p-axis-00002)=
### [P-AXIS-00002](https://infosys.beckhoff.com/content/1033/tf5200_axis_parameter/117616267.html?id=763238951968738953)

***

(p-axis-00196)=
### [P-AXIS-00196](https://infosys.beckhoff.com/content/1033/tf5200_axis_parameter/117617803.html?id=4389054295584788680)

***

(p-axis-00195)=
### [P-AXIS-00195](https://infosys.beckhoff.com/content/1033/tf5200_axis_parameter/117619339.html?id=1007466434962408522)

***

(p-axis-00198)=
### [P-AXIS-00198](https://infosys.beckhoff.com/content/1033/tf5200_axis_parameter/117620875.html?id=2649523321864525789)

***

(p-axis-00197)=
### [P-AXIS-00197](https://infosys.beckhoff.com/content/1033/tf5200_axis_parameter/117622411.html?id=8064045793283888564)

***

(p-axis-00004)=
### [P-AXIS-00004](https://infosys.beckhoff.com/content/1033/tf5200_axis_parameter/117623947.html?id=9010184314467822815)

***

(p-axis-00200)=
### [P-AXIS-00200](https://infosys.beckhoff.com/content/1033/tf5200_axis_parameter/117625483.html?id=4648014058197092242)

***

## チャンネルパラメータ

各チャンネルにおけるパラメータを解説します。

***

(p-chan-00082)=
### [P-CHAN-00082](https://infosys.beckhoff.com/english.php?content=../content/1033/tf5200_channel_parameter/149143563.html&id=7339672895428656137)

チャンネルで扱うスピンドル軸の数

***

(p-chan-00051)=
### [P-CHAN-00051](https://infosys.beckhoff.com/english.php?content=../content/1033/tf5200_channel_parameter/149149707.html&id=5999017703334273912)

メインスピンドルとなる軸番号

***

(p-chan-00053)=
### [P-CHAN-00053](https://infosys.beckhoff.com/english.php?content=../content/1033/tf5200_channel_parameter/149151243.html&id=7819480764968471708)

メインスピンドルとしてNCプログラムから扱うときの名前

***

(p-chan-00007)=
### [P-CHAN-00007](https://infosys.beckhoff.com/english.php?content=../content/1033/tf5200_channel_parameter/149155851.html&id=5836675451676730391)

チャンネル内に登録する各スピンドルのデフォルト名

***

(p-chan-00036)=
### [P-CHAN-00036](https://infosys.beckhoff.com/english.php?content=../content/1033/tf5200_channel_parameter/149159051.html&id=1616390936463113186)

チャンネル内に登録した各スピンドルの軸番号

***

(p-chan-00071)=
### [P-CHAN-00071](https://infosys.beckhoff.com/english.php?content=../content/1033/tf5200_channel_parameter/149296907.html&id=7399776100798316168)

***
