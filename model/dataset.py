import os
import torch

from torchvision import models, transforms
from torch.utils.data import Dataset, DataLoader
from PIL import Image
from pycocotools.coco import COCO

from utils import resize_annotation

class CoralDataset(Dataset):
    def __init__(self, root, annotation, transforms=None):
        super(Dataset, self).__init__()
        self.root = root
        self.transforms = transforms
        self.coco = COCO(annotation)
        self.ids = list(sorted(self.coco.imgs.keys()))

    def __getitem__(self, index):
        coco = self.coco
        img_id = self.ids[index]
        ann_ids = coco.getAnnIds(imgIds=img_id)
        target = coco.loadAnns(ann_ids)

        path = coco.loadImgs(img_id)[0]['file_name']
        img = Image.open(os.path.join(self.root, path))

        # Number of objects in the image
        num_objs = len(target)
        boxes = []

        for i in range(num_objs):
            xmin = target[i]['bbox'][0]
            ymin = target[i]['bbox'][1]
            xmax = xmin + target[i]['bbox'][2]
            ymax = ymin + target[i]['bbox'][3]
            original_boxes = xmin, ymin, xmax, ymax
            xmin, ymin, xmax, ymax = resize_annotation(original_boxes, (640, 640), (224, 224))
            boxes.append([xmin, ymin, xmax, ymax])
        
        boxes = torch.as_tensor(boxes, dtype=torch.float32)
        labels = torch.ones((num_objs, ), dtype=torch.int64)

        img_id = torch.tensor([img_id])
        areas = []
        for i in range(num_objs):
            areas.append(target[i]['area'])
        areas = torch.as_tensor(areas, dtype=torch.float32)
        iscrowd = torch.zeros((num_objs,), dtype=torch.int64)

        annotation = {}
        annotation['boxes'] = boxes
        annotation['labels'] = labels
        annotation['image_id'] = img_id
        annotation['areas'] = areas
        annotation['iscrowd'] = iscrowd    

        if self.transforms is not None:
            img = self.transforms(img)

        return img, annotation
    def __len__(self):
        return len(self.ids)
    
