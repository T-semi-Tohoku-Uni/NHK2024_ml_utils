from ultralytics import YOLO
import argparse
import os
import shutil

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('image', help='path of dataset dir')
    parser.add_argument('box', help='path of save dif')
    parser.add_argument('model', help='path of model dir')
    args = parser.parse_args()
    
    image_path = args.image
    box_path = args.box
    model_path = args.model
        
    # load model
    model = YOLO(model_path)
    
    # datasets_dirの中にあるファイルを全て取り出す
    for filename in os.listdir(image_path):
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
        
        with open(save_txt_path, "w") as f:
          for index, cls in enumerate(classes):
            f.write(f"{int(cls)} {(boxes.xywhn[index][0])} {boxes.xywhn[index][1]} {boxes.xywhn[index][2]} {boxes.xywhn[index][3]}\n")
        
    # create classes.txt
    with open(os.path.join(box_path, "classes.txt"), "w") as f:
        for value in model.names.values():
            f.write(value + '\n')