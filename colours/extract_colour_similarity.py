import json
import os
from statistics import mean

import numpy as np
import pandas as pd
from skimage import io
from skimage.color import deltaE_ciede94, rgb2lab
from skimage.transform import resize

IMG_SIZE = (90, 160)

path = "colours/pics/"
os.chdir(os.getcwd() + "/" + path)
images = os.listdir()


def deltaE(newimage, oldimages):
    delta = []

    nimg = rgb2lab(resize(io.imread(newimage), IMG_SIZE))
    for oldimg in oldimages:
        oimg = rgb2lab(resize(io.imread(oldimg), IMG_SIZE))

        delta.append(mean([deltaE_ciede94(nimg, oimg).mean(),
                           deltaE_ciede94(oimg, nimg).mean()]))

    return pd.Series(delta, name=newimage, index=oldimages)


oldimages = [images[0]]
deltas = pd.DataFrame(np.nan, index=[images[0]], columns=[images[0]])
for i, img in enumerate(images[1:]):
    print("Images left:", len(images[1:]) - i, end="\r")
    delta = deltaE(img, oldimages)
    deltas.loc[img] = delta
    deltas[img] = delta
    oldimages.append(img)

print(deltas.to_json(), file=open("../testfile.json", "w"))
