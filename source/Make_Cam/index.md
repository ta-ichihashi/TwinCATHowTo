---
aliases: 
created: 2023-06-12
updated: 2023-06-20
---
## Camを作成する

TwinCAT XAEのCam Design Toolを使用してCamを作成することができる。

TE1510 : Cam Design Tool

Cam のデータを再編集する際に必要となる。
ライセンスがない場合は新規作成は可能だが、編集することが出来ないので注意する。

### NC Task を追加する

![Image](assets/Make_Cam_01.png)

MOTION > Add New Item...を選択する。

![Image](assets/Make_Cam_02.png)

目的の NCTask を作成する。

### Axis を追加する

![Image](assets/Make_Cam_03.png)

Axes > Add New Item...を選択する。

![Image](assets/Make_Cam_04.png)

Master と Slave 用に 2 軸 Continuous Axis を追加する。

### Master を追加する

![Image](assets/Make_Cam_05.png)

Tables > Add New Item...を選択する。

![Image](assets/Make_Cam_06.png) 

Motion Diagram で Master を追加する。

### Slave を追加する

![Image](assets/Make_Cam_07.png)

Master > Add New Item...を選択する。

![Image](assets/Make_Cam_08.png)

Slave を追加する。

## Cam の作成

### Motion の作成

Slave を選択します。

![Image](assets/Make_Cam_09.png)  

上がポイントの情報画面(上部)
下がプロファイル画面(下部)

![Image](assets/Make_Cam_10.png)

![Image](assets/Make_Cam_11.png)

Insert Point を選択します。

![Image](assets/Make_Cam_12.png)

下部にポイントを作る。

![Image](assets/Make_Cam_13.png)

ポイントができると上部にポイントのデータが自動生成されます。

![Image](assets/Make_Cam_14.png)

ポイントを 2 つ追加する。

![Image](assets/Make_Cam_15.png)

上部のデータも自動追加されます。

### グラフの形状を変える

![Image](assets/Make_Cam_16.png)

上部の Fuction でグラフの形状を変更できます。

![Image](assets/Make_Cam_17.png)

Function に合わせてグラフが変化します。
