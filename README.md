# YAML Editor Web

このプログラムは、Flaskを使用してWeb上でYAMLファイルを編集するためのものです。

## 機能

- './'上にある複数のYAMLファイルを選択して編集できます。
- HTML上でファイルを読み出し、テーブルに展開します。
- テーブルを編集して変更内容をYAMLファイルに保存できます。

## 使用方法

1. editor_web.pyと同じ階層にYAMLファイルを保存します。
2. 起動します python editor_web.py
3. ブラウザで http://localhost:5000/ にアクセスします。
4. YAMLファイルを選択し、"Read File"ボタンをクリックしてファイルを読み込みます。
5. 表示されたテーブルで編集を行い、"Write"ボタンをクリックして変更内容を保存します。

## 注意事項
配列には対応していません。
