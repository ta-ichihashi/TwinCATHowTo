# 並列非同期ジョブ制御

制御システムでは、様々な動作や振る舞いを持つサブコンポーネント機器を取り扱う必要があり、これらの特徴に合わせて制御機器システムのソフトウェア開発とテスト（品質管理）に手間や工数をかけなければなりません。

この工数を定量化し、品質のばらつきを低減させるためには、抽象度に応じた設計の分離が欠かせません。

例えばモーション機器であれば、メーカや機種によってI/Oの入出力構成や通信インターフェースはバラバラですが、これらの機器に求める機能はインチング、JOG、原点復帰、リミット制御、位置決め、トルクなどの共通機能に抽象化できます。さらに、これらの機器がどのようなシーンで使われるか、という視点に移すと、保守・調整、生産運転、段取り替えなどの生産現場におけるさまざまなユースケースまで抽象化できます。

このように抽象度の層の間を共通のインターフェースとしておく事により、抽象度の高い機能レベルから取り扱える機器は簡単に付け替えることが可能となります。

ポリモフィズムは、この抽象度の異なるオブジェクト間を共通インターフェースによって結び付け、共通のロジックから様々な異なる具象オブジェクトを取り扱う事ができるようにするオブジェクト指向の機能概念です。

ここでは、制御でよく使われる状態マシンとアクティビティ制御を抽象化し、様々な機器を一様に制御する方法についてご紹介します。

状態マシンとは、{numref}`state-machine` に示す例のようなプログラムコードをいいます。`_state`変数に格納された状態に応じて処理が順次実行されたり、場合によっては任意の処理ステップへジャンプすることができます。`CASE`文では、マッチしない`_state`番号のブロックは一切処理が行われません。

{numref}`state-machine` のプログラムでは、状態1で3秒のディレイ時間を経て、状態2で外部入力の信号の立ち上がりをカウントし、20回に達するまで`bOutput`をTRUE状態にする、という処理を行っています。

```{code-block} iecst
:caption: 状態マシン例
:name: state-machine

VAR
    _state : UINT;
    bStart :BOOL;
    bOutput AT%Q* :BOOL;
    bInput AT%I* :BOOL;
    bComplete :BOOL;
    delay_timer :TON;
    input_edge :R_TRIG;
    counter : DINT;
    delay_time :TIME := T#3S;
    process_count : DINT := 30;
END_VAR


CASE _state OF
    0:
        bOutput := FALSE;
        bComplete := FALSE;
        counter := 0;
        IF bStart THEN
            _state := 1;
        END_IF
    1:
        delay_timer(IN := TRUE, PT:=delay_time);
        IF process_timer.Q THEN
            _state := 2;
        END_IF
    2:
        bOutput := TRUE;
        input_edge(CLK := bInput);
        IF input_edge.Q THEN
            counter := counter + 1;
        END_IF
        IF counter >= process_count THEN
            _state := 3;
        END_IF
    3:
        bOutput := FALSE;
        bComplete := TRUE;
        IF NOT bStart THEN
            _state := 0;
        END_IF
END_CASE
```

このプログラムコードには欠陥があります。`delay_timer` は状態1の時にしか実行されません。このため、状態2に移行した後も`delay_timer`のTONインスタンスの状態は保持されたままとなります。次回この状態マシンを最初から実行し直すと、状態1を実行し始めた時点ですでに前回のタイマ値を保持しており、ディレイ時間の設定値3秒が経過した状態から始まります。よって、一瞬で状態1が終了してしまうこととなります。

従って、{numref}`state-machine2` の通りタイマファンクションブロックを別の状態の際に初期化しなければなりません。

```{code-block} iecst
:caption: タイマファンクションブロックの初期化を施した状態マシン例
:name: state-machine2

CASE _state OF
    0:
        bOutput := FALSE;
        bComplete := FALSE;
        counter := 0;
        IF bStart THEN
            _state := 1;
            delay_timer(IN := FALSE);
        END_IF
    1:
        delay_timer(IN := TRUE, PT:=delay_time);
        IF process_timer.Q THEN
            _state := 2;
        END_IF
    2:
        delay_timer(IN := FALSE);
        bOutput := TRUE;
        input_edge(CLK := bInput);
        IF input_edge.Q THEN
            counter := counter + 1;
        END_IF
        IF counter >= process_count THEN
            _state := 3;
        END_IF
    3:
        bOutput := FALSE;
        bComplete := TRUE;
        IF NOT bStart THEN
            _state := 0;
        END_IF
END_CASE
```

このように、コアとなる処理内容はタイマにより時間計測を行うことですが、その前後で初期化などを行う必要があります。

この実装例でみられるとおり、本来の目的では、状態1はタイマによる処理、状態2はカウンタによる処理、としたいところですが、タイマの後始末や初期化処理がその前後のステップに食い込むなど、明確にプログラムロジックが分かれていません。

これはメンテナンス性、可読性を落とす原因となっています。これらを処理目的毎に明確に「タスク」に分離し、オブジェクトモデルでジョブを構築できることを目指しましょう。

## サンプルプログラム解説

```{note}

本サンプルプログラムは、以下で公開しています。

[https://github.com/Beckhoff-JP/PLC_JobManagementFramework.git](https://github.com/Beckhoff-JP/PLC_JobManagementFramework.git)

```

まず、今回作成するジョブ制御フレームワークのクラス図を{numref}`fig_job_control_class_diagram` に示します。

このモデルの中核は、タスクの構成を表すインターフェース`InterfaceFuture`です。非同期並列処理の概念である、[Futureパターン](https://ja.wikipedia.org/wiki/Future_%E3%83%91%E3%82%BF%E3%83%BC%E3%83%B3)からこの名前としました。

このインターフェースでは、次のメソッドを定義します。いずれも引数は無しで、戻り値はBOOL型です。`FB_Executor` オブジェクトによりメソッドが実行され、処理を進行するためには、個々のメソッドの戻り値をTRUEにします。処理結果は別途`HRESULT`型のプロパティ`result`にセットします。

```{csv-table}
:header: メソッド名, 説明

`init`, 実行前に必要な変数やオブジェクトの初期化を行います。
`execute`, 独自の処理ロジックを実装します。
`quit`, 実行後の変数やオブジェクトの後始末を行います。
```

このインターフェースを実装するプログラムは、すべて特定のフォルダに集めておきます。この例では`activities`フォルダにあります。

ここには、いわば制御デザインパターンを格納する場所です。ハードウェアに合わせたものや、動作パターン毎にファンクションブロックを配置します。

正常系だけではなく、異常終了した後の特別な処理なども定義しておくと良いでしょう。

```{figure} assets/activity_control_class_diag.png
:align: center
:name: fig_job_control_class_diagram

JOB制御クラス図
```

InterfaceFutureを実装したファンクションブロックインスタンスを`FB_Executor`の`future`プロパティを経てロードし、init()およびexecute()メソッドを実行すると、{numref}`fig_future_time_chart`の基本処理単位のセッションを実施します。先ほど示した状態マシンの例にあるような、制御実行前の準備、そして、制御終了後の処理など個別に定義でき、前処理や処理本体の開始タイミングは外部から与えられるようにします。

```{figure} assets/task_time_chart.png
:align: center
:name: fig_future_time_chart

Futureの構成とハンドシェーク
```

また、単一のタスクだけではなく、複数のタスクをまとめて処理するコンテナオブジェクトを用意しました。`FB_ParallelJobContainer`や`FB_SerialJobContainer`を用いると、{numref}`fig_parallel_job_container`や、{numref}`fig_serial_job_container`のように同時実行、または、逐次実行が可能となります。


```{figure} assets/run_future_cue.png
:align: center
:name: fig_parallel_job_container

並列処理JOBコンテナ（`FB_ParallelJobContainer`によるJOB配置イメージ）
```

```{figure} assets/run_future_serial.png
:align: center
:name: fig_serial_job_container

直列処理JOBコンテナ（`FB_SerialJobContainer`によるJOB配置イメージ）
```

また、`FB_ParallelJobContainer`と`FB_SerialJobContainer`もまた`InterfaceFuture`インターフェースを実装していますので、それ自体を`FB_Executor`に処理させることができます。これにより、並列処理と逐次処理を組み合わせた複雑なタスク実行が可能となっています。

```{tip}
このデータモデルは、コンテナと処理が親子関係を構成し、定義によってさまざまな枝葉モデルが構築可能です。このソフト実装のデザインパターンを、[GoFのCompositeパターン](https://ja.wikipedia.org/wiki/Composite_%E3%83%91%E3%82%BF%E3%83%BC%E3%83%B3)と呼びます。
```

コンテナも含めたJOBの概念図は次の通りとなります。色付きの線が、個々のタスクに該当します（{numref}`fig_job_control_class_diagram`の`ConcreteActivity`に該当するオブジェクト）。これらはFB_ParallelJobContainerやFB_SerialJobContainerと共に、InterfaceFutureを実装したものです。このインターフェースを使って、FB_Executorが処理を実行します。

![](assets/sample_code_job_structure.png){align=center}

次のMAINプログラムは、この図に従った実際のプログラム例です。

```{code-block} iecst
PROGRAM MAIN
VAR
    _state :UINT;
    fbTask1 : FB_ControllerType_1;
    fbTask2 : FB_ControllerType_1;
    fbTask3 : FB_ControllerType_2;
    fbTask4 : FB_ControllerType_2;
    component1_in : BOOL;
    component1_out : BOOL;
    component2_in : BOOL;
    component2_out : BOOL;
    component3_in : BOOL;
    component3_out : BOOL;
    component4_in : BOOL;
    component4_out : BOOL;
    serial_job1 : FB_SerialJobContainer;
    serial_job2 : FB_SerialJobContainer;
    serial_job3 : FB_SerialJobContainer;
    pararel_job1 : FB_ParallelJobContainer;
    pararel_job2 : FB_ParallelJobContainer;
    executor : FB_Executor;
END_VAR


// FB_Executor.execute()メソッドは常時実行
executor.execute();

CASE _state OF
    0:
        // 固有パラメータ設定
        fbTask1.own_parameter := T#3S;
        fbTask2.own_parameter := T#10S;
        fbTask3.own_parameter := 2;
        fbTask4.own_parameter := 2;
        
        // 入出力変数の受け渡し
        fbTask1(own_output := component1_out);
        fbTask2(own_output := component2_out);
        fbTask3(own_input := component3_in, own_output := component3_out);
        fbTask4(own_input := component4_in, own_output := component4_out);
        
        // futureオブジェクトの配置により実行順序を定義
        pararel_job1.add_future(serial_job1);
        pararel_job1.add_future(serial_job2);
        serial_job1.add_future(fbTask1);
        serial_job1.add_future(fbTask2);
        serial_job2.add_future(fbTask3);
        serial_job2.add_future(fbTask4);
        pararel_job2.add_future(fbTask1);
        pararel_job2.add_future(fbTask2);
        serial_job3.add_future(pararel_job1);
        serial_job3.add_future(pararel_job2);
        executor.future := serial_job3;
        _state := 1;
    1:
        // シーケンス開始
        IF executor.ready THEN
            executor.start();
        END_IF
        IF executor.done THEN
            _state := 2;
        END_IF
    2:
        executor.init();
        _state := 1;
END_CASE
```
