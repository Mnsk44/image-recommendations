import json
import os
from statistics import mean

import numpy as np
import pandas as pd
from skimage import io
from skimage.color import deltaE_ciede94, rgb2lab
from skimage.transform import resize

import datetime

""" Initialization """
print("Starting to load data into memory")

""" This will change the working directory to where the small pics are for the deltaE func """
path = "colours/smallpics/"
os.chdir(os.getcwd() + "/" + path)
images = os.listdir()

imagedata = {}
for img in images:
    try:
        img1 = io.imread(img)
        imagedata[img] = img1
    except ValueError:
        print("Error in file", img)

ilabels = pd.read_csv("../datatemp.csv", sep=",")
imagelabels = {}
for idx, img in ilabels.iterrows():
    if img[0] in imagelabels.keys():
        imagelabels[img[0]].append((img[1], img[2]))
    else:
        imagelabels[img[0]] = [(img[1], img[2])]


workorder = []
with open("../workorder.txt") as todo:
    workorder = [img.strip("\n") for img in todo.readlines()]


with open("../output.csv", "w") as output:
    print("image1,image2,type,value", file=output)

print("Load ended succesfully (if it didn't crash by now)")

""" Initialization ends """

# Define as Jaccard Distance == 1 - Jacc sim, to be the same way as deltaE (1 for not equal)


def jaccardDistance(image1, image2):
    def getLabels(image, sort):
        labels = imagelabels[image]
        first_label = ""
        if sort:
            # sort by validity
            labels = sorted(labels, key=lambda x: x[1], reverse=True)
            first_label = labels[0][0]  # get the most important label
        return(set(item[0] for item in labels), first_label)

    A, f_label = getLabels(image1, 1)
    B = getLabels(image2, 0)[0]

    if f_label not in B:  # if image1's most important label is not in image2's labels: return max distance
        return 1
    else:
        return 1 - (len(A & B)) / (len(A | B))


def deltaE(image1, image2):

    img1 = rgb2lab(image1)
    img2 = rgb2lab(image2)

    """ Very generalized view that deltaE generally is between 0-100:
        Normalize with that range to make this comparable with jaccard,
        and as we are trying to find the minimal for this, it doesn't actually
        matter if some value is over 100 """
    return (mean([deltaE_ciede94(img1, img2).mean(),
                  deltaE_ciede94(img2, img1).mean()]) / 100)


# Keep only 10 best in store
def betterRecommendation(new, current):
    if new > max(current.values()) and len(current) == 10:
        return False
    else:
        return True


# Keep only 10 best in store
def updateRecommendations(newname, newvalue, current):
    if "No recommendations" in current.keys():
        current.pop("No recommendations")

    if len(current) < 10:
        current[newname] = newvalue
    else:
        current.pop(max(current, key=lambda key: current[key]))
        current[newname] = newvalue
    return


for img1 in workorder:
    deltas = {"No recommendations": 1}
    jaccs = {"No recommendations": 1}
    combined = {"No recommendations": 1}

    for img2 in filter(lambda x: x != img1, images):
        delta = deltaE(imagedata[img1], imagedata[img2])
        jacc = jaccardDistance(img1, img2)
        comb = 0.7*jacc + 0.3*delta

        if betterRecommendation(delta, deltas):
            updateRecommendations(img2, delta, deltas)

        if betterRecommendation(jacc, jaccs):
            updateRecommendations(img2, jacc, jaccs)

        if betterRecommendation(comb, combined):
            updateRecommendations(img2, comb, combined)

    with open("../output.csv", "a") as output:
        for pic, val in deltas.items():
            print(img1, pic, "deltae", val, sep=",", file=output)
        for pic, val in jaccs.items():
            print(img1, pic, "jaccard", val, sep=",", file=output)
        for pic, val in combined.items():
            print(img1, pic, "combined", val, sep=",", file=output)
