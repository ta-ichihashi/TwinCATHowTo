# 配列オブジェクトの参照渡しと処理

配列を取り扱うプログラムをライブラリなど汎用性を高めるために必要なテクニックをご紹介します。

## 可変長配列

```{note}
参考InfoSysサイト : [Array with variable length](https://infosys.beckhoff.com/content/1033/tc3_plc_intro/8825257611.html?id=420093545259366736)
```

ファンクションブロックのVAR_IN_OUT定義ブロック内では可変長配列を定義することができます。可変長であるのはあくまでもファンクションブロック内部だけであり、入出力変数に外部からセットする際の配列長は固定でなければなりません。

ファンクションブロック内部では配列サイズに依存しないプログラムロジックを組む事で、ライブラリを利用するユーザ側は様々なサイズの配列を取り扱う事ができます。


### ファンクションやファンクションブロックの作り方と取り扱い方

可変長配列の宣言は簡単です。VAR_IN_OUTに定義する配列変数のサイズ指定を`*`アスタリスクとします。

```{code} iecst
FUNCTION F_Sum : DINT;
VAR_IN_OUT
    aData     : ARRAY [*] OF INT;
END_VAR
VAR
    i, nSum   : DINT;
END_VAR
```

ただし、中で使われるプログラムコードは、FOR文などを用いますが、配列サイズが分かりません。これを知る手段として、次のものがあります。

```{code} iecst
配列の最小の要素インデックス番号 := LOWER_BOUND( <配列変数名> , <配列次元数> )
配列の最大の要素インデックス番号 := UPPER_BOUND( <配列変数名> , <配列次元数> )
```

これを用いる事で、FOR文は以下の通り定義できます。

```{code} iecst
nSum := 0;
 
FOR i := LOWER_BOUND(aData,1) TO UPPER_BOUND(aData,1) DO
    nSum := nSum + aData[i];
END_FOR;

F_Sum := nSum;
```

この通り、配列変数とその次元番号を指定することで、最小、最大のインデックス番号を知る事ができます。

これを定義したファンクションやファンクションブロックは、次の通り異なる配列サイズを処理する事ができます。

```{code} iecst
VAR
    aNaturalNumber1_10 := ARRAY [1..10] OF DINT := 1,2,3,4,5,6,7,8,9,10; // 1～10までの自然数が定義された配列

    aNaturalNumber11_15 := ARRAY [1..5] OF DINT := 11,12,13,14,15; // 1～10までの自然数が定義された配列
    iSumValue : INT;
END_VAR

// iSumValue = 55
iSumValue := F_Sum(aNaturalNumber1_10)

// iSumValue = 65
iSumValue := F_Sum(aNaturalNumber11_15)
```

## ポインタを用いた配列操作

配列の実態は、決まったデータ型の連続したメモリイメージです。従って、個々のデータ型のサイズと、構造体やファンクションブロックであれば、メモリアドレスとその操作により配列操作を行う事ができます。

一例として、ある構造体配列とそのポインタアドレスを外部から定義し、両端キュー（deque）に該当する処理を行うファンクションブロックをご紹介します。


```{code} iecst
FUNCTION_BLOCK FB_deque
VAR_INPUT
    pArrayData: PVOID; // 配列変数のポインタ
    pData : PVOID; // セットしたいデータ型の無いメモリアドレスを指定する場合はPVOID型を使う
    cbData: UDINT; // 配列の要素変数のサイズを指定
    bPut: BOOL; // 書込み
    bGet: BOOL; // 読み出し
    nArraySize: UDINT; // 配列サイズ
END_VAR

VAR_OUTPUT
    buffer_usage: UDINT; // バッファ使用数
    bError: BOOL; //バッファ満杯
END_VAR

VAR
    write_index: UDINT; // 現在の書込みバッファインデックス
    read_index: UDINT; // 現在の読み込みバッファインデックス
    address_temp: PVOID;
END_VAR

bError := FALSE;

// バッファ書き込み要求の処理
IF bPut AND buffer_usage < nArraySize AND nArraySize > 0 THEN
    // 書込み先の配列アドレスを計算
    address_temp := pArrayData + cbData * write_index;
    // 計算したアドレスへ、データをデータサイズ分メモリコピーする
    MEMCPY(address_temp, pData, cbData);
    // 次のバッファインデックスへ繰り上げ
    write_index := write_index + 1;
    // 配列サイズに達したらインデックスを0リセット
    IF write_index > nArraySize - 1 THEN
        write_index := 0;
    END_IF
    // Buffer使用量カウンタを繰り上げ
    buffer_usage := buffer_usage + 1;
ELSIF bPut THEN
    bError := TRUE;
END_IF

// バッファからデータ読み出し要求の処理

IF bGet AND buffer_usage > 0 AND nArraySize > 0 THEN
    // 書込み先の配列アドレスを計算
    address_temp := pArrayData + cbData * read_index;
    // 計算したアドレスへ、データをデータサイズ分メモリコピーする
    MEMCPY(pData, address_temp, cbData);
    // 次のバッファインデックスへ繰り上げ
    read_index := read_index + 1;
    // 配列サイズに達したらインデックスを0リセット
    IF read_index > nArraySize - 1 THEN
        read_index := 0;
    END_IF
    // Buffer使用量カウンタを繰り下げ
    buffer_usage := buffer_usage - 1;
ELSIF bGet THEN
    bError := TRUE;
END_IF
```

このファンクションブロックは次の通り使う事ができます。まずは、処理するデータモデルを構造体で定義します。

```{code} iecst
TYPE User :
STRUCT
    first_name : STRING;
    last_name  : STRING;
    age        : UINT;
END_STRUCT
END_TYPE
```

次のプログラムにより、のび太、ドラえもん、しずちゃんの3名を300msに一度キューに登録し、100msに一回ひとりづつキューから取り出してoutputに書き込みます。

```{code} iecst
PROGRAM MAIN
VAR CONSTANT
    BUFFER_SIZE : UINT := 100;
END_VAR
VAR
    Users : ARRAY [1..BUFFER_SIZE] OF User;
    Nobita_kun : User := (first_name := 'Nobita', last_name := 'Nobi', age := 10);
    Doraemon : User := (first_name := 'Doraemon', last_name := 'Nobi', age := 2433);
    Shizu_chan : User := (first_name := 'Shizuka', last_name := 'Minamoto', age := 10);
    fb_deque : FB_deque;
    write_trigger : TON;
    read_trigger : TON;
    output : User;
END_VAR

// キューインみトリガ
write_trigger(IN := NOT write_trigger.Q, PT := T#300MS);
// キューアウトトリガ
read_trigger(IN := NOT read_trigger.Q, PT := T#100MS);

// キューイン
fb_deque(
    pArrayData := ADR(Users),
    pData := ADR(Nobita_kun),
    cbData := SIZEOF(Nobita_kun),
    nArraySize := BUFFER_SIZE,
    bGet := FALSE,
    bPut := write_trigger.Q
);

fb_deque(
    pArrayData := ADR(Users),
    pData := ADR(Doraemon),
    cbData := SIZEOF(Doraemon),
    nArraySize := BUFFER_SIZE,
    bGet := FALSE,
    bPut := write_trigger.Q
);

fb_deque(
    pArrayData := ADR(Users),
    pData := ADR(Shizu_chan),
    cbData := SIZEOF(Shizu_chan),
    nArraySize := BUFFER_SIZE,
    bGet := FALSE,
    bPut := write_trigger.Q
);

// キューアウト
fb_deque(
    pArrayData := ADR(Users),
    pData := ADR(output),
    cbData := SIZEOF(output),
    nArraySize := BUFFER_SIZE,
    bPut := FALSE,
    bGet := read_trigger.Q
);
```

```{note}
今回は、サンプルコード紹介する際の見せ方の都合で、キューイン、キューアウトともにファンクションブロック本体に記述してbPut, bGetの入力変数で制御していますが、変数状態によっては両方動作してしまう事で書込みデータを破壊する恐れがあります。よって、より望ましいのはメソッドで処理していただいた方が安全です。
```


