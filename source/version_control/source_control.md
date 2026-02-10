(section_install_git)=
# 導入

[InfoSys サイトリンク](https://infosys.beckhoff.com/content/1033/tc3_sourcecontrol/index.html?id=6468228250695776754)

## GITのインストール

[https://git-scm.com/install/windows](https://git-scm.com/install/windows) からインストーラをダウンロードしてインストールするか、管理者権限でターミナルを起動してWingetを使ったインストールを行ってください。

```{code} powershell
winget install --id Git.Git -e --source winget
```

## Git初期設定

Gitのインストールが終わったら初期設定を行います。

まず、あなたの著者としてユーザ名とメールアドレスを設定します。これは、gitの変更履歴に記録される変更を行った開発者の名前として使用されます。

ターミナルを起動して以下のコマンドを順次入力してください。

```{code} powershell
git config --global user.name "あなたの名前（ニックネームも可）"
```

```{code} powershell
git config --global user.email "あなたのメールアドレス"
```

新規作成するリポジトリの既定ブランチ名を main に設定します。公開リポジトリも幹は `main` ブランチですので、`main` と設定します。

```{code} powershell
git config --global init.defaultBranch main
```

```{admonition} Git用Windows向けクライアントソフト TortoiseGit のご紹介
Gitをインストールしただけですと、原則CUI（コマンドユーザインターフェース）のみの機能が提供されます。Windowsエクスプローラに紐づいてGitの操作を行う便利なヘルパーソフトもありますので、必要に応じて以下のリンクからインストールしてください。

[https://tortoisegit.org/](https://tortoisegit.org/)
```

## TwinCATの設定

1. TwinCAT XAEを立ち上げ、`Tools` > `Options` を開きます。ツリーメニューの、 `TwinCAT` > `XAE Environment` > `File settings` を開き、 `Enable Multiple Project Files` を `True` にします。

    ![](assets/2023-05-23-23-10-38.png){width=600px align=center}

2. 続いて `Source Control` > `Plug-in Slection` にて、`Current source control plug-in` を、 `Git` に設定します。

    ![](assets/2023-05-23-23-17-46.png){width=600px align=center}

