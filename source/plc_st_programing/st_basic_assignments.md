# 代入文

ST言語における代入式について説明します。

## 値の代入

値の代入を行う代入式は次のとおりとなります。

```{code-block} iecst
:caption: 代入式

代入先変数 := 代入元変数;   // 値の代入
代入元変数 => 代入先変数;   // 値の代入
```

これは、代入元、代入先それぞれにメモリ領域が確保されていて、その中身の値が代入によって **コピー** されています。

(section_reference_assignment)=
## 参照の代入

参照型とは、実体のある変数に対するショートカットのようなものです。このショートカットに対して実体のある変数へのリンクを代入することで、ショートカットを通じて様々な処理を行うことが可能です。

参照型変数へのリンクを設定する代入式として `REF=` があります。この代入はあくまでもショートカットのリンクを設定するだけですから、値の代入とは違ってメモリの内容をコピーしている訳ではないことに留意してください。

```{code-block} iecst
:caption: 参照型変数の代入式
VAR
    代入元変数 : INT;
    INT型の参照変数 : REFERENCE TO INT; // 参照型変数
END_VAR

INT型の参照変数 REF= 代入元変数; // 代入元変数へのショートカットリンクが設定される
```

具体例のプログラムはつぎの通りです。`ref_counter` は `counter` の参照として設定します。その後、参照変数の値を変更すると、参照元の `counter` が影響を受けていることがわかります。

```{code-block} iecst
:emphasize-lines: 8
PROGRAM MAIN
VAR
    counter : INT;
    ref_counter : REFERENCE TO INT;
END_VAR

counter := 1;
ref_counter REF= counter;
ref_counter := ref_counter + 1;
// ref_counterはcounterへの参照なので、counterもref_counterも値は2になっている
```

プログラム内で参照を代入する場合は `REF=` を使用するのですが、関数やメソッド、入力変数等の引数（VAR_INPUT）に参照型変数が宣言されている場合、この引数に代入する場合は `:=` を使用します。

下記の例は、引数に与えた`INT`型の変数を参照型として受け取り、1加算するファンクションです。

```{code-block} iecst
FUNCTION F_AddOne : BOOL
VAR_INPUT
    iValue : REFERENCE TO INT;
END_VAR

iValue := iValue + 1;
```

このファンクションを用いたプログラム例は次のとおりです。この例のとおり、`F_AddOne`関数の入力変数 `iValue` は `REFERENCE TO` として宣言された参照型変数ですが、引数として値を渡す場合には`:=`を使用します。

```{code-block} iecst
:linenos:
:emphasize-lines: 8, 14
PROGRAM MAIN
VAR
    counter : INT;
    ref_counter : REFERENCE TO INT;
END_VAR

counter := 1;
F_AddOne(iValue := counter); // iValueは参照型だが := で代入する。
// counterへの参照を使って加算したのでcounterの値は2になっている

ref_counter REF= counter;    // 引数ではないプログラム中の代入では REF= とする。
// ref_counterはcounterに対するショートカット。値は2が入っている。

F_AddOne(iValue := ref_counter); // 参照型は通常の変数のように渡すことができる
// ref_counterはcounterへの参照なので、counterもref_counterも値は3になっている
```

11 行目に見られるように、プログラム内で参照型変数に参照を代入する場合、`REF=` を用います。ここで `ref_counter` という参照型の変数に対して、`counter` の参照を渡しています。

参照型変数は元の型（INT）と同様に使用することができます。14行目に見られるように`ref_counter`を`F_AddOne`関数に渡しています。

````{admonition} __ISVALIDREF() を使って参照定義済みかチェックを行う
:class: important

`REFERENCE TO` で定義した参照型変数に参照を設定する前に使用するとページフォルトとなりプログラムが異常停止してしまいます。このため、参照型変数を使用する個所では `__ISVALIDREF()` 関数によりその参照が定義済みかどうかチェックして、必要があります。

上記プログラム例では説明の都合上省きましたが、正しくは次の通り定義する必要があります。


```{code-block} iecst
:emphasize-lines: 6-8
FUNCTION F_AddOne : BOOL
VAR_INPUT
    iValue : REFERENCE TO INT;
END_VAR

IF NOT __ISVALIDREF(iValue) THEN
    RETURN; // iValueが未設定参照であればこれ以後実行しない
END_IF

iValue := iValue + 1;
```
````

## SETとRESET

代入先がBOOL型変数の場合、SETやRESET構文も用意されています。

SET
    : 評価式がFALSE > TRUEへの立ち上がりエッジの場合に代入先変数を **TRUE** へ変化させる。
      ```{code-block} iecst
      代入先変数 S= 評価式;
      ```
RESET
    : 評価式がFALSE > TRUEへの立ち上がりエッジの場合に代入先変数を **FALSE** へ変化させる。
      ```{code-block} iecst
      代入先変数 R= 評価式;
      ```

