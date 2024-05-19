import config as cfg

from dataset import CoralDataset
from utils import make_transform, collate_fn

import torch, torchvision
from torch import optim
from torch.utils.data import DataLoader
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor

# Create & load datasets
dataset_train = CoralDataset(cfg.DATASET_TRAIN_PATH, cfg.DATASET_TRAIN_ANNOTATION_PATH, transforms = make_transform())
dataset_val = CoralDataset(cfg.DATASET_VAL_PATH, cfg.DATASET_VAL_ANNOTATION_PATH, transforms = make_transform())

# Create data-loaders pipeline
loader_train = DataLoader(dataset_train, 
                          batch_size=cfg.BATCH_SIZE, shuffle=True, collate_fn=collate_fn)
loader_val = DataLoader(dataset_val, batch_size=cfg.BATCH_SIZE, shuffle=True, collate_fn=collate_fn)

# Loading FastRNCC pre-trained model
def get_model_instance_segmentation(num_classes):
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=False)
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    return model

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
num_classes = cfg.NUM_CLASSES
num_epoch = cfg.EPOCHS
model = get_model_instance_segmentation(num_classes)

params = [p for p in model.parameters() if p.requires_grad]
optimizer = torch.optim.SGD(params, lr=0.005, momentum=0.9, weight_decay=0.0005)

for epoch in range(num_epoch):
    model.train()
    i = 0
    for imgs, annotations in loader_train:
        i += 1
        imgs = list(img.to(device) for img in imgs)
        annots = [{k: v.to(device) for k, v in t.items()} for t in annotations]

        loss_dict = model(imgs, annotations)
        losses = sum(loss for loss in loss_dict.values())

        optimizer.zero_grad()
        losses.backward()
        optimizer.step()
        print(f'Iteration: {i}/{len(loader_train)}, Loss: {losses}')
