# 時系列データベース記録用PLCライブラリの使い方

実際の運用では、様々なデータモデルとそのデータの生成タイミングでデータベースに記録する必要があります。このためサンプルコードを含むプロジェクトを公開いたします。ライブラリとしてもお使いいただくことができます。

```{admonition} 公開先のGithubリポジトリ
:class: info 

以下のリポジトリにて公開しています。プルリクエストをお待ちしています。

[https://github.com/Beckhoff-JP/tc_influxdb_client](https://github.com/Beckhoff-JP/tc_influxdb_client) 

```

## クイックスタート

本プロジェクトに含まれるファンクションブロック等を用いる事で、次の手順でInfluxDBへアクセス頂く事ができます。

以下の手順で実装してください。

### DUTs へのInfludxDBへ記録するデータモデルの登録

まず、登録したいデータモデルを構造体で定義します。構造体の各要素の宣言行の上部に、次の書式で

* `{attribute 'TagName' := 'タグ名称'}`

	タグ（インデックス）となるデータ行の上部に宣言します。

* `{attribute 'FieldName' := 'フィールド名称'}`

	フィールドとなるデータ行の上部に宣言します。


下記の通り、タグとフィールドの構造体を分けて定義し、フィールド定義構造体では、タグ定義構造体を継承して定義すると良いでしょう。これにより、 Measurement 毎に共通のタグセットを定義する事ができます。

```{admonition} 警告：タグのバリエーションにご注意ください
:class: warning

`DataTag` 構造体で定義する要素は一般的なデータベースシステムにおけるインデックスに該当します。influxDBは時刻に加えてこのこのタグを組合せて高速に検索できる仕様となっています。

このタグの値のバリエーションが多くなる [^high-cardinality] と、influxDBは非常に多くのメモリを消費する事が分かっています。このため、動作が遅くなったり他のプロセスに影響を及ぼし、システムを不安定にさせる要因となります。よって、タグに設定するデータには次の要件を満たすものに対して割り当てていただくよう、十分にご注意ください。

* 見積可能な有限の種類のデータであること

	短期間に毎回異なる値がセットされるようなデータにはタグを割り当てず、フィールドに割り当ててください。
	
	リテンションポリシーのデータの保存期間において予測可能なデータの種類の数が、許容できるメモリ消費量に収まっていることが求められます。

* データの種類が増える頻度とタイミングが一定で予測可能であること

	イベントデータ等で、予測不可能なタイミングでデータ書き込みが行われ、都度その値が変化するようなものをタグとして登録すると、イベントが集中することで意図せずカーディナリティが上昇し、メモリを圧迫する恐れがあります。

```

[^high-cardinality]: この状態を「カーディナリティが高い」状態といいます。



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

フィールド構造体（サイクル記録実装例用）

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

フィールド構造体（イベントデータ記録実装例用）

```pascal
TYPE ProcessModeData EXTENDS DataTag:
STRUCT
	{attribute 'FieldName' := 'executing'}
    executing: BOOL;
	{attribute 'FieldName' := 'message'}
	message: STRING := 'ABC000';
END_STRUCT
END_TYPE

```

###  メインプログラムの作成
*
#### サイクル記録（cyclic_record）実装例

PLCの制御サイクル毎に取得できるデータを、あらかじめ用意したバッファに記録しつつ、一定のサイズのチャンクとなるまで蓄積されたら、コマンドキューを通じてデータベースに書込みコマンドを送る記録方式です。

実装方法は次の通りです。

* DUTsで定義するデータベース記録データ構造体と、バッファ制御FB（ RecordDataQueue ）はペアで定義します。
* これらのペアは、複数のデータモデルや、記録周期の違うデータを複数処理定義可能です。
* データバッファとバッファ制御FBは、データモデル毎に複数持つことができます。
* データベース書込みロジックは、これら複数のバッファの先頭データのポインタとチャンクサイズで構成されたコマンドをキューを経由して受け取り、書込み処理を行います。
* 本サンプルコードは単一のデータモデルですが、github上のサンプルコードは複数データモデルで構成されています。

```{figure} tsdb_library_feature.png
:width: 600px
:align: center
:name: figure_tsdb_library_feature

本ライブラリの機能概要
```

```{figure} cyclic_data_buffer.png
:width: 400px
:align: center
:name: figure_cyclic_data_buffer

サイクリックデータバッファの構造
```



以上を満たすプログラム実装例を次に示します。

* 宣言部

	```pascal

	PROGRAM RecordToInfluxDB

	VAR CONSTANT
		RECORD_DATA_MAX_INDEX: UDINT := 4999;	// データバッファのUPPER BOUND
		TARGET_DBID: UDINT := 1;	// TF6420に定義したInfluxDBのDBID
	END_VAR

	VAR
		// 前節で定義した構造体型（PerformanceData）型の配列（連続データを記録するバッファ）
		PerformanceDataRecordBuffer	: ARRAY [0..RECORD_DATA_MAX_INDEX] OF PerformanceData;
		// 現在のサイクルで登録するデータセット
		PerformanceDataRecordData	:PerformanceData;

		// データベース書き込みコマンドを処理するFIFOキュー
		command_queue	: CommandQueueMember;

		// ビジネスロジック用ファンクションブロック
		fbPerfromanceDataCommandBuffer	:RecordDataQueue; // バッファキュー制御ロジック
		fbInfluxDBRecorder	:RecordInfluxDB;	// データベース書込みロジック

		// おまけ。IPCの各種メトリクス（CPU占有率やメトリクス等）を収集する独自のFB
		fb_PLCTaskMeasurement: PLCTaskMeasurement;

	END_VAR
	```

* プログラム部

	まずはデータの収集とバッファへのデータセットです。
	```pascal
	// コマンドキューの生成
	command_queue.controller(aData := command_queue.buffer_index);

	// Tag Dataのセット
	PerformanceDataRecordData.machine_id := 'machine-1';  // 装置1のデータである事を示す
	PerformanceDataRecordData.job_id := 'task_info';	　// データ種別

	// Field Data のセット（IPCの各種状態を計測し、書込みデータモデルにセット）
	fb_PLCTaskMeasurement(ec_master_netid := '169.254.55.71.4.1');
	PerformanceDataRecordData.task_time := fb_PLCTaskMeasurement.total_task_time;
	PerformanceDataRecordData.cpu_usage := fb_PLCTaskMeasurement.cpu_usage;
	PerformanceDataRecordData.latency := fb_PLCTaskMeasurement.latency;
	PerformanceDataRecordData.max_latency := fb_PLCTaskMeasurement.max_latency;
	PerformanceDataRecordData.exceed_counter := fb_PLCTaskMeasurement.exceed_counter;
	PerformanceDataRecordData.ec_frame_rate := fb_PLCTaskMeasurement.ec_frame_rate;
	PerformanceDataRecordData.ec_q_frame_rate := fb_PLCTaskMeasurement.ec_q_frame_rate;
	PerformanceDataRecordData.ec_lost_frames := fb_PLCTaskMeasurement.ec_lost_frames;
	PerformanceDataRecordData.ec_lost_q_frames := fb_PLCTaskMeasurement.ec_lost_q_frames;

	// 上記までで収集したデータが PerformanceRecordData にセットされたため、
	// コマンドバッファが管理している現在記録中のindexへ書き込む。
	PerformanceDataRecordBuffer[fbPerfromanceDataCommandBuffer.index] := PerformanceDataRecordData;
	```

	続いてバッファ制御部（一定量蓄積したら書込みキューに送る処理）の実装です。

	```pascal
	// 書き込んだデータをジェネリクス型（T_Arg）に変換してセットする。
	fbPerfromanceDataCommandBuffer.data_pointer := F_BIGTYPE(
			pData := ADR(PerformanceDataRecordBuffer[fbPerfromanceDataCommandBuffer.index]), 
			cbLen := SIZEOF(PerformanceDataRecordBuffer[fbPerfromanceDataCommandBuffer.index])
		);
	// InfluxDBの書込み対象Measurement名をセット
	fbPerfromanceDataCommandBuffer.db_table_name := 'PerformanceData';
	// DUTsで定義した書込みデータの構造体名をセット
	fbPerfromanceDataCommandBuffer.data_def_structure_name := 'PerformanceData';
	// チャンクの最小サイズを設定（DB書込みスループットにより自動拡張される）
	fbPerfromanceDataCommandBuffer.minimum_chunk_size := 500;
	// データバッファ（PerformanceDataRecordBuffer）の配列の最大要素番号をセット
	fbPerfromanceDataCommandBuffer.upper_bound_of_data_buffer	:= RECORD_DATA_MAX_INDEX;
	// バッファ制御FBを実行。コマンドキューを渡す。
	fbPerfromanceDataCommandBuffer(
		command_queue := command_queue
	);

	// サイクル記録メソッドの連続実行
	fbPerfromanceDataCommandBuffer.cyclic_record();
	```

	最後にデータベース書込み制御部です。

	```pascal
	// データベース書込みロジック

	fbInfluxDBRecorder(
		command_queue := command_queue,
		nDBID := 1,      // Database ID by TF6420 configurator
	);
	```

#### イベントデータ記録（record_once）実装例


* 宣言部

	```pascal

	PROGRAM RecordToInfluxDB

	VAR
		// 書き込むデータインスタンスの定義
		DataBaseProcessModeRecordData	:ProcessModeData;

		// データベース書き込みコマンドを処理するFIFOキュー
		command_queue	: CommandQueueMember;

		// ビジネスロジック用ファンクションブロック
		fbProcessModeBuffer	:RecordDataQueue; // キュー制御ロジック
		fbInfluxDBRecorder	:RecordInfluxDB;	// データベース書込みロジック

		// おまけ。処理開始、終了のイベントとプロセス番号定義
		bExecuting	: BOOL;
		dProcessNumber: UDINT;
		bExecRTrig	:R_TRIG;
		bExecFTrig	:F_TRIG;

	END_VAR
	```

* プログラム部

	まずはデータのセット部。サイクル記録と違うのは、バッファが無いこと。直接 `DataBaseProcessModeRecordData` という単一データ（配列化して複数データを用意する事も可能）を作成し、データベース書込みチャンクとする。

	```pascal
	// コマンドキューの生成
	command_queue.controller(aData := command_queue.buffer_index);

	// Tag Dataのセット
	DataBaseProcessModeRecordData.machine_id := 'machine-1';  // 装置1のデータである事を示す
	DataBaseProcessModeRecordData.job_id := 'task_info';	　// データ種別

	// 疑似処理開始、終了パルス
	bExecRTrig(CLK := bExecuting);
	bExecFTrig(CLK := bExecuting);

	IF bExecRTrig.Q THEN
		// 処理開始毎に処理番号を繰り上げ
		dProcessNumber := dProcessNumber + 1;
	END_IF

	// Field Data のセット（イベントの状態セット）
	DataBaseProcessModeRecordData.executing := bExecuting;
	DataBaseProcessModeRecordData.message := Tc2_Standard.CONCAT('Process # : ',UDINT_TO_STRING(dProcessNumber));

	```

	続いてキュー制御部の実装。用意したチャンクデータを同様にT_Arg型へ変換してセット。そのあと各種属性を定義し、

	```pascal
	// 書き込んだデータをジェネリクス型（T_Arg）に変換してセットする。
	fbProcessModeBuffer.data_pointer := F_BIGTYPE(
			pData := ADR(DataBaseProcessModeRecordData), 
			cbLen := SIZEOF(DataBaseProcessModeRecordData)
		);
	// InfluxDBの書込み対象Measurement名をセット
	fbProcessModeBuffer.db_table_name := 'PerformanceData';
	// DUTsで定義した書込みデータの構造体名をセット
	fbProcessModeBuffer.data_def_structure_name := 'ProcessModeData';
	// チャンクの最小サイズを設定（DB書込みスループットにより自動拡張される）
	fbProcessModeBuffer.minimum_chunk_size := 1;
	// バッファ制御FBを実行。コマンドキューを渡す。
	fbProcessModeBuffer(
		command_queue := command_queue
	);

	IF bExecRTrig.Q OR bExecFTrig.Q THEN
		// 必ず1サイクルだけ実行すること。
		// 実行し続けたら極小のチャンクの書込み命令が毎サイクルキューインするため、あっという間にキューが溢れる。
		fbProcessModeBuffer.record_once();
	END_IF
	```

	最後にデータベース書込み制御部です。

	```pascal
	// データベース書込みロジック

	fbInfluxDBRecorder(
		command_queue := command_queue,
		nDBID := 1,      // Database ID by TF6420 configurator
	);
	```

## Chronograf による可視化

influxDBには、 Chronograf と呼ばれる可視化ソフトが付属しています。これを用いて次図のようなダッシュボードを簡単に構築することができます。

ここでは前章に掲載した60秒毎に1000回づつループ回数を増やしてCPU負荷を増やすプログラムを実行した
様子を記録したデータを表示しています。

この結果、CPU使用率とExceedカウンタの値のヒストリを並べたところ、52 $\%$ のCPU使用率となった辺りからExceedカウンタが上がり始めている事がわかります。

![](2023-02-19-19-33-21.png)

なおこのデータは、C6025において、BaseTime（1tick）を 1$ms$ とし、サイクルタイムを1tick （$=1ms$）に設定したPLCタスクをCore2（0から数えて）にWindowsと共用で80%の占有率で割り当てた際の計測データです。PLC Cycle timeの設定を遵守できない要因はCPU負荷率だけとは限らないため、ここに示す解析例はあくまでも一例としてご理解願います。
