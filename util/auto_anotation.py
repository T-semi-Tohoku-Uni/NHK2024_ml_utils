from ultralytics import YOLO
import argparse
import os
import shutil

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--image' ,required=True, help='path of dataset dir')
    parser.add_argument('--box' ,required=True, help='path of save dif')
    parser.add_argument('--model' ,required=True, help='path of model dir')
    parser.add_argument('--ratio', required=True, help='ratio of train and val')
    args = parser.parse_args()
    
    image_path = args.image
    box_path = args.box
    model_path = args.model
    ratio = args.ratio

    data_cnt = 0
        
    # load model
    model = YOLO(model_path)
    
    # datasets_dirの中にあるファイルを全て取り出す
    for filename in os.listdir(image_path):
        try:
            file_path = os.path.join(image_path, filename)
            
            # YOLO
            results = model.predict(file_path)
            
            # # save_dirに保存
            output_filename = os.path.splitext(filename)[0] + ".txt"
            save_txt_path = os.path.join(box_path, output_filename)
            
            classes = results[0].boxes.cls
            boxes = results[0].boxes
            
            print(classes)
            print(boxes.xyxy)

            # もしclassesが空 or いらないファイルなら、txtファイルを作成せずに、画像ファイルを削除する
            data_cnt += 1
            if len(classes) == 0 or not data_cnt % int(ratio) == 0:
                os.remove(file_path)
                continue
            
            with open(save_txt_path, "w") as f:
                for index, cls in enumerate(classes):
                    f.write(f"{int(cls)} {(boxes.xywhn[index][0])} {boxes.xywhn[index][1]} {boxes.xywhn[index][2]} {boxes.xywhn[index][3]}\n")

        except Exception as e:
            os.remove(file_path)
            print(e)
            print(f"Error: {file_path}")
            continue
        
    # create classes.txt
    print(model.names)
    with open(os.path.join(box_path, "classes.txt"), "a") as f:
        for value in model.names.values():
            f.write(value + '\n')