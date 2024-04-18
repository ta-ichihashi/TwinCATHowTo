# PLCインスタンス作成

ここでは、軸オブジェクトであるXPlanar MC Projectとリンクを形成する ための準備を行います。

## ライブラリのインポート

XPlanarが使用するライブラリを、PLCプロジェクトの`Reference`から追加します。

```{warning}
XPlanarは非常に開発速度の速い製品です。開発時点におけるライブラリッバージョンを固定されることをお勧めします。詳しくは、{ref}`freeze_library_version`をご覧ください。
```


必須ライブラリは以下の通りです。
Tc3_PlanarMotion
  : XPlanar を動かすための機能が集約されたライブラリです。

Tc3_Physics
  : XPlanar の制御に必要な値の参照列挙体が入ったライブラリです。

Tc3_XPlanarUtility
  : TcCOM から XPlanar の情報を得たり、Visualization に反映させる機能を持つライブラリです。

Tc2_Module
  : 初期化ライブラリです。

また、次のライブラリは必要に応じて追加してください。

Tc2_MC2
  : ExternalSetPoint 機能を使用する場合に主軸として追加する場合に必要です。

## 設定

Track など機能を使用するには初期設定をプログラムで記述する必要があります。
記述は別資料を参考にしてください。
XPlanar 関係の FB には Update(Method)が実装されています。
Update は 1 周期に 1 回必ず読み込まれるように記述してください。最後に書くことを推奨する。

## 指令

- PLC Open の形式とは異なり、Method で指令を行う。
- MC_PlanarMover.〇〇 の Mover の Method で動作指令を行う。
  指令位置は PositionXYC.SetValue で定義する。
  指令条件は DynamicConstrait_PathXY.SetValue で定義する。
- Track の指令は MoveOnTrack で指令する。使用するには JoinTrack で Track 軌道に乗せておく必要がある。外す場合には LeaveTrack する。
- Track 軌道中に自由移動したい場合は ExternalSetPoint を使用する。

```
//指令の例
IF bSwitch THEN
  MC_PlanarMover.MoveToPosition(
    feedback:= MC_PlanarFeedback,
    TargetPosition:= PositionXYC,
    Constrait:= DynamicConstrait_PathXY,
    options:= ST_MoveToPositionOptions
  );
  bSwitch := FALSE;
  bBusy := TRUE;
END_IF
IF bBusy AND MC_PlanarFeedback.Done THEN
  bBusy := FALSE;
  bDone := TRUE;
ELSE
  bDone := TRUE;
END_IF

fbPlanarMover.Update();
fbPlanarFeedback.Update();
```

## Tips

- MC_PlanarFeedback で状態遷移を監視することになるので XPlanar 系 FB ごとに用意することを推奨します。
- CamInPosTrack は新機能です。今回は使わなかったが、デモで使用実績がある。
- 原点(初期位置)は Mover が 4 つ 以下なら四隅に設定すると Collision Avoidance 等で移動できないという状態を回避できる。
- PositionXYC では分割された x,y,z,a,b,c の座標を取得することができない。MoveVector で個別の座標を取得する。PositionXYC を代入して使用する。
- Z 軸の高さを設定したい場合はパラメータの zPosAtEnable に設定する。この値の高さにサーボ ON と同時浮き上がる。プログラム上で自由に変化させたい場合に MoveZ を子よゆする。
- 1 回転以上回転させたい場合は ST_MoveCOption.direction := MC_DIRECTION.NonModulo と設定する。
  初期設定の最大回転速度がかなり遅めに設定されているので要変更です。
- 動作指令の完了は座標で確認することを推奨する。また、フラグを用意して組み合わせることを推奨する。
  FeedBack の状態遷移で行うと順番待ち(Track)をしている Mover は Busy 状態で動作上停止した状態になる。
  速度で指定した場合 Mover が発振した場合、Peak の高い値が出る可能性があり誤作動の恐れがある。

## 注意

- 古いサンプルプログラムで DynamicConstrait_PathXY が DynamicConstrint になっている場合があります。バージョンによって引数に使用する型が変わる場合があるため注意する。告知もありません。
- ExternalSetPoint は衝突回避機能を使用することができないので使用する場合は注意する必要がある。
