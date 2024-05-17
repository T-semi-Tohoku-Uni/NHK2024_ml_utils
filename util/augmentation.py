import os
from PIL import Image
import argparse

def adjust_box(annotation_lines):
    adjusted_lines = []
    for line in annotation_lines:
        parts = line.split()
        if len(parts) == 5:
            cls, x, y, w, h = parts
            x = 1 - float(x)
            y = 1 - float(y)
            adjusted_lines.append(f"{cls} {x} {y} {w} {h}\n")
    return adjusted_lines

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True, help="base directory")
    parser.add_argument("--image", required=True, help="image directory")
    parser.add_argument("--box", required=True, help="bounding box directory")
    args = parser.parse_args()

    base_path = args.base
    image_path = os.path.join(base_path, args.image)
    box_path = os.path.join(base_path, args.box)

    image_files = [f for f in os.listdir(image_path) if os.path.isfile(os.path.join(image_path, f)) and f.lower().endswith(('.png', '.jpg', 'jpeg'))]

    for image_file in image_files:
        filename = os.path.splitext(image_file)[0]
        image_file_path = os.path.join(image_path, image_file)
        box_file_path = os.path.join(box_path, filename + ".txt")

        if not os.path.exists(box_file_path):
            continue
        
        with Image.open(image_file_path) as img:
            rotated_img = img.rotate(180)
            rotated_iamge_path = os.path.join(image_path, filename + "_rotated.jpg")
            rotated_img.save(rotated_iamge_path)

            rotated_box_path = os.path.join(box_path, filename + "_rotated.txt")
            with open(box_file_path, "r") as f:
                annotation = f.read()
            
            adjusted_lines = adjust_box(annotation.split("\n"))

            with open(rotated_box_path, "w") as rotated_box_file:
                print(adjusted_lines)
                rotated_box_file.writelines(adjusted_lines)