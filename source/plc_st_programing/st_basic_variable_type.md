```{role} iecst(code)
   :language: iecst
```

# 変数の型

IEC 61131-3で使用できる変数の標準型（プリミティブ型）は以下をご覧ください。

[https://infosys.beckhoff.com/content/1033/tcplccontrol/925423371.html?id=173322321907090634](https://infosys.beckhoff.com/content/1033/tcplccontrol/925423371.html?id=173322321907090634)


```{csv-table}
:header: 型,サイズ,リテラル最小値,リテラル最大値

BOOL,1,{iecst}`FALSE`,{iecst}`TRUE`
BYTE,1,$0$,$255$
WORD,2,$-32768$,$32768$
DWORD,4,$0$,$4294967295$
SINT,1,$-128$,$128$
USINT,1,$0$,$255$
INT,2,$-32768$,$32767$
UINT,2,$0$,$65535$
DINT,4,$-2147483648$,$2147483647$
UDINT,4,$0$,$4294967295$
REAL,4,$-3.402823 \times 10^{38}$,$3.402823 \times 10^{38}$
LREAL,8,$-1.79769313486231 \times 10 ^{308}$,$1.79769313486232 \times 10^{308}$
STRING,81 [^f1] ,シングルコーテーションで囲った文字列 [^f2],
TIME,4,{iecst}`T#0ms`,{iecst}`T#71582m47s295ms`
TIME_OF_DAY (TOD),4,{iecst}`TOD#00:00`,{iecst}`TOD#1193:02:47.295`
DATE,4,{iecst}`D#1970-01-01`,{iecst}`D#2106-02-06`
DATE_AND_TIME (DT),4,{iecst}`DT#1970-01-01-00:00`,{iecst}`DT#2106-02-06-06:28:15`
```


[^f1]: デフォルトの占有サイズ。{iecst}`STRING(255)` のように、型宣言に続く小括弧でバイトサイズを指定。占有メモリサイズは指定サイズに加えてNULL文字の1バイトが確保される。
[^f2]: 指定サイズ（デフォルト半角80文字）が最大格納文字。確保されたデータの最終には必ずNULLが付加される。

## ユーザ定義型

ユーザ定義型には次の種類があります。

[https://infosys.beckhoff.com/content/1033/tcplccontrol/925468811.html?id=1593624705725169244](https://infosys.beckhoff.com/content/1033/tcplccontrol/925468811.html?id=1593624705725169244)

### ARRAY

同じ型のものを指定した型の配列。下記例では1から3の要素番号でアクセスできる3個の`UDINT`型のメモリが確保されます。初期化は大括弧で囲ったカンマ区切りで全要素値を指定します。

```{code-block} iecst
aValues : ARRAY [1..3] OF UDINT := [1,2,3];
```

値を代入する場合には、`配列名[要素番号]` のように大括弧で括った整数で要素番号を指定して要素へアクセスします。

```{code-block} iecst
aValues[2] := 300; // aValuesの値は [1,300,3] となる
```

2次元以上の配列を組むことも可能です。方法は次の二つがあります。

2次元配列方式
    : 列がメモリ上連続したアドレス上に配置されるため初期化時には連続した配列を与えます。

配列の配列
    : 配列内に名前なし配列が作成されるデータモデルです。初期化時は入れ子の配列を指定します。


```{code-block} iecst
VAR
    aPoints : ARRAY[1..2,1..3] OF INT := [1,2,3,4,5,6];
    a2Boxes : ARRAY[1..2] OF ARRAY[1..3] OF INT := [ [1, 2, 3], [ 4, 5, 6]];
END_VAR
```

アクセス方法は次の通りの違いがあります。

```{code-block} iecst
aPoints[1, 2] := 1200;
a2Boxes[1][2] := 1200;
```

次のとおり値がセットされます。

![](https://infosys.beckhoff.com/content/1033/tc3_plc_intro/Images/png/8826246923__Web.png){align=center}

### POINTER

ポインタとは任意の変数のアドレスと型情報を保持する型です。次の例では、変数Aのポインタを保持する変数Bによるプロラム例です。

8行目、`変数B := ADR(変数A);`にて変数Bに変数Aのポインタにセットしています。9行目ではポインタ変数に`^`を付加することでデリファレンス（実変数へアクセス）し、この値を変数Cに代入しています。

その後、ポインタ変数Bへのデリファレンスに別の値5を代入すると、実際は変数Aに対して5を代入していることと同じになります。

```{code-block} iecst
:caption: 変数Aのメモリアドレスを変数Bに代入
:linenos:

VAR
    変数A : INT;
    変数B : POINTER TO INT;
    変数C : INT;
END_VAR

変数A := 3;
変数B := ADR(変数A); // 変数A = 3, 変数B^ = 3
変数C := 変数B^;     // 変数A = 3, 変数B^ = 3, 変数C = 3
変数B^ := 5;         // 変数A = 5, 変数B^ = 5, 変数C = 3
```

ポインタ型変数は、`ADR()` による実変数のメモリアドレスと型情報を保持できる変数です。メモリアドレスだけを格納する型は`PVOID` となります。


```{code-block} iecst
:caption: 変数のアドレスを格納する汎用型PVOID
:linenos:

VAR
    counter 
    p_counter : 
    len_counter : UDINT;
END_VAR
```

### ENUMERATION

### STRUCTURE

### REFERENCE

参照とは、実体のある変数に対するショートカットのようなものです。詳細は{ref}`section_reference_assignment` で説明します。下記の例のとおり、変数Bは変数Aの参照（ショートカット）となっています。宣言時は未定義ですが、プログラム中で変数Aに対する参照設定を`REF=`代入演算子を使って行います。この結果、参照変数Bの値を変更するとその元となる変数Aも連動して値が変化します。

```{code-block} iecst
VAR
    変数A : INT;
    変数B : REFERENCE TO INT;
    変数C : INT;
END_VAR

変数A := 3;
変数B REF= 変数A; // 変数A = 3, 変数B = 3
変数C := 変数B;   // 変数A = 3, 変数B = 3, 変数C = 3
変数B := 5; 　　　// 変数A = 5, 変数B = 5, 変数C = 3
```


### Subrange
