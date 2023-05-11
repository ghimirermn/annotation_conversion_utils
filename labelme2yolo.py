import os
import json
from tqdm import tqdm

def convert(size, box):
    dw, dh = 1./size[0], 1./size[1]
    x, y = (box[0] + box[1])/2.0, (box[2] + box[3])/2.0
    w, h = box[1] - box[0], box[3] - box[2]
    return (x*dw, y*dh, w*dw, h*dh)

def convert_labelme_to_yolo(labelme_dir, output_dir):
    categories, class_index = {}, 0

    for filename in tqdm(os.listdir(labelme_dir)):
        if not filename.endswith('.json'):
            continue

        json_file = os.path.join(labelme_dir, filename)
        with open(json_file, 'r') as f:
            data = json.load(f)

        width, height = data['imageWidth'], data['imageHeight']

        for shape in data['shapes']:
            category = shape['label']
            if category not in categories:
                categories[category] = class_index
                class_index += 1

        annotations = []
        for shape in data['shapes']:
            category = shape['label']
            x, y = zip(*shape['points'])
            xmin, ymin, xmax, ymax = min(x), min(y), max(x), max(y)
            b = (xmin, xmax, ymin, ymax)
            bb = convert((width, height), b)
            annotations.append((categories[category], *bb))

        txt_file = os.path.splitext(filename)[0] + '.txt'
        txt_path = os.path.join(output_dir, txt_file)

        with open(txt_path, 'w') as f:
            for annotation in annotations:
                line = ' '.join(map(str, annotation))
                f.write(line + '\n')

convert_labelme_to_yolo("lableme_dir", "output_dir")