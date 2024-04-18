# Configurator 手順

## 準備

- 実機を準備する。
- 接続順番と Tile の BTN を記録する。
  - Tile の登録時に必要です。

```{admonition} 注意
:class: warning

Configurator は実機と接続してる際に実機情報と簡単にリンクさせるためのソフトウェアです。実機なしのプログラムを作成しているときは Infosys を参考に設定してください。
```

## 実機の Device を読み込む

1. I/O > Devices > Scan を選択する。  

  ![DeviceScan](assets/DeviceScan.png)

2. 注意文が出るので OK を押す。  

  ![Scan警告](assets/scan_warning.png)

3. EtherCAT 接続されたポートを選択(自動)して OK を押す。

  ![接続先の決定](assets/select_port.png)

4. Scan for boxes のダイアログが出るので、Yes を選択する。
 
  ![ScanForBoxes](assets/ScanForBoxes.png)

5. 接続されたデバイスが登録されます。  

  ![IODevice登録完了](assets/complete.png)

6. FreeRun モードにする。

## Configurator を立ち上げる

TwniCAT > XPlanar > Configurator を選択する。  
![MenuBar_Configurator](assets/MenuBar_Configurator.png)

## Parts 設定

中央グラフィックの使用するタイルをクリックする。  
![Configurator_Parts](assets/Configurator_Parts.png)

> FreeRun モードでないと Scan BTNs で Device が見つからないので注意する。

画面左上の Factory Settings から ScanBTN を選択する。  
![Parts_ScanBTN](assets/Parts_ScanBTN.png)

Tile Settings から Assign BTNs で適切な BTN を割り当てる。  
![Parts_AssignBTN](assets/Parts_AssignBTN.png)
![Parts_SelectBTN](assets/Parts_SelectBTN.png)

全て選択すると下記のようになります。
(BTN はご使用の XPlanar 固有のものになります。)  
![Parts_RegisterBTN](assets/Parts_RegisterBTN.png)

## Mover 設定

上部のボタンから使用する Mover 種類を選択する。  
タイル上に使用する Mover を置く。  
![Configurator_Mover](assets/Configurator_Mover.png)

## Real-Time 設定

![Configurator_Real-Time](assets/Configurator_Real-Time.png)

使用する Core の割り当てを入力する。  
![Real-Time_SystemSetting](assets/Real-Time_SystemSetting.png)

- Restrict CPU Count に ☑ を入れる。

  - Isolated Core に設定するため。

- Restrict CPU Count に 1 を入れる。
  - 1 以外は入れない。1 以外はタスクの自動割付がされない。

Reassign Modules を選択する。  
![Real-Time_CpuInformation](assets/Real-Time_CpuInformation.png)

Isolated CPUs の 250 µs のコアに割り当てられているか確認する。  
![Real-Time_IsolatedCore](assets/Real-Time_IsolatedCore.png)

## 設定データの出力

下記の操作にて次の処理が行われます。処理が完了するまでTwinCATのプロジェクトを閉じない様に注意してください。

* bmlファイルの出力
* TwinCATのモーション軸の生成

次の手順を実行します。

1. 上部メニューから Export を選択する。  

  ![Configurator_Menu](assets/Configurator_Menu.png)

2. 確認画面で Yes を選択する。  

  ![Export_Confirmation](assets/Export_Confirmation.png)

3. Console 画面が表示される。  

  ![Export_Console](assets/Export_Console.png)

処理が完了すると、自動的に以下のフォルダへにbmlファイルが保存されたフォルダを開いたエクスプローラが出現します。

```
C:\TwinCAT\Functions\TF5890-TC3-XPlanar-Technology\mllib_toolbox\target
```

![TagetFile](assets/TagetFile.png)

4. これらのファイル全てを選択し、ターゲットIPCの以下のフォルダへ配置してください。

```
C:\TwinCAT\3.1\Target\Config\XPlanar\bml
```

  ![BmlFile](assets/BmlFile.png)


5. TwinCAT XAE 上のプロジェクトには、SYSTEM, MOTION に自動でオブジェクトが登録されます。

  ![FinishConfiguration](assets/FinishConfiguration.png)
