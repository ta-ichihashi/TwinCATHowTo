# メインプログラムでの実行

mainプログラムに `fb_PLCTaskMeasurement` ファンクションブロックのインスタンスを定義して実行します。これにより出力変数にて各種メトリクス値を取り出すことができます。

また、PLC演算時間ストレスをかけるため、test_timerにて設定した時間が到達するたびに1000個づつの繰り返し回数が増加し、毎サイクルこの設定回数分、加算処理を行うプログラムを定義しています。

また、CPUの使用率が70%の危険水準を超えると、自動的に繰り返し回数のターゲットを0にリセットする様にしています。

```pascal
VAR
    fb_PLCTaskMeasurement: PLCTaskMeasurement;
    test_timer :TON;
    j:UDINT := 0;
    target: UDINT := 0;
    test_var:ULINT;
END_VAR

// Get ipc data.
fb_PLCTaskMeasurement(ec_master_netid := '*.*.*.*.*.*'); // Should be defined the EtherCAT master AMSnetID


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

```

読み取ったデータは、Scope viewのプロジェクトを新規に作成し、Target browserにてMAINプログラムの `fb_CPUTaskMeasurement` インスタンスの各変数を登録し、次図の通り表示させてください。Task実行時間の単位は、100ns単位です。

```{figure} 2023-02-17-19-33-45.png
:width: 600px
:align: center
:name: scope_view

スコープビューの例
```

ただし、{ref}`scope_view` の通り、Scope viewを継続的に監視し、永続化ファイルへ保存するにはScope view professional ライセンスが別途必要となります。また、PC上の他のプログラムとシームレスに連携してデータ活用を行うには、一般的なデータベースの活用が欠かせません。

そこで次章より、TF6420 Database serverを用いた、時系列データベース "influxDB" に対してリアルタイムデータ記録を行うプログラム例をご紹介いたします。
