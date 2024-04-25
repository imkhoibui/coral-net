import config as cfg

from dataset import CoralDataset
from utils import make_transform, collate_fn

import torch
from torch.utils.data import DataLoader

# Create & load datasets
dataset_train = CoralDataset(cfg.DATASET_TRAIN_PATH, cfg.DATASET_TRAIN_ANNOTATION_PATH, transforms = make_transform())
dataset_val = CoralDataset(cfg.DATASET_VAL_PATH, cfg.DATASET_VAL_ANNOTATION_PATH, transforms = make_transform())

# Create data-loaders pipeline
loader_train = DataLoader(dataset_train, 
                          batch_size=cfg.BATCH_SIZE, shuffle=True, collate_fn=collate_fn)
loader_val = DataLoader(dataset_val)

# Loading an image instance
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

for imgs, annotations in loader_train:
    imgs = list(img.to(device) for img in imgs)
    annotations = [{k: v.to(device) for k, v in t.items()} for t in annotations]
    print(annotations)
    break