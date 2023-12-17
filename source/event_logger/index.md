# イベントロガーとアラーム管理

装置の制御ロジックで発生した様々なインシデントについて、その発生時刻や重大度、および、メッセージをロギングする機構があり、TwinCAT EventLoggerと呼びます。

![](https://infosys.beckhoff.com/content/1033/tc3_eventlogger/Images/png/4992463627__Web.png){align=center}

この機構を使い、装置制御にて発生した様々な警告、メッセージをHMIへ表示したり、制御上でオペレータへ通知するブザーやランプ等の点灯を行ったり、Windowsアプリケーションログ・SysLog等へ記録させる事ができます。

本章では、PLCプログラム上における異常監視ロジックの実装と、アラームイベントの登録方法、そして全てのアラームの集計や、ブザーやHMIへの表示・制御インターロックへ用いるための一連のデザインパターンをご紹介します。

{ref}`alarm_system_library` 節の実装を独立したライブラリとして保存しておくと、汎用的なアラーム管理フレームワークとして活用いただく事が可能になっています。

```{toctree}
:maxdepth: 2
:caption: 目次

make_user_event
fb_alarm_library
relation_with_database
user_alarm
```
