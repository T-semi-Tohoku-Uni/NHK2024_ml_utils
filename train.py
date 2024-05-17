from ultralytics import YOLO
import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True, help='path of model dir')
    parser.add_argument('--yaml', required=True, help='path of yaml file')
    args = parser.parse_args()
    
    model_path = args.model
    yaml_path = args.yaml
    
    save_dir = "./run"
    os.makedirs(save_dir, exist_ok=True)
    
    model = YOLO(model_path)  # Load model
    model.train(
        data=yaml_path,
        epochs=2000, 
        batch=48,
        project=save_dir,
    )