<#
TcXaeMgmtによるTwinCAT変数のCSV出力と書き戻しPowerShellスクリプト例
#>

function write-value {
    Param(
        $ads_value, # データオブジェクト
        $symbol, # TwinCATのシンボルオブジェクト
        [ref]$dict, # 変数のシンボルパスと値の連想配列を参照渡し
        [bool]$ReadOnly = $false, # TwinCAT変数へは書込みを行わないオプションを有効にする
        [bool]$MergeDict = $false # $dictの定義内容をTwinCAT変数へ反映する動作を有効にする
    )

    if ($ads_value -is [array]){
        # 配列ならば要素ごとに再起呼び出し
        for ($i=$ads_value.GetLowerBound(0);$i -le $ads_value.GetUpperBound(0); $i++){
            write-value $ads_value.item($i) $symbol.item($i) $dict $ReadOnly $MergeDict
        }
    }elseif($symbol.IsContainerType){
        # 構造体ならば要素ごとに再起呼び出し
        foreach ($sym in $symbol.MemberInstances){
            $instance_name = $sym.InstanceName
            write-value $ads_value.$instance_name $sym $dict $ReadOnly $MergeDict
        }
    }else{
        # プリミティブの場合の処理
        if(!$ReadOnly){
            # ReadOnlyでなければADS経由で変数に書き込み
            if ($MergeDict -and $dict.Value.ContainsKey($symbol.InstancePath) -and $dict.Value[$symbol.InstancePath] -ne $ads_value){
                # マージオプションが有効なら、ディクショナリの値と$ads_dataの内容が異なる場合にディクショナリの内容に書き換える
                $ads_value = $dict.Value[$symbol.InstancePath]
            }
            $symbol | Write-TcValue -Value $ads_value -Force
        }
        # ディクショナリを更新
        if($dict.Value.ContainsKey($symbol.InstancePath)){
            $dict.Value[$symbol.InstancePath] = $ads_value
        }else{
            $dict.Value.add($symbol.InstancePath, $ads_value)
        }

    }
}

<#
メインロジック
#>


# ローカルPCのPLCへ接続
$session = New-TcSession -NetId '127.0.0.1.1.1' -Port 851

<#
構造体で定義された複雑なデータ構造を持つ変数の現在値を一括して読み出して"original.csv"という名前のCSVファイルに出力する。
#>

# 読み出し
$symbol = $session | Get-TcSymbol -path 'GVL.test_data'
$data = $symbol | Read-TcValue


# エクスポート用の連想配列
$result = [System.Collections.Generic.Dictionary[String, PSObject]]::new()

# 現在値を保存するCSVファイル名の指定
$current_data_file_name = "original.csv"

# 変数の内容を全検索して、エクスポート用の連想配列にセット
# -ReadOnly $trueによりTwinCATの変数には反映しない
write-value $data $symbol ([ref]$result) -ReadOnly $true
# $result 連想配列を加工し、original.csvファイルにCSVファイルとして出力
$result.GetEnumerator() | Select @{N="Variable"; E={$_.Key}}, @{N="Value"; E={$_.Value}} | Export-Csv $current_data_file_name -Encoding Default -NoTypeInformation

<#
CSVファイルで定義したデータをインポートして反映し、マージ後の全データをafter_merge.csvに保存する。
#>

$import_file_name = "import.csv"
$after_merge_data_file_name = "after_merge.csv"

if(Test-Path $import_file_name){

    # CSVファイルを読みだしてオブジェクト作成
    $import_data = Import-Csv -Path $import_file_name -Encoding Default


    # インポート用の連想配列新規作成
    $import = [System.Collections.Generic.Dictionary[String, PSObject]]::new()

    # CSVファイルから読みだしたオブジェクトを、$import連想配列に変換
    foreach($row in $import_data){
        if($import.ContainsKey($row.Variable)){
            $import[$row.Variable] = $row.Value
        }else{
            $import.add($row.Variable, $row.Value)
        }
    }

    # 連想配列のデータをマージモードでTwinCATへ書き出し
    # -ReadOnly $true を指定しないとデフォルト設定が有効となり、TwinCATへの変数書込みが実施される
    # -MergeDict $true で$importの連想配列の値を反映させる。
    write-value $data $symbol ([ref]$import) -MergeDict $true

    # マージ後の全データをafter_merge.csvにCSVファイルとして出力
    $import.GetEnumerator() | Select @{N="Variable"; E={$_.Key}}, @{N="Value"; E={$_.Value}} | Export-Csv $after_merge_data_file_name -Encoding Default -NoTypeInformation

}
