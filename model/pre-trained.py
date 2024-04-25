import timm 
import torch
import urllib
from PIL import Image
from timm.data import resolve_data_config
from timm.data.transforms_factory import create_transform

# Loading pre-trained model
model = timm.create_model('densenet121', pretrained=True)
model.eval()

# Loading and pre-process an image
config = resolve_data_config({}, model = model)
transform = create_transform(**config)

filename = './data/frames/frame_0000.jpg'
img = Image.open(filename).convert('RGB')
tensor = transform(img).unsqueeze(0)

with torch.no_grad():
    out = model(tensor)
probabilities = torch.nn.functional.softmax(out[0], dim=0)

url, filename = ("https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt", "imagenet_classes.txt")
urllib.request.urlretrieve(url, filename) 
with open("imagenet_classes.txt", "r") as f:
    categories = [s.strip() for s in f.readlines()]

# Print top categories per image
top5_prob, top5_catid = torch.topk(probabilities, 5)
for i in range(top5_prob.size(0)):
    print(categories[top5_catid[i]], top5_prob[i].item())
