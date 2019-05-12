# 垂れ流し君のアップデート
>関連コマンドは必ず/musicをつけ、引数はすべて半角スペースで区切ること
## 呼び出し

- Botを使用する際はオンラインの状態で必ずこの<font color="Orange">**call**</font>コマンドを使用してボイスチャンネルに呼ぶこと。
**このコマンドを使用しない限り後述のコマンドが使用できないので注意**

		例:/music call

## 音声の再生方法
- ローカルファイルと特定のウェブページからの再生が可能
### ローカルファイル
- ローカルファイル呼び出しの場合<font color="Orange">**local**</font>コマンドを使用しその後に再生する曲の番号を半角で指定する


		例:/music local [再生したい音楽の番号]


- 番号のリストは番号の代わりに<font color="Orange">**list**</font>を指定することでHTML形式で送付され
る

		例:/music local list

### URL
- ウェブ上の動画呼び出しの場合<font color="Orange">**url**</font>コマンドを使用しその後に再生するURLを指定する

		例:/music url [再生したい動画のURL]

- どのサイトが再生に対応しているかのリストは<font color="Orange">**list**</font>を指定することでHTML形式で送付される

		例:/music url list

	>※主にyoutube、ニコニコ動画、Dropboxの共有リンクが有効
## 一時停止
- 再生中の楽曲を一時停止する場合は<font color="Orange">**pause**</font>コマンドを利用する

		例:/music pause

## 再開
- pauseコマンドで一時停止させてた楽曲を再開させる場合<font color="Orange">**resume**</font>コマンドを利用する

		例:/music resume

## 次の曲を再生
- 現在の曲を中断し、次の曲を再生する場合は<font color="Orange">**skip**</font>コマンドを利用する

		例:/music skip

## 再生中の曲名を取得
- 現在再生している楽曲のタイトル、URLを表示する場合は<font color="Orange">**current**</font>コマンドを利用する

		例:/music current

## 再生待ちのリストを取得
- 再生予定の楽曲タイトル、URLを表示する場合は<font color="Orange">**list**</font>コマンドを利用する

		例:/music list