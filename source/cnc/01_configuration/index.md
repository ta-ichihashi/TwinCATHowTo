# 設定

設計した機械を制御するために適したCNCの設定を行う必要があります。  
本項では、ケース別に合わせたCNCの様々な設定方法を紹介します。  

***

## 回転軸の設定

作成した軸が回転軸であることを設定します。  
(「軸」 -> 「Configuration」タブ -> 「Feed Axis」のチェックを外す)

```{figure} assets/01_configuration_001.png
:name: figure_indexaxis_config
回転軸の設定
```

パラメータで回転軸であることの設定として、回転軸であること([P-AXIS-00018](p-axis-00018))、0~360°内で動作可能なモジュロ軸であること([P-AXIS-00015](p-axis-00015))を設定します。  
(「軸」 -> 「Param List」タブ -> 「P-AXIS-00018」=2, P-AXIS-00015」=0x4)  

```{figure} assets/01_configuration_002.png
:name: figure_indexaxis_param
回転軸のパラメータ
```

```{tip}
可動範囲が制限されている場合や非モジュロ軸として扱いたい場合には、P-AXIS-00015」=0x1を設定してください。
```

***

## 速度・加速度設定

軸の速度・加速度に関するパラメータは、軸パラメータの「Dynamic」の項目にあります。

```{figure} assets/01_configuration_003.png
:name: figure_param_dynamic
Dynamic
```

```{csv-table} 速度・加速度パラメータ
:header: 項目, パラメータ
:name: param_velo_and_acc

軸の最大速度, [P-AXIS-00212](p-axis-00212)
早送り(G00)の速度, [P-AXIS-00209](p-axis-00209)
軸の最大加減速, [P-AXIS-00008](p-axis-00008)
エラー時の減速度, [P-AXIS-00003](p-axis-00003)
加加速度の最小時定数, [P-AXIS-00201](p-axis-00201)
曲線部の加加速度の時定数, [P-AXIS-00199](p-axis-00199)
```

マニュアル操作時の速度・加速度に関するパラメータは、軸パラメータの「Manual mode」の項目にあります。

```{figure} assets/01_configuration_004.png
:name: figure_param_manual
Manual mode
```

```{csv-table} 速度・加速度パラメータ（マニュアルモード）
:header: 項目, パラメータ
:name: param_velo_and_acc

軸の最大速度, [P-AXIS-00213](p-axis-00213)
軸の最大加減速, [P-AXIS-00009](p-axis-00009)
```

加加速度制御を有効に設定するために、[P-CHAN-00071](p-chan-00071)=1にします。

```{figure} assets/01_configuration_005.png
:name: figure_param_chan_00071
p-chan-00071
```

加加速度制御のパラメータは、「Non-linear slope」の項目にあります。

```{figure} assets/01_configuration_006.png
:name: figure_param_nonlinear-slope
Non-linear slope
```

```{csv-table} 加加速度制御パラメータ
:header: 項目, パラメータ
:name: param_jerk

G01時の最大加速度, [P-AXIS-00001](p-axis-00001)
G01時の最大減速度, [P-AXIS-00002](p-axis-00002)
G01時の加速時の立上り時定数 {numref}`figure_jerk_section`(1), [P-AXIS-00196](p-axis-00196)
G01時の加速時の立下り時定数 {numref}`figure_jerk_section`(3), [P-AXIS-00195](p-axis-00195)
G01時の減速時の立上り時定数 {numref}`figure_jerk_section`(5), [P-AXIS-00198](p-axis-00198)
G01時の減速時の立下り時定数 {numref}`figure_jerk_section`(7), [P-AXIS-00197](p-axis-00197)
G00時の最大加減速, [P-AXIS-00004](p-axis-00004)
G00時の加加速度時定数, [P-AXIS-00200](p-axis-00200)
```

```{figure} assets/01_configuration_007.png
:name: figure_jerk_section
加速度プロファイル
```
