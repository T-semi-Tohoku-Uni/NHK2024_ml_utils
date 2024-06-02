# NHK2024_ml_utils
アノテーションする際のユーティリティー

# 学習の流れ
まず, 画像ファイル名のファイル名をユニークにして, `datasets/image`ディレクトリに保存する. 
```
python3 util/add_label.py --raw=data --base=datasets/red --output=image
```
その後, 現在のモデルを使用して自動でアノテーションを行う.
```
python3 util/auto_anotation.py --image=datasets/silo/image/ --box=datasets/silo/box --model=... --ratio=10
```
`labelImg`を使って手動でチェックする. 
自動アノテーションをしたデータをサーバーからローカルに持ってくる方法
```
sftp ユーザー名@ホスト名
> get サーバーのパス ローカルのパス
```

zipファイルに保存する前に, data argumantしたものを削除
```
python3 util/delete_rotated.py --datasets=datasets/...
```


アノテーションが完了したら, 画像とアノテーションのテキストファイルをzipファイルに保存する.
```
zip -r datasets.zip datasets/
```

画像を180度回転させたデータも学習データとして扱う
```
python3 util/augmentation.py --base=datasets/silo --image=image --box=box
```

データセットを, 学習用と検証用のデータセットに分割する.
```
python3 util/split.py --datasets=datasets --image=image --box=box
```

最後にモデルを再学習させる
```
python3 train.py --model=yolov8s.pt --yaml=settings/red_model.yaml 
```
学習結果は`run`ディレクトリに格納される.

学習が終わったら, `bets.pt`を対象のリポジトにアップロード, データセットのzipファイルをgithubのrelease機能を使ってアップロードする.

### 青と紫のデータセットを学習させる場合
まず`data`ディレクトリに追加で学習するデータをおく.
次のコマンドを実行
```
python3 util/add_label.py --raw=data --base=datasets/blue --output=image
```
```
python3 util/auto_anotation.py --image=datasets/blue/image/ --box=datasets/blue/box --model=NHK2024_blue_ball_model/blue_ball_model.pt --ratio=10
```
頑張ってアノテーションする

前回のデータと統合した後
```
python3 util/augmentation.py --base=datasets/blue --image=image --box=box
```
```
python3 util/split.py --datasets=datasets/blue --image=image --box=box
```
```
python3 train.py --model=yolov8s.pt --yaml=settings/blue_model.yaml 
```

# それぞれのプログラムの使いかた

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
