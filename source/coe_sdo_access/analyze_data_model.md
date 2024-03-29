# SDOデータの構造解析

ここでは、EL6695（EtherCATゲートウェイターミナル）を例として取り上げます。このターミナルでは、Index `0xFA20` に診断データが格納されています。これらをコンプリートアクセスで読み出します。

個々のオブジェクトのデータ仕様は、エントリをダブルクリックすることで詳細ウィンドウが現れますのでここから確認できます。データサイズは最下部の`Bit Size`を閲覧できますので、対応する型を選定してください。

![](assets/2024-03-29-15-48-52.png){align=center}

もう一つの方法として、ESIファイルをテキストエディタで開く方法があります。TwinCATのXAEにおいてESIファイルは、`C:\TwinCAT\3.1\Config\Io\EtherCAT` 以下に配置します。この中の該当するサブデバイスのESIファイルを閲覧する事で、個々の`Sub index`オブジェクトの名称、データ型、サイズがわかります。

```{code-block} xml
:caption: Beckhoff EL66xx.xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<EtherCATInfo xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="EtherCATInfo.xsd" Version="1.2">
    <Descriptions>
        <Devices>
            <Device Physics="KK">
                <Profile>
                    <Dictionary>
                        <DataTypes>
                            <DataType>
                                <Index>#xFA20</Index>
                                <Name>Device Diag</Name>
                                <Name>DTFA20</Name>
                                <BitSize>480</BitSize>
                                <SubItem>
                                    <SubIdx>0</SubIdx>
                                    <Name>SubIndex 000</Name>
                                    <Type>USINT</Type>
                                    <BitSize>8</BitSize>
                                    <BitOffs>0</BitOffs>
                                    <Flags>
                                        <Access>ro</Access>
                                    </Flags>
                                </SubItem>
                                <SubItem>
                                    <SubIdx>1</SubIdx>
                                    <Name>Status</Name>
                                    <Type>UINT</Type>
                                    <BitSize>16</BitSize>
                                    <BitOffs>16</BitOffs>
                                    <Flags>
                                        <Access>ro</Access>
                                    </Flags>
                                </SubItem>
                                <SubItem>
                                    <SubIdx>2</SubIdx>
                                    <Name>CPU Usage [%]</Name>
                                    <Type>UINT</Type>
                                    <BitSize>16</BitSize>
                                    <BitOffs>32</BitOffs>
                                    <Flags>
                                        <Access>ro</Access>
                                    </Flags>
                                </SubItem>
                                <SubItem>
                                    <SubIdx>3</SubIdx>
                                    <Name>Heap Usage [%]</Name>
                                    <Type>UINT</Type>
                                    <BitSize>16</BitSize>
                                    <BitOffs>48</BitOffs>
                                    <Flags>
                                        <Access>ro</Access>
                                    </Flags>
                                </SubItem>
                                    :
```
これに応じた構造体を以下の通り定義します。

```{admonition} 重要
:class: warning

コンプリートアクセスでサブインデックスがバイト列で構成されたSDOは、2byteアライメントのデータ配置となっています。対してTwinCAT3の標準的なメモリアライメントは8byteアライメントです。このままではバイト配列を構造体データに対応せずデータがずれてしまいます。このため、SDOとマッピングする構造体、または、そのインスタンス変数などに対しては、必ず2byteアライメントを指定する`{attribute 'pack_mode' := '2'}`のattributeを付与してください。
```

```{code-block} iecst
{attribute 'pack_mode' := '2'}
TYPE sdo_EL6695_diag :
STRUCT
    identify : USINT;
    status : UINT;
    cpu_usage : UINT;
    heap_usage : UINT;
    aoe_packets: UINT;
    eoe_packets : UINT;
    foe_packets : UINT;
    soe_packets : UINT;
    voe_packets : UINT;
    other_pacekts: UINT;
    mbx_info : UINT;
    pd_copy_time_my: UINT;
    pd_copy_time_remote :UINT;
    info_2 : UINT;
    info_3 : UINT;
    info_4 : UINT;
    info_5 : UINT;
    info_6 : UINT;
    info_7 : UINT;
    info_8 : UINT;
    info_9 : UINT;
    info_10 : UINT;
    info_11 : UINT;
    info_12 : UINT;
    info_13 : UINT;
    info_14 : UINT;
    info_15 : UINT;
    info_16: UINT;
    info_17 : UINT;
    info_18 : UINT;
END_STRUCT
END_TYPE

```

