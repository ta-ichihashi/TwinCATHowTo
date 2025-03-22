Param(
   [switch]$gitonly,
   [switch]$includelatex,
   [switch]$tcconfig
)

$OutputEncoding = [Text.Encoding]::UTF8

# install scoop
gcm scoop -ea SilentlyContinue | Out-Null

if ($? -ne $true) {
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser # Optional: Needed to run a remote script the first time
   irm get.scoop.sh | iex
}

# git インストール
scoop install git

# git の初期設定
$username = Read-Host "Type user name for git author"
$emailaddr = Read-Host "Type email address for git author"

git config --global user.name $username
git config --global user.email $emailaddr
git config --global core.editor 'code --wait'
git config --global init.defaultBranch main
git config --global --unset credential.helperselector.selected
git config --global credential.helperselector.selected manager-core


## Diff and Merge for TwinCAT
if ($tcconfig) {
   git config --global diff.tool 'TcProjectCompare'
   git config --global difftool.TcProjectCompare.path 'C:/TwinCAT/3.1/Components/TcProjectCompare/TcProjectCompare.exe'
   git config --global difftool.TcProjectCompare.cmd '\"C:/TwinCAT/3.1/Components/TcProjectCompare/TcProjectCompare.exe\" //filel \"$LOCAL\" //filer \"$REMOTE\" //dl  \"$LOCAL\" //dr \"$REMOTE\"  //sc'
   git config --global difftool.TcProjectCompare.keepbackup false
   git config --global difftool.TcProjectCompare.trustExitCode true
   git config --global merge.tool 'TcProjectCompare'
   git config --global mergetool.TcProjectCompare.path 'C:/TwinCAT/3.1/Components/TcProjectCompare/TcProjectCompare.exe'
   git config --global mergetool.TcProjectCompare.cmd '\"C:/TwinCAT/3.1/Components/TcProjectCompare/TcProjectCompare.exe\" //filel \"$LOCAL\" //filer \"$REMOTE\" //filem \"$MERGED\" //dl  \\\"Head: \"$LOCAL\"\\\" //dm  \\\"Result: \"$MERGED\"\\\" //dr \"$REMOTE\" //sc'
   git config --global mergetool.TcProjectCompare.keepbackup false
   git config --global mergetool.TcProjectCompare.trustExitCode true
}

# versions bucketの追加
scoop bucket add versions
scoop bucket add extras

# vscode インストール
scoop install vscode

# vs-code extension インストール
code --install-extension ExecutableBookProject.myst-highlight
code --install-extension mushan.vscode-paste-image

if ( - ! $gitonly) {
   # python インストール
   scoop install uv
   uv sync

   if ($includelatex) {
      # latex インストール
      scoop install latex perl
   }
}


scoop cleanup *
scoop cache rm -rf *
