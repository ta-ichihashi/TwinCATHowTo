(alarm_system_library)=
# 付録：開発者ドキュメント

個々のイベントエントリをPLCで扱うための`FB_Alarm`ファンクションブロックと、アラームエントリを集計する`FB_AlarmCalculator`ファンクションブロックを実装します。

また、`FB_AlarmCalculator`では、アラーム発生、消滅のイベントを監視し、`I_EventExporter`を実装したファンクションブロックによりさまざまなメディアにイベント通知を送ることができます。

本ライブラリにはTF6420を通じて{ref}`chapter_influxdb`へエクスポートするファンクションブロックが内包されています。インターフェース仕様に応じて独自のエクスポート機能を実装することも可能です。

## クラス図

![](assets/model.drawio.png){align=center}

FB_Alarm
    : `FB_TcAlarm`を継承した個々のアラームエントリのインスタンスです。コンストラクタメソッド（FB_init）にて`FB_AlarmCalculator`のリファレンスを登録しておくことで、同ファンクションブロックによる集計対象にすることができます。

FB_AlarmCalculator
    : 登録された`FB_Alarm`を走査し、発生中アラーム、また、新規（未確認）アラームの有無を集計することができます。

I_EventExporter
    : FB_AlarmCalculatorにより実行されるアラームの発生、消滅の際に実行される`send_signal`イベントハンドラ、サイクリック実行される`execute`の二つのメソッドを定義したインターフェースです。実装パターンによりデータベースやCSVファイル、MQTTメッセージペイロードなど、様々なメディアにイベントデータをエクスポートすることができます。

FB_AlarmDBExporter
    : I_EventExporterを実装した、{ref}`chapter_influxdb`にアラームの発生、解除イベントを記録するエクスポートロジックを実装したファンクションブロックです。

