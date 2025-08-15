# パッケージマネージャでオフラインインストールする方法

## オンラインPCでのパッケージのダウンロード

PowerShellなどのコマンドラインインターフェースにて、次のコマンドを発行してください。

1.  インストール可能な代表パッケージ名一覧を出力。

    ```{code} powershell
    PS> tcpkg list -t workload
    ```

2.  この中から必要なパッケージを選択して、次のコマンドによりダウンロードする。

    たとえば、XAEとXARの両方を” C:\home\Administrator\pakages” にダウンロードする場合は以下のコマンド発行します。最初表示が無いまま時間を要しますが根気強く待ってください。
    ```{code} powershell
    PS> tcpkg download TwinCAT.Standard.XAE TwinCAT.Standard.XAR -o "C:\home\Administrator\pakages"
    ```

3.  このpackagesフォルダをUSBメモリ等に入れます。

## オフライン環境のIPCでの作業

次にオフライン環境のIPCにてUSBメモリを挿し、IPC内に展開します。パッケージマネージャの設定にてオフラインパス設定を変更し、そのフォルダからインストールできるようにします。

4. IPCにUSBメモリを挿し、任意のフォルダへコピーします。

    本手順の例では `C:\Users\Administrator\Documents\packages` にコピーしたものとします。

5. パッケージマネージャを起動し、設定画面を開き、`Feeds` タブを選び、左下の `+` アイコンを押します。

    ![](assets/2025-08-15-18-38-10.png){align=center}

6. 追加するFeedの `Name` に適当な名前を付けて、`Feed url..` に `C:\Users\Administrator\Documents\packages` を設定して `Save` ボタンを押します。

    ![](assets/2025-08-15-18-38-53.png){align=center}

7. 追加したFeed以外のEnableのチェックを外し、右下のフロッピーアイコンを押します。

    ![](assets/2025-08-15-18-39-18.png){align=center}

以上です。通常通りのパッケージインストールを実施してください。

```{note}
Feed URLで指定したフォルダを定期的に更新してください。Feed URLで指定したフォルダ内にあるパッケージのみインストール可能です。
```