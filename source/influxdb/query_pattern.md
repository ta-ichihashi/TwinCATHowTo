# さまざまなクエリパターン

## アラームやイベントの発生期間を調べる

イベントのタイトルが`text`フィールドに、その変化後の状態がboolean型で`status`フィールドに記録される`EventLogger`メジャメントをクエリする例です。次の手順でデータ加工を行います。

1. pivotにより、_fieldに記載されたフィールド名毎に列を分けた表に変換します。
2. イベント種類である`text`毎にグループ化します。
3. `events.duration`によりtrue/false間それぞれの間隔を秒数で計算し、`duration`列に出力します。

```{note}
events.durationについては以下をご参照ください。unitを変更することでより精度の高い間隔時間を計算することができます。

[https://docs.influxdata.com/flux/v0/stdlib/contrib/tomhollingworth/events/duration/](https://docs.influxdata.com/flux/v0/stdlib/contrib/tomhollingworth/events/duration/)
```

これにより、イベントの発生時刻、解消時刻と、その間隔が一覧される表が出力されます。

``` flux
import "array"
import "contrib/tomhollingworth/events"
from(bucket: "machine_monitoring")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "EventLogger")
  |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
  |> group(columns: ["text"])
  |> events.duration(unit: 1s)
  |> yield(name: "mean")
```

クエリにより得られたデータをCSVに出力した結果例は以下の通りです。

```{csv-table}
:header: 
#group,false,false,false,false,false,false,false,false,false,false,false,false,true,false
#datatype,string,long,dateTime:RFC3339,dateTime:RFC3339,dateTime:RFC3339,string,string,string,string,string,long,boolean,string,long
#default,mean,,,,,,,,,,,,,
,result,table,_start,_stop,_time,_measurement,machine_id,module_name,uuid,event_id,severity,status,text,duration
,,0,2023-11-29T21:00:00Z,2023-11-30T09:01:00Z,2023-11-29T23:35:34.911Z,EventLogger,Roll Dice demo,Event,11881C9C-6ABE-4B99-86DD-C74B4FE79496,1,3,true,!! EMO Stop !!,667
,,0,2023-11-29T21:00:00Z,2023-11-30T09:01:00Z,2023-11-29T23:46:42.498Z,EventLogger,Roll Dice demo,Event,11881C9C-6ABE-4B99-86DD-C74B4FE79496,1,3,false,!! EMO Stop !!,4351
,,0,2023-11-29T21:00:00Z,2023-11-30T09:01:00Z,2023-11-30T00:59:13.723Z,EventLogger,Roll Dice demo,Event,11881C9C-6ABE-4B99-86DD-C74B4FE79496,1,3,true,!! EMO Stop !!,17
,,0,2023-11-29T21:00:00Z,2023-11-30T09:01:00Z,2023-11-30T00:59:31.427Z,EventLogger,Roll Dice demo,Event,11881C9C-6ABE-4B99-86DD-C74B4FE79496,1,3,false,!! EMO Stop !!,384
,,0,2023-11-29T21:00:00Z,2023-11-30T09:01:00Z,2023-11-30T01:05:55.983Z,EventLogger,Roll Dice demo,Event,11881C9C-6ABE-4B99-86DD-C74B4FE79496,1,3,true,!! EMO Stop !!,6
```
