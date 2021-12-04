import numpy as np
import cv2
import torch
import os
import shutil
from base64 import b64encode, b64decode
import json
import requests
from time import sleep
from src.model import create_model
from super_image import EdsrModel, ImageLoader

class TrashInContainerDetector:
    def __init__(self, 
                 model_path_container, 
                 model_path_trash, 
                 num_classes=2, 
                 detection_threshold_container=0.8, 
                 detection_threshold_trash=0.5):
        self.detection_threshold_container = detection_threshold_container
        self.detection_threshold_trash = detection_threshold_trash
        self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

        self.model_containers = create_model(num_classes).to(self.device)
        self.model_containers.load_state_dict(torch.load(model_path_container, map_location=self.device))
        self.model_containers.eval()

        self.model_trash = create_model(num_classes).to(self.device)
        self.model_trash.load_state_dict(torch.load(model_path_trash, map_location=self.device))
        self.model_trash.eval()

        self.model_sr = EdsrModel.from_pretrained('eugenesiow/edsr-base', scale=4)

    def detect_containers(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32)
        img /= 255.0
        img = np.transpose(img, (2, 0, 1)).astype(np.float)
        img = torch.tensor(img, dtype=torch.float).to(self.device)
        img = torch.unsqueeze(img, 0)
        with torch.no_grad():
            outputs = self.model_containers(img)
        if len(outputs[0]['boxes']) == 0:
            return []
        boxes = outputs[0]['boxes'].cpu().data.numpy()
        scores = outputs[0]['scores'].cpu().data.numpy()
        boxes = boxes[scores >= self.detection_threshold_container].astype(np.int32)
        return boxes

    def detect_trash(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32)
        img /= 255.0
        img = np.transpose(img, (2, 0, 1)).astype(np.float)
        img = torch.tensor(img, dtype=torch.float).to(self.device)
        img = torch.unsqueeze(img, 0)
        with torch.no_grad():
            outputs = self.model_trash(img)
        if len(outputs[0]['boxes']) == 0:
            return []
        boxes = outputs[0]['boxes'].cpu().data.numpy()
        scores = outputs[0]['scores'].cpu().data.numpy()
        boxes = boxes[scores >= self.detection_threshold_trash].astype(np.int32)
        return boxes

    def super_resolute(self, img):
        img = torch.from_numpy(np.expand_dims(np.moveaxis(img, -1, 0), axis=0))
        preds = (self.model_sr(img / 255) * 255).detach().cpu().numpy()[0]
        preds = np.moveaxis(preds, 0, -1)
        return preds

    def detect_trash_in_containers(self, img):
        #print(img.shape)
        container_boxes = self.detect_containers(img)
        trash_boxes = []
        container_sizes = []
        for box in container_boxes:
            xmin = box[0]
            ymin = box[1]
            xmax = box[2]
            ymax = box[3]
            box_img = img[ymin:ymax, xmin:xmax, :]
            box_img = self.super_resolute(box_img)
            #print(box_img.shape)
            tmp_trash_boxes = self.detect_trash(box_img)
            trash_boxes.append(tmp_trash_boxes)
            container_sizes.append([box_img.shape[1], box_img.shape[0]])
            '''
            #code for drawing images
            #print(tmp_trash_boxes)
            #print(box_img.shape)
            for trash_box in tmp_trash_boxes:
                #print(trash_box, box_img.shape)
                #return box_img, trash_box
                cv2.imwrite('kek.png', box_img)
                box_img = cv2.imread('kek.png')
                box_img = cv2.rectangle(box_img, (int(trash_box[0]), int(trash_box[1])), (int(trash_box[2]), int(trash_box[3])), (0, 0, 255), 2)
                #return 
            cv2_imshow(box_img)
            '''
        return container_boxes, trash_boxes, container_sizes


class ImageProcessor:
    def __init__(self, 
                 model_path_container,
                 model_path_trash, 
                 num_classes=2, 
                 detection_threshold_container=0.8, 
                 detection_threshold_trash=0.5):
        self.detector = TrashInContainerDetector(model_path_container,
                                                 model_path_trash,
                                                 num_classes,
                                                 detection_threshold_container,
                                                 detection_threshold_trash)
        
    def get_staticticsByImage(self, img_path):
        img = cv2.imread(img_path)
        container_boxes, trash_boxes, container_sizes = self.detector.detect_trash_in_containers(img)
        result = []
        for i in range(len(container_sizes)):
            result.append(container_info(trash_boxes[i], container_sizes[i]))
            xmin_container = container_boxes[i][0]
            ymin_container = container_boxes[i][1]
            img = cv2.rectangle(img, 
                                (int(container_boxes[i][0]), int(container_boxes[i][1])), 
                                (int(container_boxes[i][2]), int(container_boxes[i][3])), 
                                (255, 0, 0), 
                                2)
            for box in trash_boxes[i]:
                xmin = int(box[0] / 4 + xmin_container)
                ymin = int(box[1] / 4 + ymin_container)
                xmax = int(box[2] / 4 + xmin_container)
                ymax = int(box[3] / 4 + ymin_container)
                img = cv2.rectangle(img, 
                                    (xmin, ymin), 
                                    (xmax, ymax), 
                                    (0, 0, 255), 
                                    2)
        #cv2_imshow(img)
        return result, img


class DirectoryParser:
    def __init__(self, 
                 source_path, 
                 model_path_container,
                 model_path_trash,
                 service_ip):
        self.source_path = source_path
        self.imgprocessor =  ImageProcessor(model_path_container, model_path_trash)
        self.service_ip = service_ip

    def delete_file(self, path):
        if os.path.exists(path):
            if os.path.isfile(path):
                os.remove(path)
            else:
                shutil.rmtree(path)
    
    def parse_filename(self, filename):
        if filename[-4:] != ".png" and filename[-4:] != ".jpg":
            print("Incorect extension.")
            return False
        return True
    
    def start(self):
        print("Processing directory")
        while True:
            files = os.listdir(self.source_path)
            for filename in files:
                parse_results = self.parse_filename(filename)
                print(f"Starting to process file {filename}")
                if not parse_results:
                    print(f"Incorrect file in video_source directory: \"{filename}\"")
                    self.delete_file(f"{self.source_path}/{filename}")
                    continue
                res, img = self.imgprocessor.get_staticticsByImage(f"{self.source_path}/{filename}")
                #width = img.shape[1] // 3
                #height = img.shape[0] // 3
                #img = cv2.resize(img, 
                #                 (img.shape[1] // 3, img.shape[0] // 3), 
                #                 interpolation = cv2.INTER_AREA)
                cv2.imwrite(f"{self.source_path}/{filename[:-4]}.jpg", img)
                with open(f"{self.source_path}/{filename[:-4]}.jpg", 'rb') as f:
                    encoded_file = b64encode(f.read()).decode('utf-8')
                self.delete_file(f"{self.source_path}/{filename}")
                self.delete_file(f"{self.source_path}/{filename[:-4]}.jpg")
                #print(res)
                tmp_id = int(filename[0] * (filename[0].isdigit()) + '0' * (not filename[0].isdigit()))#'100' + 
                res_dict = dict()
                res_dict['containers'] = []
                for r in res:
                    tmp_dict = dict()
                    tmp_dict['insideGarbage'] = r[0]
                    tmp_dict['nearbyGarbage'] = r[1]
                    res_dict['containers'].append(tmp_dict)
                #res_dict['cameraId'] = tmp_id

                res_dict['totalContainers'] = len(res)
                res_dict['filledContainers'] = sum([r[0] > 0 for r in res])
                res_dict['photo'] = dict()
                res_dict['photo']['data'] = encoded_file
                res_dict['photo']['extension'] = 'jpg'
                #with open('file.json', 'w', encoding='utf-8') as f:
                #    json.dump(res_dict, f)
                #print(tmp_id)
                #print(f'http://{self.service_ip}/api/cameras/{tmp_id}')
                r = requests.post(f'http://{self.service_ip}/api/cameras/{tmp_id}', json=res_dict, headers={'Content-Type': 'application/json'})
                print(r, r.text)              
            sleep(10)

def container_info(trash_boxes, container_size):
    counter_inside = 0
    counter_outside = 0
    #print(trash_boxes, container_size)
    for box in trash_boxes:
        x_center = (box[2] - box[0]) / 2 + box[0]
        y_center = (box[3] - box[1]) / 2 + box[1]
        if y_center < container_size[1] / 2:
            counter_inside += 1
        else:
            counter_outside += 1
    return counter_inside, counter_outside