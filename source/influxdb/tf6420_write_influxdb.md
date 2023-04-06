## IPCのパフォーマンスデータをデータベースへ記録するPLCプログラムサンプル

```{admonition} 前提条件
事前にTF6420をインストールして、ConfiguratorにてinfluxDBとの接続設定を行う必要があります。
```

influxDBへ登録するデータ構造体をDUTへ登録します。タグとフィールドを個別に定義し、タグを継承した構造体をお使い頂くことで、全てのデータセットで共通したタグキーの定義を強制させることができます。

タグ構造体
```pascal
TYPE DataTag:
STRUCT
    {attribute 'TagName' := 'machine_id'}
    machine_id : STRING(255);

    {attribute 'TagName' := 'data_type_id'}
    data_type_id : STRING(255);
END_STRUCT
END_TYPE
```

フィールド構造体
```pascal
TYPE PerformanceData EXTENDS DataTag:
STRUCT
    {attribute 'FieldName' := 'plc_task_time'}
    task_time: UDINT;
    {attribute 'FieldName' := 'cpu_usage'}
    cpu_usage: UDINT;
    {attribute 'FieldName' := 'latency'}
    latency: UDINT;
    {attribute 'FieldName' := 'max_latency'}
    max_latency: UDINT;
    {attribute 'FieldName' := 'exceed_counter'}
    exceed_counter: UDINT;
    {attribute 'FieldName' := 'ec_lost_frames'}
    ec_lost_frames: UDINT;
    {attribute 'FieldName' := 'ec_frame_rate'}
    ec_frame_rate: LREAL;
    {attribute 'FieldName' := 'ec_lost_q_frame'}
    ec_lost_q_frames: UDINT;
    {attribute 'FieldName' := 'ec_q_frame_rate'}
    ec_q_frame_rate: LREAL;
END_STRUCT
END_TYPE
```

また、influxDBとのアクセス状態をEnum型の定数で定義します。

```pascal
{attribute 'qualified_only'}
{attribute 'strict'}
TYPE E_DbLogState :
(
    idle := 0,
    init,
    writing,
    error
);
END_TYPE
```

メインプログラムです。100サイクル( `RECORD_DATA_SEGMENT_SIZE` )分のデータをまとめて記録するため配列を作成し、2つ( `RECORD_DATA_SEGMENT_NUM` )の配列をバッファとして交互に記録しながらinfluxDBへ書き込みを行うプログラムです。

PerformanceData構造体型のバッファ配列を上記の2つのセグメントに分け、連続的に交互に記録しつつ、セグメントの最終要素への記録が終了すると、TF6420を通じてinfluxDBへ100サイクル分のデータを追加（インサート）しています。

```{admonition} influxDBへの書き込み時間が不安定な場合

サーバのパフォーマンスや、通信経路の問題でinfluxDBへの書き込みに時間がかかる場合、書き込みにおいてbErrorが応答される可能性があります。この場合バッファ数を増やして対処してください。
```


```{admonition} 警告：タグのバリエーションにご注意ください
:class: warning

`DataTag` 構造体で定義する要素の値は、一般的なデータベースシステムにおけるインデックスに該当します。influxDBは時刻に加えてこのこのタグを組合せて高速に検索できる仕様となっています。
また、influxDBの特性として、タグの値の種類が増えた状態[^high-cardinality]のbucketに対して行われるデータ検索時に特に負荷が高くなる傾向があり、より多くのCPUリソースを消費します。タグに設定するデータのバリエーションは、時間とともに変化せず、なるべく必要最小限となるようなデータベース設計としていただくよう、ご注意ください。

```

[^high-cardinality]: この状態を「カーディナリティが高い」といいます。

```pascal
PROGRAM MAIN

VAR CONSTANT
	RECORD_DATA_SEGMENT_SIZE : UDINT := 100;
	RECORD_DATA_SEGMENT_NUM: UDINT := 2;
	RECORD_DATA_MAX_INDEX: UDINT := RECORD_DATA_SEGMENT_SIZE * RECORD_DATA_SEGMENT_NUM - 1;
	TARGET_DBID: UDINT := 1;
END_VAR

VAR
	fb_PLCTaskMeasurement: PLCTaskMeasurement;
	
	// PLC System parameters
     fbGetCurTaskIdx  : GETCURTASKINDEX;
     nCycleTime       : UDINT;
	 
	 
	// DataBase
	
	RecordData:	ARRAY [0..RECORD_DATA_MAX_INDEX] OF PerformanceData;
	current_segment: UDINT := 0;
	next_last_index: UDINT := 0;
	State: E_DbLogState	:= E_DbLogState.init;
	bWriting: BOOL; // Set this bool fla to write the data once into the InfluxDB
	dbid: UDINT := 1; // Handle to the configured database
	QueryOption_TSDB_Insert : T_QueryOptionTimeSeriesDB_Insert; // defines detailed Queryparameter
    fbNoSQLQueryBuilder_TimeSeriesDB : FB_NoSQLQueryBuilder_TimeSeriesDB; // defines database type specific api
    fbNoSqlQueryEvt : FB_NoSQLQueryEvt(sNetID := '', tTimeout := T#15S); // functionblock to execute queries
       
    // error handling helper values
    TcResult: Tc3_Database.I_TcMessage;
    bError: BOOL;
    sErrorMessage: STRING(255);

	i:UDINT := 0;
	
	test_timer :TON;
	j:UDINT := 0;
	target: UDINT := 0;
	test_var:ULINT;
	
	buttons: ARRAY [0..3] OF SwitchLamp;
	k:	UINT;
	l: UINT;
	
END_VAR


// Get ipc data.
fb_PLCTaskMeasurement(ec_master_netid := '169.254.55.71.4.1');

// Proceed database records

IF i > RECORD_DATA_MAX_INDEX THEN
	i := 0;
END_IF

RecordData[i].machine_id := 'machine-1';
RecordData[i].data_type_id := 'task_info';
RecordData[i].task_time := fb_PLCTaskMeasurement.total_task_time;
RecordData[i].cpu_usage := fb_PLCTaskMeasurement.cpu_usage;
RecordData[i].latency := fb_PLCTaskMeasurement.latency;
RecordData[i].max_latency := fb_PLCTaskMeasurement.max_latency;
RecordData[i].exceed_counter := fb_PLCTaskMeasurement.exceed_counter;
RecordData[i].ec_frame_rate := fb_PLCTaskMeasurement.ec_frame_rate;
RecordData[i].ec_q_frame_rate := fb_PLCTaskMeasurement.ec_q_frame_rate;
RecordData[i].ec_lost_frames := fb_PLCTaskMeasurement.ec_lost_frames;
RecordData[i].ec_lost_q_frames := fb_PLCTaskMeasurement.ec_lost_q_frames;

IF next_last_index = 0 THEN
	next_last_index := RECORD_DATA_SEGMENT_SIZE * current_segment + RECORD_DATA_SEGMENT_SIZE - 1;
	State := E_DbLogState.idle;
END_IF


IF next_last_index = i THEN
	// Data set
	fbNoSQLQueryBuilder_TimeSeriesDB.pQueryOptions := ADR(QueryOption_TSDB_Insert);
	fbNoSQLQueryBuilder_TimeSeriesDB.cbQueryOptions := SIZEOF(QueryOption_TSDB_Insert);    
	QueryOption_TSDB_Insert.sTableName := 'PerformanceData';
	QueryOption_TSDB_Insert.sDataType := 'PerformanceData';
	QueryOption_TSDB_Insert.pSymbol := ADR(RecordData[current_segment * RECORD_DATA_SEGMENT_SIZE]);
	QueryOption_TSDB_Insert.cbSymbol := RECORD_DATA_SEGMENT_SIZE * SIZEOF(RecordData[i]);
	QueryOption_TSDB_Insert.nDataCount := RECORD_DATA_SEGMENT_SIZE;
	QueryOption_TSDB_Insert.nStartTimestamp := F_GetSystemTime();
	
	// get cycle time
	fbGetCurTaskIdx();
	nCycleTime := _TaskInfo[fbGetCurTaskIdx.index].CycleTime;
	
	QueryOption_TSDB_Insert.nCycleTime := nCycleTime; // (in 100 ns)
	State := E_DbLogState.writing;
	IF current_segment < RECORD_DATA_SEGMENT_NUM - 1 THEN
		current_segment := current_segment + 1;
	ELSE
		current_segment := 0;
	END_IF
	next_last_index := RECORD_DATA_SEGMENT_SIZE * current_segment + RECORD_DATA_SEGMENT_SIZE - 1;
END_IF

i := i + 1;

CASE State OF

	E_DbLogState.writing:

		IF fbNoSqlQueryEvt.Execute(TARGET_DBID, fbNoSQLQueryBuilder_TimeSeriesDB) THEN
			IF fbNoSqlQueryEvt.bError THEN
				TcResult := fbNoSqlQueryEvt.ipTcResult;                
				State := E_DbLogState.error;
				bError := FALSE;
			ELSE
				State := E_DbLogState.idle;
			END_IF
		END_IF

	E_DbLogState.error:
	
		IF TcResult.RequestEventText(1033, sErrorMessage, SIZEOF(sErrorMessage)) THEN
            TcResult.Send(F_GetSystemTime());
            State := E_DbLogState.idle;
            bError := TRUE;
        END_IF
END_CASE

// Add PLC calculation stress step by step.
test_timer(IN := NOT test_timer.Q, PT := T#60S);
IF test_timer.Q THEN
	target := target + 1000;
END_IF

FOR j := 0 TO target DO
	test_var := test_var + 1;
END_FOR

IF fb_PLCTaskMeasurement.cpu_usage > 70 THEN
	target := 0;
END_IF

IF k > 3 THEN
	k := 0;
END_IF

FOR l := 0 TO 3 DO
	IF k = l THEN
		buttons[l].lamp := TRUE;
	ELSE
		buttons[l].lamp := FALSE;
	END_IF
END_FOR

k := k + 1;
```

## Chronograf による可視化

influxDBには、 Chronograf と呼ばれる可視化ソフトが付属しています。これを用いて次図のようなダッシュボードを簡単に構築することができます。

ここでは前章に掲載した60秒毎に1000回づつループ回数を増やしてCPU負荷を増やすプログラムを実行した
様子を記録したデータを表示しています。

この結果、CPU使用率とExceedカウンタの値のヒストリを並べたところ、52 $\%$ のCPU使用率となった辺りからExceedカウンタが上がり始めている事がわかります。

![](2023-02-19-19-33-21.png)

なおこのデータは、C6025において、BaseTime（1tick）を 1$ms$ とし、サイクルタイムを1tick （$=1ms$）に設定したPLCタスクをCore2（0から数えて）にWindowsと共用で80%の占有率で割り当てた際の計測データです。PLC Cycle timeの設定を遵守できない要因はCPU負荷率だけとは限らないため、ここに示す解析例はあくまでも一例としてご理解願います。
