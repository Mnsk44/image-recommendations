import os
import numpy as np
from skimage import io
from skimage.transform import resize
from sys import argv

IMG_SIZE = (90, 160)

paths = [argv[p] for p in range(2, len(argv))]

imagenames = []
imagelocations = []
for path in paths:
    files = os.listdir(path)
    imagenames.extend(files)
    imagelocations.extend([path + "/" + file for file in files])


for name, img in zip(imagenames, imagelocations):
    out = f"{argv[1]}/{os.path.splitext(name)[0]}.jpg"
    img = resize(io.imread(img), IMG_SIZE)
    io.imsave(out, img)
