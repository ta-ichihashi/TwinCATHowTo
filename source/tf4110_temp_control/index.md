# TF4110 Temperature Controller

## 必要ライセンス

開発環境側
  : * TC1200 (TwinCAT3 PLC)
    * TF4110 (TwinCAT3 Temperature Controller)

ランタイム環境
  : * TC1200 (TwinCAT3 PLC)
    * TF4110 (TwinCAT3 Temperature Controller)

{bdg-link-info}`参考Infosys <https://infosys.beckhoff.com/content/1033/tf4110_tc3_temperature_controller/250632331.html?id=7386734594846779259>`

## ブロック図

{bdg-link-info}`参考Infosys <https://infosys.beckhoff.com/content/1033/tf4110_tc3_temperature_controller/250638347.html?id=2903513728700600135>`

TF4110の温度コントロールFunctionBlock (FB_CTRL_TempController / FB_CTRL_TempController_DistComp)は、下図のようないくつかのFunctionBlockで構成されています。

![Block Diagram 1:](https://infosys.beckhoff.com/content/1033/tf4110_tc3_temperature_controller/Images/png/8940568843__Web.png){align=center}

```{csv-table}
FB_Selftuner,PIDパラメータを自動調整する。
FB_ControlAlgorithm,PID制御による温度調整を行う。
FB_SetpointConditioner,設定温度を制御。設定温度の急激な変化を防ぐためのランプ機能及び、低い温度で一定時間維持してから目標温度へ上げるヒーターベーキング機能を有する。
FB_ControlValueConditioner,制御出力（PWM・アナログ信号）を適切な範囲内に調整する。
FB_Alarming,異常検知とエラー通知を行う。
```

温度コントローラであるTF4110の温度コントローラ `FB_CTRL_TempController` を用いた設備の立ち上げ手順、及びプログラムの実装について記述します。

### コントローラの立ち上げ手順

TF4110の `FB_CTRL_TempController` を用いた、設備の段階的な立ち上げについて記述します。

{bdg-link-info}`参考Infosys <https://infosys.beckhoff.com/content/1033/tf4110_tc3_temperature_controller/250636939.html?id=2903897965104742967>`

1. TwinCATの開発環境（XAE）のPLCプロジェクトに、以下のライブラリを追加します。

   - Tc2_TempController

   - Tc2_ControllerToolbox\
     このライブラリのデータ型をFunctionBlock `FB_CTRL_TempController` で定義する為に必要

1. FB_CTRL_TempController（以下、「コントローラ」と呼ぶ）をプログラムに実装
   
   制御対象のモデルや制御方法に合わせて、付録に示した{ref}`section_st_ctrl_tempcontrolparameter` を適切に設定した構造体変数を用意します。これをロードした`FB_CTRL_TempController`インスタンスを実装します。この実装では、次ステップの 試運転 に示すチューニングステップを含めたマシンのふるまいを定義する必要があります。

3. 試運転

   試運転では制御するヒーター機器の他に、熱電対からの計測温度をコントローラに入力します。

  1. チューニング
  
     コントローラの制御モード(eCtrlMode)をチューニングモード(eCTRL_MODE_TUNE)に設定してから実行することで、目標設定温度の80%までの温調制御をおこない、最適なPIDパラメータを算出します（セルフチューニング）。

  2. 試運転
  
     チューニングしたパラメータを基に試運転を行います。


  試運転に必要なチューニング方法と、サンプルコードを以下のページで紹介します。

  ```{toctree}
  self_tuning
  ```

## 付録

(section_fb_ctrl_tempcontroller_parameter)=
### FB_CTRL_TempControllerのパラメータ

{bdg-link-info}`参考Infosys <https://infosys.beckhoff.com/content/1033/tf4110_tc3_temperature_controller/250647307.html?id=6554319289930271976>`


#### VAR_INPUT

```{list-table}
:header-rows: 1 

* - パラメータ
  - 型
  - 説明
* - eCtrlMode
  - [E_CTRL_MODE](https://infosys.beckhoff.com/content/1033/tf4100_tc3_controller_toolbox/245508619.html?id=9060504954589953283)
  - Tc2_ControllerToolboxライブラリの E_CTRL_MODE から 次のいずれかを選択。
    * eCTRL_MODE_PASSIVE
    * eCTRL_MODE_ACTIVE
    * eCTRL_MODE_TUNE
* - SelSetpoint
  - BOOL
  - =FALSE：通常温度(fW1)を設定\
    =TRUE：待機温度(fW2)を設定
* - fW1
  - LREAL
  - 通常温度[$^\circ\text{C}$]
* - fW2
  - LREAL
  - 待機温度 [$^\circ\text{C}$] fW2 $\lt$ fW1
* - fX
  - LREAL
  - 実際の温度[$^\circ\text{C}$]（熱電対などから測定した温度値）
* - fYManual
  - LREAL
  - 手動操作時の制御値 $[-100\%, +100\%]$
* - bOpenThermocouple
  - BOOL
  - =TRUE：熱電対を使用しない\
    通常はFALSEにし、EL3xxx, KL3xxxなどを通じて温度を計測する
* - bReverseThermocouple
  - BOOL
  - 熱電対の接続極性が逆の場合はTRUEにする
* - bBackVoltage
  - BOOL
  - 熱電対の入力電圧が高すぎる際にTRUEにする
* - bLeakage
  - BOOL
  - 熱電対の漏れ電流が発生したときにTRUEにする
* - bShortCircuit
  - BOOL
  - ヒーターエレメントで短絡が検出されたときにTRUEにする
* - bOpenCircuit
  - BOOL
  - ヒーターエレメントで断線を検出したときにTRUEにする
* - sParaControllerExternal
  - [ST_CTRL_ParaController](https://infosys.beckhoff.com/content/1033/tf4110_tc3_temperature_controller/20031015179.html?id=3150988003907548454)
  - （HMIやPLCプログラムなど）外部からパラメータを設定する場合に使用する
```

#### VAR_OUTPUT

```{csv-table}
:header: パラメータ,型,説明
fYAnalog,LREAL,温度制御のアナログ出力値  $[-100\%, +100\%]$
bPWMPPos,BOOL,加熱用のPWM信号
bPWMPNeg,BOOL,冷却用のPWM信号
bDigPos,BOOL,3ステップ制御出力のON/OFF信号 加熱用
bDigNeg,BOOL,3ステップ制御出力のON/OFF信号 冷却用
dwAlarm,DWORD,エラーや異常状態をビット単位で格納する
fMaxOverShoot,LREAL,PID制御の最大オーバーシュートが格納される[$^\circ\text{C}$]
tStartUpTime,TIME,ヒーターが初めて設定温度に達するまでの時間
eCtrlState,[E_CTRL_STATE](https://infosys.beckhoff.com/content/1033/tf4110_tc3_temperature_controller/20031731851.html?id=4469777480351482806),現在のコントローラの状態
sParaControllerInternal,[ST_CTRL_ParaController](https://infosys.beckhoff.com/content/1033/tf4110_tc3_temperature_controller/20031015179.html?id=3150988003907548454),（チューニングによって決定された）内部コントローラのパラメータを取得することが可能
bError,BOOL,エラー発生時TRUEになる
iErrorId,INT,bErroがTRUEの場合、エラーコードが格納 （ENUM ...を参照）
```

#### VAR_IN_OUT

```{csv-table}
:header: パラメータ,型,説明
sControllerParameter,[ST_CTRL_TempCtrlParameter](https://infosys.beckhoff.com/content/1033/tf4110_tc3_temperature_controller/20031014027.html?id=5859794518451108043),サンプリング時間などの一般的なパラメータをこの構造体で設定する
```

(section_st_ctrl_tempcontrolparameter)=
### ST_CTRL_TempCtrlParameterのパラメータ

`FB_CTRL_TempController` ファンクションブロックの `VER_IN_OUT` にロードする`sControllerParameter`変数の構造体について説明します。

{bdg-link-info}`参考Infosys <https://infosys.beckhoff.com/content/1033/tf4110_tc3_temperature_controller/20031014027.html?id=5859794518451108043>`

#### General Parameters

```{list-table}
:header-rows: 1

* - パラメータ
  - 型 
  - 説明
* - iMode
  - [E_CTRL_ControlMode](https://infosys.beckhoff.com/content/1033/tf4110_tc3_temperature_controller/20031723787.html?id=4310393881496635381)
  - 加熱、冷却、加冷却の制御方法を選択
* - iReactionOnFailure
  - [E_CTRL_ReactionOnFailure](https://infosys.beckhoff.com/content/1033/tf4110_tc3_temperature_controller/20031017483.html?id=3698384846456689223)
  - センサ断線やオーバーレンジなど、異常が発生したときのコントローラの動作。ヒーターの場合は停止させる設定(eCTRL_ReactionOnFailure_StopController)を推奨
* - bSelCtrlParameterSet
  - BOOL
  - オートチューニングで調整したPIDパラメータをsParaControllerExternalにセットして用いるときにTRUEにする
* - dwAlarmSup
  - DWORD
  - アラームの抑制を行う場合、該当アラームビットをマスクする
* - tCtrlCycleTime
  - TIME
  - コントローラ演算が行われるサンプリング周期。一般的に、制御対象の時定数の1/10以下に設定することが推奨される。ヒーターの場合、数十ms～数百ms程度が一般的
* - tTaskCycleTime
  - TIME
  - FBが呼ばれるタスク自体の周期。このFBが実装されているPLCのタスク周期を設定すること
```

#### Tuning Parameters

````{list-table}
:header-rows: 1

* - パラメータ
  - 型 
  - 説明
* - iTuningMode
  - [E_CTRL_TuneMode](https://infosys.beckhoff.com/content/1033/tf4110_tc3_temperature_controller/20031727243.html?id=4665835280499300939)
  - 制御対象に合わせ、チューニング方法を指定する
* - tTuneStabilisation
  - TIME
  - チューニング開始前、制御対象が安定するまでの待機時間
    ```{tip}
    熱慣性の大きい制御機器では、長めに設定しないと正しいゲインが得られない
    ```
* - fEndTunePercentHeating
  - LREAL
  - チューニング時の目標到達率[$%$]
    ```{tip}
    チューニング時に過度な温度上昇を防ぐ目的や、十分なレスポンスを確認する為に調整する
    ```
* - fYTuneHeating
  - LREAL
  - チューニング段階でヒーターをどの出力レベルで駆動するかを指定　 $[0\%, 100\%]$
* - fYStableHeating
  - LREAL
  - チューニング時の温度が安定段階になったとき、過剰なオーバーシュートを防止する
* - fScalingFactor
  - LREAL
  - オートチューニングで得たパラメータに乗算するゲイン設定
````

#### Setpoint parameters

````{list-table}
:header-rows: 1

* - パラメータ
  - 型 
  - 説明
* - fWMin
  - LREAL
  - 温度設定の下限値 [$^\circ\text{C}$]
* - fWMax
  - LREAL
  - 温度設定の上限値 [$^\circ\text{C}$]
````

#### Start up

````{list-table}
:header-rows: 1

* - パラメータ
  - 型 
  - 説明
* - bEnableSoftstart
  - BOOL
  - 加熱開始時に急激な加熱を避ける
* - bEnableRamping
  - BOOL
  - ランプ機能
    ```{tip}
    bEnableSoftstartとの違いは、こちらは「出力」ではなく「セットポイントそのもの」を段階的に変化させる
    ```
* - fStartUp
  - LREAL
  - ソフトスタートやランピング開始時の初期セットポイント[ $^\circ\text{C}$ ]
* - bStartUpRamping
  - BOOL
  - 指導段階でランプ機能をON
* - fStartUpVelPos\
    fStartUpVelNeg	
  - LREAL
  - スタートアップ時の加熱/冷却の温度変化速度[$^\circ\text{C}$/s]
* - fValuePos\
    fValueNeg
  - LREAL
  - 加熱/冷却の温度変化速度[$^\circ\text{C}/s$]
````

#### Actual value parameters

````{list-table}
:header-rows: 1

* - パラメータ
  - 型 
  - 説明
* - bFilter
  - BOOL
  - 実測値に対し一次遅れのフィルタをON
    ```{tip}
    温度センサがノイズ等で安定しない場合はTRUE
    ```
* - tFilter
  - TIME
  - 一次フィルタの時定数
````

#### Deadband parameters

````{list-table}
:header-rows: 1

* - パラメータ
  - 型 
  - 説明
* - bDeadband
  - BOOL
  - デッドバンドのON/OFF
* - fDeadband
  - LREAL
  - デッドバンドの範囲[ $^\circ\text{C}$ ]
````

#### Control value parameters

````{list-table}
:header-rows: 1

* - パラメータ
  - 型 
  - 説明
* - fYMin\
    fYMax
  - LREAL
  - PID演算結果の出力をこの範囲にクリップする[$\%$]\
    $[-100\%, +100\%]$
* - fYManual
  - LREAL
  - マニュアルモード時の出力値[$\%$]
* - fYOnFailure
  - LREAL
  - 異常時の出力値[$\%$]
    ```{tip}
    ヒーターの場合、安全性を重視するのであれば$0\%$（ヒーターOFF）に設定
    ```
* - tPWMCycleTime
  - TIME
  - PWM信号の1サイクルの時間
    ```{tip}
    制御出力の分解能と応答性に影響する
    ```
* - tPWMMinOffTime\
    tPWMMinOnTime
  - TIME
  - PWM信号の最小OFF/ON時間
* - fYThresholdOff\
    fYThresholdOn
  - LREAL
  - 3点制御（加熱/オフ/冷却）でOFF/ONに切り替える出力閾値[$\%$]
* - nCyclesForSwitchOver
  - INT
  - モード切り替え時、何サイクル掛けて移行を行うか
````

#### Controller settings

````{list-table}
:header-rows: 1

* - パラメータ
  - 型 
  - 説明
* - bEnablePreController
  - BOOL
  - プリコントローラを有効にする
* - bEnableZones
  - BOOL
  - 設定値に近づくまで開ループ特性をオンにする
* - bEnableCVFilter
  - BOOL
  - 出力に対しフィルタを適用する
* - iFilterType
  - [E_CTRL_FilterType](https://infosys.beckhoff.com/content/1033/tf4110_tc3_temperature_controller/20031728395.html?id=3764549182722085417)
  - 一次遅れフィルタ、移動平均フィルタを指定
* - iControllerType
  - [E_CTRL_ControllerType](https://infosys.beckhoff.com/content/1033/tf4110_tc3_temperature_controller/20031729547.html?id=6401950606519105954)
  - メインコントローラのアルゴリズムを指定 (PID, PI, PD, On/Off)
````

#### Min/Max temperatures

````{list-table}
:header-rows: 1

* - パラメータ
  - 型 
  - 説明
* - TempLow\
    TempLowLow
  - LREAL
  - 目標温度に対する、第1段階と第2段階の警報ゾーンの設定[ $^\circ\text{C}$ ]　マイナス側
* - TempHigh\
    TempHighHigh
  - LREAL
  - 目標温度に対する、第1段階と第2段階の警報ゾーンの設定[$^\circ\text{C}$]　プラス側
* - TempAbsoluteHigh\
    TempAbsoluteLow
  - LREAL
  - 測定値の絶対温度の上下限[$^\circ\text{C}$]
    ```{note}
    最終防御ライン
    ```
````

#### Internal tuning parameters (Expert parameters)

````{list-table}
:header-rows: 1

* - パラメータ
  - 型 
  - 説明
* - fTuneKp
  - LREAL
  - 比例ゲイン
* - fTuneTn
  - LREAL
  - 積分時間
* - fTuneTv\
    fTuneTd
  - LREAL
  - 微分フィルタに関する調整
````
