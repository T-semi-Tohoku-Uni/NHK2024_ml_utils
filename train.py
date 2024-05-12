from ultralytics import YOLO
import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True, help='path of model dir')
    args = parser.parse_args()
    
    model_path = args.model
    
    save_dir = "./run"
    os.makedirs(save_dir, exist_ok=True)
    
    model = YOLO(model_path)  # Load model
    model.train(
        data='yolo.yaml',
        epochs=500, 
        batch=16,
        project=save_dir,
    )