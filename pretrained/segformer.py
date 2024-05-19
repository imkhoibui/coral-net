from transformers import SegformerImageProcessor, SegformerForSemanticSegmentation
from PIL import Image
from utils.palette import ade_palette

import torch
import matplotlib.pyplot as plt
import numpy as np

# Checkpoint 1: Loading pretrained model
model_name = "nvidia/segformer-b5-finetuned-ade-640-640"
processor = SegformerImageProcessor(do_resize=False)
model = SegformerForSemanticSegmentation.from_pretrained(model_name)

# Checkpoint 2: Fine-tuning
image_path = "data/frames/frame_0000.jpg"
image = Image.open(image_path)

pixel_values = processor(image, return_tensors="pt").pixel_values

with torch.no_grad():
    outputs = model(pixel_values)
    logits = outputs.logits

# Checkpoint 3: Inference
predicted_segmentation_map = processor.post_process_semantic_segmentation(outputs, target_sizes=[image.size[::-1]])[0]
predicted_segmentation_map = predicted_segmentation_map.cpu().numpy()
color_seg = np.zeros((predicted_segmentation_map.shape[0], predicted_segmentation_map.shape[1], 3), dtype=np.uint8)
palette = np.array(ade_palette())

for label, color in enumerate(palette):
    color_seg[predicted_segmentation_map == label, :] = color

# Checkpoint 4: Visualize results
color_seg = color_seg[..., ::-1]
img = np.array(image) * 0.5 + color_seg * 0.5
img = img.astype(np.uint8)

plt.figure(figsize=(15, 10))
plt.imshow(img)
plt.savefig('plotted/image_with_mask.png') 
plt.show()



