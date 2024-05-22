import os
import shutil
from datetime import datetime
import time
import argparse

def add_timestamp_to_filename():
    if not hasattr(add_timestamp_to_filename, "cnt"):
        add_timestamp_to_filename.cnt = 0  # counterが未定義の場合に初期化
    timestamp = time.time()
    new_file_name = f"{timestamp}_{add_timestamp_to_filename.cnt}.jpg"
    add_timestamp_to_filename.cnt += 1
    return new_file_name

def create_name_with_timestamp(s_dir, output_dir):
    for filename in os.listdir(s_dir):
        file_or_dir_path = os.path.join(s_dir, filename)
        
        if os.path.isfile(file_or_dir_path):
            new_file_name = add_timestamp_to_filename()
            if not (file_or_dir_path.endswith("jpeg") or file_or_dir_path.endswith("jpg")):
                continue
            shutil.copy(file_or_dir_path, os.path.join(output_dir, new_file_name))
        else:
            if ignore_frame in file_or_dir_path:
                print(file_or_dir_path)
                continue
            create_name_with_timestamp(file_or_dir_path, output_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", required=True, help="raw image data directory")
    parser.add_argument("--base", required=True, help="base directory")
    parser.add_argument("--output", required=True, help="target directory")
    
    ignore_frame = "depth_frame"
    
    args = parser.parse_args()
    raw_image_data_dir = args.raw
    base_dir = args.base
    output_dir = os.path.join(base_dir,args.output)
    
    # create output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # create box dir to save bounding box text file
    if not os.path.exists(os.path.join(base_dir, "box")):
        os.makedirs(os.path.join(base_dir, "box"))
    
    create_name_with_timestamp(raw_image_data_dir, output_dir)