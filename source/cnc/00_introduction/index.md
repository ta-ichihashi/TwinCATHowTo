# 導入

TwinCAT 3 CNCで軸を動作させるためのプロジェクトの設定方法です。  
直交3軸+主軸の構成を想定したCNCの設定・操作を行います。

## CNCPLCBaseの追加

配布された「CNCPLCBase」のPLCプロジェクトを追加します。

```{figure} assets/00_introduction_001.png
:name: figure_cncplcbase_add1
CNCPLCBaseの追加 (1)
```

```{figure} assets/00_introduction_002.png
:name: figure_cncplcbase_add2
CNCPLCBaseの追加 (2)
```

CNCのライブラリを追加します。  
「References」 -> 「Library Repository」

```{figure} assets/00_introduction_024.png
:name: figure_cnc_library
CNCのライブラリ追加（1）
```

「Install」をクリック

```{figure} assets/00_introduction_025.png
:name: figure_cnc_library2
CNCのライブラリ追加（2）
```

配布された「Tc3_CNC.Library」を選択

```{figure} assets/00_introduction_026.png
:name: figure_cnc_library3
CNCのライブラリ追加（3）
```

## CNCの設定

CNCのコンフィグレーションを追加します。

```{figure} assets/00_introduction_003.png
:name: figure_cnc_add1
CNCの追加 (1)
```

```{figure} assets/00_introduction_004.png
:name: figure_cnc_add2
CNCの追加 (2)
```

CNC軸を追加します。

```{figure} assets/00_introduction_005.png
:name: figure_axis_add1
軸の追加 (1)
```

XYZの直交3軸+主軸の計4軸を設定するため、4軸追加します。

```{figure} assets/00_introduction_006.png
:name: figure_axis_add2
軸の追加 (2)
```

追加した軸に名前を付けます。

```{figure} assets/00_introduction_007.png
:name: figure_axis_name
軸の名前付け
```

補間する軸の系統(チャンネル)を「CNC」を右クリック -> 「Add New Item..」で追加します。

```{figure} assets/00_introduction_008.png
:name: figure_channel_add1
チャンネルの追加 (1)
```

```{figure} assets/00_introduction_009.png
:name: figure_channel_add2
チャンネルの追加 (2)
```

各軸にチャンネルを割り当てます。  
(「軸」 -> 「Configuration」タブ -> 「Default Channel」で「Channle_1」を選択)

```{figure} assets/00_introduction_010.png
:name: figure_channel_feed
チャンネルの設定 (feed)
```

スピンドル軸は、チャンネルを割り当てない設定になります。
(「軸」 -> 「Configuration」タブ -> 「Spindle」にチェック)

```{figure} assets/00_introduction_011.png
:name: figure_channel_spindle
チャンネルの設定 (spindle)
```

X～S軸のパラメータに、絶対位置を確立している(原点復帰が不要である)軸として、P-AXIS-00014を1に設定します。  
(「軸」 -> 「Param List」タブ -> 「P-AXIS-00014」=1)

```{figure} assets/00_introduction_012.png
:name: figure_axis_parameter_00014
軸パラメータ P-AXIS-00014 の設定
```

チャンネルのパラメータに、主軸の数(P-CHAN-00082)、軸ID(P-CHAN-00051,00036)の割り当てを行います。  
(「Channel_1」 -> 「Param List」タブ -> 「P-CHAN-00082」=1, 「P-CHAN-00051」=4, 「P-CHAN-00036」=4)

```{figure} assets/00_introduction_013.png
:name: figure_channel_parameter_spindle
チャンネルパラメータの設定 (spindle)
```

ActiveConfigurationでRunモードへ移行し、PLCを実行します。

## 標準CNC HMIの起動

配布された「TcApplication」から、「Beckhoff.App.Shell.Core.exe」を起動します。

```{figure} assets/00_introduction_014.png
:name: figure_hmi_run
標準CNC HMIの起動
```

表示されるCNC HMIの画面でCNCの状態を確認します。  
画面右上の「TwinCAT」と「PLC」がHMIと正常に接続されていると、緑色に表示されます。  
{numref}`figure_hmi_start`のように緑色でない場合は、接続設定が正しくないので、下部のボタンから「Option」から設定に進みます。

```{figure} assets/00_introduction_015.png
:name: figure_hmi_start
標準CNC HMIの起動後の画面
```

「Settings」をクリックします。

```{figure} assets/00_introduction_016.png
:name: figure_hmi_settings
標準CNC HMIの設定（1）
```

「General」 -> 「NetID」で、TwinCATのAmsNetIDを設定します。

```{figure} assets/00_introduction_017.png
:name: figure_hmi_netid
標準CNC HMIの設定（2）
```

AmsNetIdは、TwinCATの「System」 -> 「Routes」 -> 「NetId Manageement」 -> 「Target NetId」から確認できます。

```{figure} assets/00_introduction_018.png
:name: figure_hmi_netid_check
標準CNC HMIの設定（3）
```

AmsNetIdの設定が完了したら、トップの下部ボタンの「Exit」からCNC HMIを終了し、再度起動します。

```{figure} assets/00_introduction_019.png
:name: figure_hmi_exit
標準CNC HMIの設定（4）
```

前述の設定が反映されていれば、起動したCNC HMIの画面で、{numref}`figure_hmi_start2`のように「TwinCAT」と「PLC」が緑色で表示されます。  
設定が完了したら、下部のボタンから「CNC」を選択します。

```{figure} assets/00_introduction_020.png
:name: figure_hmi_start2
標準CNC HMIの起動後の画面（2）
```

それぞれの軸のサーボオン・オフは、右部のボタンの「Enable」で行います。  
  
下部のボタンから「Manual」を選択すると、手動操作が可能になります。  
上部の軸の表示パネルで、操作する軸を選択します。  
下部の操作パネルで、移動方法と移動方向を操作します。  

```{figure} assets/00_introduction_021.png
:name: figure_hmi_manual
標準CNC HMIの手動操作
```

下部のボタンから「MDI」を選択すると、数行のプログラム入力・実行が可能になります。  
プログラム入力部に、CNCのGコードを入力します。  
下部ボタンの「Start」で、入力したGコードを実行します。

```{figure} assets/00_introduction_022.png
:name: figure_hmi_mdi
標準CNC HMIのMDI操作
```

下部のボタンから「Automatic」を選択すると、プログラムの自動運転が可能になります。
フォルダから、.ncファイルを選択します。  
下部ボタンの「Start」で、選択したプログラムを実行します。

```{figure} assets/00_introduction_023.png
:name: figure_hmi_automatic
標準CNC HMIの自動運転
```

## 実軸の接続

ここまでは、シミュレーション軸の設定・動作手順を示しました。  
以降で、このシミュレーション軸に実際のモータを接続する手順を説明します。  
  
スキャンしたサーボドライブアンプが、「I/O」 -> 「Device」にあることを確認します。  
サーボドライブアンプのスキャンは、[EtherCAT Slave の Scan](scan_subdevice)をご参照ください。

```{figure} assets/00_introduction_027.png
:name: figure_io_drive
サーボドライブアンプを認識
```

サーボドライブアンプ(実軸)とシミュレーション軸をリンクします。  
(「軸」 -> 「Configuration」タブ -> 「Link to..」をクリック -> リンクするサーボドライブアンプの軸チャンネルを選択)

```{figure} assets/00_introduction_028.png
:name: figure_link_drive1
サーボドライブアンプ(実軸)とリンク（1）
```

```{figure} assets/00_introduction_029.png
:name: figure_link_drive2
サーボドライブアンプ(実軸)とリンク（2）
```

リンクすると、軸のPDOとAxis Tyepが更新されます。

```{figure} assets/00_introduction_030.png
:name: figure_link_drive3
サーボドライブアンプ(実軸)とリンク（3）
```

サーボドライブアンプに接続されているサーボモータとCNCとのスケーリングを設定します。  
  
P-AXIS-00234に、サーボモータのエンコーダにおける一回転の分解能を設定します。  
{numref}`figure_set_scaling`では、一回転の分解能を2^24=16777216[pulse/rev]で設定しています。  
P-AXIS-00233に、サーボモータの一回転における移動量(リード)を設定します。  
{numref}`figure_set_scaling`では、一回転の移動量を5[mm]で設定しています。  
(「軸」 -> 「Param List」タブ -> 「P-AXIS-00234」,「P-AXIS-00233」)

```{figure} assets/00_introduction_031.png
:name: figure_set_scaling
サーボモータのスケーリング
```

ActiveConfigurationでRunモードへ移行し、PLCを実行、CNC HMIを起動します。  
  
CNC HMIで、サーボドライブアンプとリンクした軸の位置が、スケーリングされたエンコーダ値を表示していることを確認します。  
実際に動作させて、サーボモータの一回転における移動量が正しいか確認します。  

```{figure} assets/00_introduction_032.png
:name: figure_viewer_linked_axis
リンクした軸の位置の確認
```

## 機械座標の設定

多くの場合、エンコーダ値と機械座標が一致することはありません。  
サーボモータのエンコーダ値をオフセットし、機械原点で0(もしくは任意の値)に調整することで機械座標を設定します。  
  
エンコーダ値のオフセットは、P-AXIS-00403で設定します。  
「P_cnc = P_drive + P-AXIS-00403」で機械座標(P_cnc)が決まります。  
(「軸」 -> 「Param List」タブ -> 「P-AXIS-00403」)  

```{figure} assets/00_introduction_033.png
:name: figure_encoder_offset
エンコーダ値のオフセット
```

ActiveConfigurationでRunモードへ移行し、PLCを実行、CNC HMIを起動します。  
  
CNC HMIでエンコーダ値がオフセットされていることを確認します。

```{figure} assets/00_introduction_034.png
:name: figure_set_machine_coodination
機械座標の設定
```

## ソフトリミットの設定

軸をストローク内で安全に動作させるために、ソフトリミットを設けることが有効です。  
  
ソフトリミットの下限をP-AXIS-00177で、上限をP-AXIS-00178で設定します。  
(「軸」 -> 「Param List」タブ -> 「P-AXIS-00177」,「P-AXIS-00178」)

```{figure} assets/00_introduction_035.png
:name: figure_softlimit_param
ソフトリミットの設定
```

ActiveConfigurationでRunモードへ移行し、PLCを実行、CNC HMIを起動します。  
  
ソフトリミットの上限・下限が設定されていることを確認します。  
必要であれば、実際に動かしソフトリミットが機能しているか確認します。

```{figure} assets/00_introduction_036.png
:name: figure_softlimit_display
ソフトリミットの確認
```
