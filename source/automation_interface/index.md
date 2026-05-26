TwinCATプロジェクトの構成とXARへの反映をAPIベースで操作する機能としてAutomation Interfaceというものがあります。
VisualStudioが持っている機能を使っているのですが、WindowsのCOMインターフェースを使ってTwinCATプロジェクト構成を操作するAPIが用意されています。

下記リンクのとおり、.NET, C++, Powershell, IronPython を使ってプロラムすることが可能です。

https://infosys.beckhoff.com/content/1033/tc3_automationinterface/242682763.html?id=5107059583047685772

達成している挙動はEtherCATサブデバイスの無効化とは異なりますが、
C#によるサンプルコードは以下で提供されています。
https://github.com/Beckhoff/TC_AI_DOTNET_Samples



まず、下記サイトの中盤にあります通り、構成済みのEtherCATマスターの階層にてITcSmTreeItem型のオブジェクトを取得します。

ITcSmTreeItem item = sysMan.LookupTreeItem("TIID^EtherCAT Master");
https://infosys.beckhoff.com/content/1033/tc3_automationinterface/242933643.html?id=4059804390998680177

上記の例ではDisableに設定しているだけですが、上記オブジェクトのITcSmTreeItem::ExportChildメソッドを実行すればxtiファイルは保存できると考えられます。
https://infosys.beckhoff.com/content/1033/tc3_automationinterface/242840459.html?id=7657667301273650622

逆に構成を再現するには、
1.	下記サイトの通りEtherCATマスタを構成してITcSmTreeItemオブジェクトを取得し、
https://infosys.beckhoff.com/content/1033/tc3_automationinterface/242737035.html?id=1036556170618907833
2.	ITcSmTreeItem::ImportChildを使って保存したxtiファイルをインポートする
https://infosys.beckhoff.com/content/1033/tc3_automationinterface/242838923.html?id=1721855962718315360
