import numpy as np
import cv2
import torch
import glob as glob
from src.model import create_model

class PlascticBagDetector:
    def __init__(self, model_path, num_classes=2, detection_threshold=0.8):
        self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        #device
        self.model = create_model(num_classes).to(self.device)
        #print(device)
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.eval()
        self.detection_threshold = detection_threshold

    def predict(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32)
        img /= 255.0
        img = np.transpose(img, (2, 0, 1)).astype(np.float)
        img = torch.tensor(img, dtype=torch.float).to(self.device)
        img = torch.unsqueeze(img, 0)
        with torch.no_grad():
            outputs = self.model(img)
        if len(outputs[0]['boxes']) == 0:
            return 0
        boxes = outputs[0]['boxes'].cpu().data.numpy()
        scores = outputs[0]['scores'].cpu().data.numpy()
        boxes = boxes[scores >= self.detection_threshold].astype(np.int32)
        return boxes

def process_video(camera_id, video_path, model, frames=30, save_every=600):
    cap = cv2.VideoCapture(video_path)
    i = -1
    while cap.isOpened():
        ret, img = cap.read()
        i += 1
        if not (ret and img is not None):
            break
        if i % (save_every * fps) == 0:
            num_bags = model.predict(img)
            if num_bags != 0:
                num_bags = len(num_bags)
            r = requests.post("http://127.0.0.1:8000/add_garbage_info", json={
                "camera_id": camera_id,
                "garbage_index": num_bags,
            })


def main_pipeline(model_path, image_path):
    model = PlascticBagDetector(model_path)
    img = cv2.imread(image_path)
    res = model.predict(img)
    if res == 0:
        return 0
    return len(res)