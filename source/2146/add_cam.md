# Cam 設定手順

## 前提

TE1510 : Cam Design Tool
Cam のデータを保存する場合に使用する。

## Cam の導入

### NC Task を追加する

1. `MOTION > Add New Item...` を選択する。

    ![NCTaskの追加](assets/add_nc_task.png){w=400px align=center} 

2. 目的の `NCTask` を作成する。

    ![NcTask追加ダイアログ](assets/window_add_nc_task.png){w=400px align=center} 

### Axis を追加する

1. `Axes > Add New Item...` を選択する。

    ![Axisの追加](assets/add_axis.png){w=400px align=center} 

2. `Master` と `Slave` 用に 2 軸 Continuous Axis を追加する。

    ![Axis追加ダイアログ](assets/window_add_axis.png){w=400px align=center} 

### Master を追加する

1. `Tables > Add New Item...` を選択する。

    ![Masterの追加](assets/add_master.png){w=400px align=center} 

2. `Motion Diagram` で `Master` を追加する。

    ![Master追加ダイアログ](assets/window_add_master.png){w=400px align=center} 

### Slave を追加する


1. `Master > Add New Item...` を選択する。

    ![Slaveの追加](assets/add_slave.png){w=400px align=center} 

2. `Slave` を追加する。

    ![Slave追加ダイアログ](assets/window_add_slave.png){w=400px align=center} 

## Cam の作成

### Motion の作成

1. `Slave` を選択します。

    ![Slaveの選択](assets/select_slave.png){w=200px align=center} 


    ```{figure} assets/window_cam_create.png
    :width: 400px
    :align: center
        
    ポイントの情報画面(上部)
    ```

    ```{figure} assets/window_cam_create2.png
    :width: 400px
    :align: center
        
    プロファイル画面(下部)
    ```


2. Insert Point を選択します。

    ![InsertPoint選択](assets/select_insert_point.png){align=center} 

3. 下部にポイントを作る。

    ![Pointの追加](assets/add_point.png){align=center} 

4. ポイントができると上部にポイントのデータが自動生成されます。

    ![Point追加上部](assets/add_point_upper.png){align=center} 

5. ポイントを 2 つ追加する。

    ![Pointの追加2](assets/add_point2.png){align=center} 

6. 上部のデータも自動追加されます。

    ![Point追加上部2](assets/add_point_upper2.png){align=center} 

### グラフの形状を変える

1. 上部の Fuction でグラフの形状を変更できます。

    ![Function](assets/Function.png){align=center} 

2. Function に合わせてグラフが変化します。

    ![Functionの結果](assets/result_function.png){align=center} 
