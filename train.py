from ultralytics import YOLO
import os

if __name__ == "__main__":
    
    save_dir = "./run"
    os.makedirs(save_dir, exist_ok=True)
    
    model = YOLO('yolov8s.pt')  # Load model
    model.train(
        data='yolo.yaml',
        epochs=500, 
        batch=16,
        project=save_dir,
    )