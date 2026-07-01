# 導入

まずは、TwinCAT 3 CNCで軸を動作させるためのプロジェクトの設定を行います。

## CNCPLCBaseの追加

配布されたCNCPLCBaseのPLCプロジェクトを追加します。

```{figure} assets/00_introduction_001.png
:name: figure_cncplcbase_add1
CNCPLCBaseの追加 (1)
```

```{figure} assets/00_introduction_002.png
:name: figure_cncplcbase_add2
CNCPLCBaseの追加 (2)
```

## CNCの追加

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

今回は、XYZの直交3軸+主軸の計4軸を設定するため、4軸追加します。

```{figure} assets/00_introduction_006.png
:name: figure_axis_add2
軸の追加 (2)
```

追加した軸に、それぞれ名前を付けます。

```{figure} assets/00_introduction_007.png
:name: figure_axis_name
軸の名前付け
```

補間する軸の系統(チャンネル)を追加します。

```{figure} assets/00_introduction_008.png
:name: figure_channel_add1
チャンネルの追加 (1)
```

```{figure} assets/00_introduction_009.png
:name: figure_channel_add2
チャンネルの追加 (2)
```

各軸をチャンネルに割り当てます。

````{figure} assets/00_introduction_010.png
:name: figure_channel_feed
チャンネルの設定 (feed)
````

スピンドル軸は、"Spindle"にチェックを入れます。

````{figure} assets/00_introduction_011.png
:name: figure_channel_spindle
チャンネルの設定 (spindle)
````

