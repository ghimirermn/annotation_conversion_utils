import os
import json
from tqdm import tqdm

coco_annotations_file = './val.json'
yolov5_annotations_dir = './test_coco'
os.makedirs(yolov5_annotations_dir, exist_ok=True)

with open(coco_annotations_file, 'r') as f:
    coco_data = json.load(f)

for image in tqdm(coco_data['images']):
    image_name = os.path.splitext(image['file_name'])[0]
    yolov5_annotation_file = os.path.join(yolov5_annotations_dir, f'{image_name}.txt')
    with open(yolov5_annotation_file, 'w') as f:
        annotations = [annotation for annotation in coco_data['annotations'] if annotation['image_id'] == image['id']]
        for annotation in annotations:
            x, y, w, h = annotation['bbox']
            x_center = (x + w / 2) / image['width']
            y_center = (y + h / 2) / image['height']
            w /= image['width']
            h /= image['height']
            class_id = annotation['category_id']
            f.write(f'{class_id} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}\n')
