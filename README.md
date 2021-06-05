# PySimpleNotePad

勉強用に作成したメモ帳アプリです。

このリポジトリをクローンし、以下の手順を実行すれば実行ファイル化(exe化)して使用することも可能です。

なお、pyinstallerを使用した際に「ファイルにアクセスできません」というエラーが出る場合があります。その場合、miniconda(Anaconda)の仮想環境を立ち上げ、以下のコマンドで依存ライブラリをインストールしたのちに作業を行えばビルド可能です。

`conda install -c conda-forge pysimplegui`
`conda install pyinstaller`

仮想環境のPythonのバージョンは、3.9.4で問題なく動作することを確認しています。

## exe化手順

1. クローンしたこのリポジトリまで移動
2. 次のコマンドを実行
   `pyinstaller PySimpleNotePad.py --onefile --noconsole --icon=icon//memo.ico`
3. "dist"フォルダが生成されており、その中にPySimpleNotePad.exeがあることを確認(容量は約11MB)
4. PySimpleNotePadディレクトリに"PySimpleNotePad.spec"というファイルが生成されていることを確認し、
   `pyz = PYZ(a.pure, a.zipped_data, ...` のすぐ上に `a.datas += [("memo.ico", ".\icon\memo.ico", "Data")]`を追加する
5. `pyinstaller PysimpleNotePad.spec` を実行する
6. "dist"フォルダ内の PySimpleNotePad.exeのアイコンが"memo.ico"と同じになっていることを確認する

## 機能

![PySimpleNotePad1](https://github.com/potedo/PySimpleNotePad/blob/image/PySimpleNotePad1.png)
!["PySimpleNotePad](https://github.com/potedo/PySimpleNotePad/blob/image/PySimpleNotePad2.png)