# NHK2024_ml_utils
アノテーションする際のユーティリティー

## 注意
大きなデータ（データセットの画像, モデルのパラメータファイルなどなど）は`data/`以下においてください. 大きなデータをgithubにpushすると怒られるので. `data/`は`.gitignore`で除外しています. 

## モデルを学習させる
学習用にyolo.yamlファイルを作成する. 内容は, ディレクトリのパスとラベルを書くだけ.
```
yolo detect train data=yolo.yaml model=yolov8s.pt epochs=100 imgsz=640 device=0 batch=64
```

## 画像ファイル名をユニークにする
realsenseで取得した生の画像データのファイル名を被らないようにユニークにする. \
オプションの指定方法
- `raw`: 生の画像のディレクトリのパス 
- `output`: ラベリングした画像の保存先
```
python3 util/add_label.py --raw=data --output=image
```

## TrainデータとValidationデータに分割する
`labelimg`では画像ファイルとアノテーションしたテキストファイルが別々に保存されている.
YOLOに食わせる時はこれを学習用と評価用のデータに分けないと行けない. 

オプションの指定方法
- `image` : 画像のディレクトリのパス
- `teacher` : 教師データ（bounding boxをつけたやつ）を保存しているパス
- `output`: 出力先のディレクトリ. ここに`train`と`val`が全データの`9`:`1`の割合でランダムに生成される. 
```
python3 util/split.py --image=datasets/image --teacher=datasets/teacher --output=datasets/
```

## 教師データの自動生成
