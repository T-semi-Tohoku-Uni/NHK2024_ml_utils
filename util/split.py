import os
import argparse
import shutil
from glob import glob

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--datasets', required=True, help='path of dataset dir')
    parser.add_argument('--image', required=True, help='path of output dir')
    parser.add_argument('--box', required=True, help='path of output dir')
    args = parser.parse_args()
    
    datasets_path = args.datasets
    image_path = os.path.join(datasets_path, args.image)
    bounding_box_path = os.path.join(datasets_path, args.box)

    # Create target directory
    if not os.path.exists(datasets_path):
        os.makedirs(datasets_path)
    if not os.path.exists(datasets_path + '/trains'):
        os.makedirs(datasets_path + '/trains')
    if not os.path.exists(datasets_path + '/val'):
        os.makedirs(datasets_path + '/val')

    target_dirs = {'trains': 0.9, 'val': 0.1, 'test': 0}

    # ファイルリストの取得
    img_files = glob(f'{image_path}/*.jpg')
    annot_files = glob(f'{bounding_box_path}/*.txt')

    # ファイル名でマップを作成
    img_files_map = {os.path.splitext(os.path.basename(x))[0]: x for x in img_files}
    annot_files_map = {os.path.splitext(os.path.basename(x))[0]: x for x in annot_files}

    pairs = [(img_files_map[key], annot_files_map[key]) for key in img_files_map if key in annot_files_map]

    # 分割点の計算
    num_train = int(len(pairs) * target_dirs['trains'])
    num_val = int(len(pairs) * target_dirs['val'])

    # データの分割
    train_pairs = pairs[:num_train]
    val_pairs = pairs[num_train:num_train + num_val]
    test_pairs = pairs[num_train + num_val:]

    # 各セットのファイルを対応するディレクトリにコピー
    for set_name, dataset in [(os.path.join(datasets_path, "trains"), train_pairs), (os.path.join(datasets_path, "val"), val_pairs)]:
        for img_path, annot_path in dataset:
            shutil.copy(img_path, set_name)
            shutil.copy(annot_path, set_name)