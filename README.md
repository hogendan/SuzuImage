# SuzuImage
Import image file list and Preview image file in list files.

# Github
https://github.com/hogendan/SuzuImage

# 環境構築
前提条件: python3 がインストールされている

## 仮想環境
    1. cd [インストールフォルダ]\SuzuImange
    2. python -m venv [env名]
## ライブラリ
    - pip install -U django-imagekit

# 実行方法
    1. cd D:\Programs\SuzuImange
    2. .\env\Scripts\activate
    3. python manage.py runserver
    4. http://127.0.0.1:8000/imagelist/

# アプリ機能説明
## 画像一覧表示
画像ファイルパスが記載されたファイルをインポートして画像一覧を表示する

## 画像ファイルマージ
複数の画像ファイルリストから画像を選択し、新しい画像ファイルリストを作成する

## ファイル管理
- 画像ファイルリストを削除する
- ローカルフォルダに保存されたサムネイル画像を全クリアする