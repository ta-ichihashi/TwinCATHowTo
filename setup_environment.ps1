$OutputEncoding = [Text.Encoding]::UTF8
# install scoop
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser # Optional: Needed to run a remote script the first time
irm get.scoop.sh | iex

# git インストール
scoop install git

# git の初期設定
$username = Read-Host "ユーザ名を半角英数で入力してください >"
$emailaddr = Read-Host "メールアドレスを半角英数で入力してください >"

git config --global user.name $username
git config --global user.email $emailaddr
git config --global core.editor 'code --wait'
git config --global init.defaultBranch main

# versions bucketの追加
scoop bucket add versions
scoop bucket add extras

# python インストール
scoop install python vscode

# vs-code extension インストール
code --install-extension ExecutableBookProject.myst-highlight
code --install-extension mushan.vscode-paste-image

# python 初期セットアップ
pip install wheel
python -m pip install --upgrade pip
