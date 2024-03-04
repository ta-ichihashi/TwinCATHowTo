# ADSを介して変数読み書きするPowerShellスクリプト実装

[こちらのInfoSys](https://infosys.beckhoff.com/content/1033/tc3_ads_ps_tcxaemgmt/15510665739.html?id=6452251772138829586)にて、様々な方法でデータを書き込む事例が紹介されています。ここでは構造体などの複雑なデータモデルも、メモリイメージのまま一括して送る方法や、単体の変数ノードを指定して送る方法などが紹介されています。

ここでは、最もPowerShellの高次レベルでデータモデルに読み出し、PowerShell内でデータを編集したあと変数に書き戻す実装例をご紹介します。

まず。{ref}`function_write_value`の通り、すでに読み出し済みのデータモデルに対してデータを書き込む関数を準備します。

```{code-block} powershell
:caption: 変数にデータを書き込む関数
:name: function_write_value

function write-value($ads_value,$symbol) {

    if ($ads_value -is [array]){
        # 配列ならば要素ごとに再起呼び出し
        for ($i=$ads_value.GetLowerBound(0);$i -le $ads_value.GetUpperBound(0); $i++){
            write-value $ads_value.item($i) $symbol.item($i)
        }
    }elseif($symbol.IsContainerType){
        # 構造体ならば要素ごとに再起呼び出し
        foreach ($sym in $symbol.MemberInstances){
            $instance_name = $sym.InstanceName
            write-value $ads_value.$instance_name $sym
        }
    }else{
        # プリミティブならADS経由で変数に書き込み
        $symbol | Write-TcValue -Value $ads_value -Force
        # 変数パスと値を画面に出力
        write-host $symbol.InstancePath $ads_value
    }
}
```

これを用いたメインルーチンの実装例を{ref}`main_routine` にご紹介します。最初に`New-TcSession`にてADSの通信セッションオブジェクトを生成します。本例ではIPC上のWindows上で実行することを前提としていますので、ローカルターゲットである`127.0.0.1.1.1`で、1台目のPLCのTcCOMであるADSポート`851`を指定します。

その後、`Get-TcSymbol` にてシンボルオブジェクトを取得します。この際、`-path` にて{ref}`GVL_test_data`で実装したグローバル変数を指定します。

続いて、シンボルオブジェクトを通じて`Read-TcValue`を実行することで、PLC変数の現在値を読み出して、データオブジェクトを生成します。

```{code-block} powershell
:caption: メインルーチン
:name: main_routine

# ローカルPCのPLCへ接続
$session = New-TcSession -NetId '127.0.0.1.1.1' -Port 851

# 構造体でアクセス

# 読み出し
$symbol = $session | Get-TcSymbol -path 'GVL.test_data'
$data = $symbol | Read-TcValue

# 書き換え(データ操作)

for ($j = 1; $j -le 10; $j++){
    for ($i = 1;$i -lt 9;$i++){
        $data.item($j).ar_8.item($i) = 0
    }
    $data.item($j).flag = $true
    $data.item($j).record[0].value = 10 + $data.item($j).record[0].value
    [string]$DATE = Get-Date -Format "yyyy-MM-dd hh:mm:ss" # 新しい変数を代入する場合はちゃんと型指定しなければならない。
    $data.item($j).record[0].datetime = $DATE
}

# 書き出し
write-value $data $symbol
```

読みだしたデータオブジェクトは、下記に示すエントリポイント以下からは、TwinCAT上で構築したデータモデルそのままのモデルとしてPowerShell上で直接編集可能です。

`Get-TcSymbol`で指定した変数が配列変数以外の場合
    : データオブジェクト以下直接要素にアクセスできます。配列も`[]`でアクセス可能です。

`Get-TcSymbol`で指定した変数が配列変数の場合
    : 配列要素を、データオブジェクトに`.item(<要素番号>)`を付加してから、以下各要素にアクセスします。今回の例では、`$data.item(1)`～`$data.item(10)`以下に、それぞれ`my_struct`型のデータモデルがぶら下がっています。

```{warning}
PowerShell上で新しい変数を使って代入する場合は、型を明示してください。明示しない変数を代入するとエラーとなります。
```

もっともシンプルな、単体の変数へアクセスする場合は次のような例となります。この場合、指定した変数がプリミティブ変数ですので、データオブジェクトに直接リテラルを代入した後に`write-value`関数を呼び出します。

```{code-block} iecst
:caption: グローバル変数宣言

{attribute 'qualified_only'}
VAR_GLOBAL
    test_premitive: UINT;
END_VAR
```

```{code-block} powershell
:caption: `GVL.test_premitive` 変数を4に書き換えるスクリプト例

# 読み出し
$symbol = $session | Get-TcSymbol -path 'GVL.test_premitive'
$data = $symbol | Read-TcValue

$data = 4

write-value $data $symbol
```
