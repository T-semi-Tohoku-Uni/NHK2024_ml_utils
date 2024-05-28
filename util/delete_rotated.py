import os
import argparse

def delete_rotated_files(dir):
    for filename in os.listdir(dir):
        file_or_dir_path = os.path.join(dir, filename)

        if os.path.isfile(file_or_dir_path):
            if "_rotated" in file_or_dir_path:
                os.remove(file_or_dir_path)
        else:
            delete_rotated_files(file_or_dir_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--datasets", required=True, help="datasets directory")
    args = parser.parse_args()
    datasets_dir = args.datasets

    delete_rotated_files(datasets_dir)