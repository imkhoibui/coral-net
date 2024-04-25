import torchvision

def make_transform():
    custom_transforms = []
    custom_transforms.append(torchvision.transforms.Resize((224, 224)))
    custom_transforms.append(torchvision.transforms.ToTensor())
    return torchvision.transforms.Compose(custom_transforms)

def collate_fn(batch):
    return tuple(zip(*batch))

def resize_annotation(annotation, original_size, new_size):
    x_min, y_min, x_max, y_max = annotation
    original_width, original_height = original_size
    new_width, new_height = new_size

    x_min = (x_min / original_width) * new_width
    x_max = (x_max / original_width) * new_width
    y_min = (y_min / original_height) * new_height
    y_max = (y_max / original_height) * new_height

    return x_min, y_min, x_max, y_max