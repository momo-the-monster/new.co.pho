# install DeepLab Masking
import numpy as np
import torchvision
import torch
from PIL import Image, ImageFilter
import piexif
from torchvision import transforms

model = torchvision.models.segmentation.deeplabv3_resnet101(pretrained=True)
model = model.eval()
preprocess = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Rotate image based on EXIF Data
# From Piexif docs: https://piexif.readthedocs.io/en/latest/sample.html
def rotate_jpeg(filename):
    img = Image.open(filename)
    rotated = False
    if "exif" in img.info:
        exif_dict = piexif.load(img.info["exif"])

        if piexif.ImageIFD.Orientation in exif_dict["0th"]:
            orientation = exif_dict["0th"].pop(piexif.ImageIFD.Orientation)
            exif_bytes = piexif.dump(exif_dict)

            if orientation == 2:
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 3:
                img = img.rotate(180)
            elif orientation == 4:
                img = img.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 5:
                img = img.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
                rotated = True
            elif orientation == 6:
                img = img.rotate(-90, expand=True)
                rotated = True
            elif orientation == 7:
                img = img.rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
                rotated = True
            elif orientation == 8:
                img = img.rotate(90, expand=True)
                rotated = True

            img.save(filename, exif=exif_bytes)
    return rotated

def replace_bg(img, bg):
    # run model on image
    image = Image.open(img)
    image.thumbnail((1024,1024), Image.ADAPTIVE)
    image_tensor = preprocess(image)
    input_batch = image_tensor.unsqueeze(0)
    input_batch = input_batch.to('cuda')
    model.to('cuda')
    with torch.no_grad():
        output = model(input_batch)['out'][0]
    output_predictions = output.argmax(0)

    # create empty palette lookup
    palette = torch.zeros([21,3], dtype=torch.uint8)
    # set label 15 (person) to white
    palette[15][0] = 255
    palette[15][1] = 255
    palette[15][2] = 255
    # convert palette to numpy array
    palette = palette.numpy()

    # plot the semantic segmentation predictions of 21 classes in each color
    mask = Image.fromarray(output_predictions.byte().cpu().numpy()).resize(image.size)
    mask.putpalette(palette)
    mask = mask.convert('L').filter(ImageFilter.GaussianBlur(radius=1))

    # load new bg
    bg_image = Image.open(bg)
    bg_image = bg_image.resize(image.size)

    # composite and return
    composited = Image.composite(image, bg_image, mask)
    return composited
