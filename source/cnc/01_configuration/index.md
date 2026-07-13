# 設定

設計した機械を制御するために適したCNCの設定を行う必要があります。  
本項では、ケース別に合わせたCNCの様々な設定方法を紹介します。  

## 回転軸の設定

作成した軸が回転軸であることを設定します。  
(「軸」 -> 「Configuration」タブ -> 「Feed Axis」のチェックを外す)

```{figure} assets/00_configuration_001.png
:name: figure_indexaxis_config
回転軸の設定
```

パラメータで回転軸であることの設定として、回転軸であること(P-AXIS-00018)、0~360°内で動作可能なモジュロ軸であること(P-AXIS-00015)を設定します。  
(「軸」 -> 「Param List」タブ -> 「P-AXIS-00018」=2, P-AXIS-00015」=0x4)  

```{tip}
可動範囲が制限されている場合や非モジュロ軸として扱いたい場合には、P-AXIS-00015」=0x1を設定してください。
```

```{figure} assets/00_configuration_002.png
:name: figure_indexaxis_param
回転軸のパラメータ
```
