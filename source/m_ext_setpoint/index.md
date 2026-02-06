# 外部セットポイント

TwinCATのNC/PT(ソフトウェアモーション)ではPLCライブラリで提供されている様々なFBを使って任意の加減速にて位置決め動作を実装できます。外部セットポイントはNC/PTPで補間周期毎に生成されるセットポイント(角度、速度、加速度、トルクオフセット)に対してPLCから介入してセットポイントを補正できる機能です。

PLCでは以下のTc2_MC2ライブラリへ含まれているFBを使います。

1. MC_ExtSetpointGenEnable
    : 外部セットポイントモードの有効化。


2. MC_ExtSetpointGenDisable
    : 外部セットポイントモードの無効化。

3. MC_ExtSetpointGenFeed
    : 外部セットポイント値の代入

4. MC_ExtSetpointGenFeedTorqueOffset
    : 外部セットポイント値の代入＋トルクオフセット


```{toctree}
:caption: 実装手順
axis_setting.md
task_setting.md
plc_program.md
```