from ultralytics import YOLO
from core.marking import *
from core.packing import *
import os
import random
import shutil
from PIL import Image
import matplotlib.pyplot as plt
import threading

class TeaDeer:
    def __init__(self):
        self.model = None

    def load(self, path):
        self.model = YOLO(path)

    def detect(self, source, stream=False, ):
        if not self.model:
            raise 'Model not loaded!'
        sort(self.model(source, imgsz=1280, conf=0.5, stream=stream))
        return self.model(source, imgsz=1280, conf=0.5, stream=stream)

    def plot(self, result):
        im_bgr = result.plot()
        im_rgb = Image.fromarray(im_bgr[..., ::-1])
        plt.axis('off')
        plt.imshow(im_rgb)
        plt.show()

    def markDrafts(self, directory, save_directory):
        for root, dirs, files in os.walk(directory):
            _class = os.path.basename(root)
            for file in files:
                try:
                    full_path = os.path.join(root, file)
                    if get_file_type(full_path) == 'img':
                        print(f"✨ Processing 🏙️ image {_class} in {full_path}")
                        threading.Thread(target=markImage, args=(_class, full_path, save_directory)).start()
                    elif get_file_type(full_path) == 'vid':
                        print(f"✨ Processing 📹 video {_class} in {full_path}")
                        threading.Thread(target=markVideo, args=(_class, full_path, save_directory)).start()
                    else:
                        raise NameError('Unknown file format')
                except:
                    print(f"⚠️ File has an unknown format or is damaged!")
    def splitDataset(self, base_path, train_ratio=0.7, val_ratio=0.15, seed=62):
        random.seed(seed)
        images_path = os.path.join(base_path, "images")
        labels_path = os.path.join(base_path, "labels")

        for set_type in ["train", "val"]:
            for content_type in ["images", "labels"]:
                os.makedirs(os.path.join(base_path, set_type, content_type), exist_ok=True)

        all_files = [
            f for f in os.listdir(images_path) if os.path.isfile(os.path.join(images_path, f))
        ]
        random.shuffle(all_files)

        total_files = len(all_files)
        train_end = int(train_ratio * total_files)
        val_end = train_end + int(val_ratio * total_files)

        train_files = all_files[:train_end]
        val_files = all_files[train_end:val_end]

        def copy_files(files, set_type):
            for file in files:
                shutil.copy(os.path.join(images_path, file), os.path.join(base_path, set_type, "images"))
                label_file = file.rsplit(".", 1)[0] + ".txt"
                shutil.copy(os.path.join(labels_path, label_file),os.path.join(base_path, set_type, "labels"),)

        copy_files(train_files, "train")
        copy_files(val_files, "val")

        print("🪄 Dataset successfully split into train and val sets.")