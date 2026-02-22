# Image EXIF Adder for mac
## EXIF情報を追加した1:1の画像を作成するアプリケーション

#### ディレクトリ構成
```
image/
├── test/
│   ├── single.py
│   ├── multi.py
│   ├── EXIF.py
│   ├── path.py
│   └── create_image.py
│
├── image/
│   ├── image.jpg
│   ├── image1.jpg
│   │── image2.jpg
│   │      ...
│   └── image-n.jpg
│
├── src/
│   ├── main.py
│   ├── process.py
│   ├── EXIF.py
│   ├── path.py
│   ├── interface.py
│   └── create_image.py
│
└── output/
```

#### 実行スクリプト一覧
- single.py
    相対パスを指定した一枚の画像に対して処理を実行

    ```
    python single.py
    ```

- multi.py
    相対パスを指定したディレクトリ内の全ての画像に対して処理を実行
    ```terminal
    python single.py
    ```

- src/main.py
    GUIによりディレクトリの選択が可能
    画像ディレクトリおよび出力ディレクトリを選択することで、画像ディレクトリ内の全ての画像に対して処理がなされる。
    出力ディレクトリに処理を終えた画像が保存される。
    ```terminal
    python GUI/main.py
    ```



#### 出力EXIF情報
- [x] 日付
- [ ] 時間
- [x] カメラ機種名
- [x] 焦点距離
- [x] ISO感度
- [x] シャッタースピード
- [x] F値
