import json
import os
from statistics import mean

import numpy as np
import pandas as pd
from skimage import io
from skimage.color import deltaE_ciede94, rgb2lab
from skimage.transform import resize

import datetime

import DBConnection.py as db


""" This will change the working directory to where the small pics are for the deltaE func """
path = "colours/smallpics/"
os.chdir(os.getcwd() + "/" + path)
images = os.listdir()


# Define as Jaccard Distance == 1 - Jacc sim, to be the same way as deltaE (1 for not equal)
def jaccardDistance(image1, image2):
    def getLabels(image, sort):
        with db.connect_to_database() as cursor:
            cursor.execute("""SELECT labels, validity
                            FROM omaluokittelu
                            WHERE imagepath = %s;
                            """, (image,))
            labels = []
            for i in cursor:
                labels.append([i[0], i[1]])
            if sort:
                labels = sorted(labels, key=lambda x:x[1], reverse=True) #sort by validity
                first_label = labels[0][0] #get the most important label
            return(set(item[0] for item in labels), first_label)
    
    A, f_label = getLabels(image1, 1)
    B = getLabels(image2, 0)[0]
    
    if f_label not in B: #if image1's most important label is not in image2's labels: return max distance
        return 1
    else:
        return 1 - (len(A & B)) / (len(A | B))


def deltaE(image1, image2):

    img1 = rgb2lab(io.imread(image1))
    img2 = rgb2lab(io.imread(image2))

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


for img1 in images:
    deltas = {"No recommendations": 1}
    jaccs = {"No recommendations": 1}
    combined = {"No recommendations": 1}

    for img2 in filter(lambda x: x != img1, images):
        delta = deltaE(img1, img2)
        jacc = jaccardDistance(img1, img2)
        comb = 0.7*jacc + 0.3*delta

        if betterRecommendation(delta, deltas):
            updateRecommendations(img2, delta, deltas)

        if betterRecommendation(jacc, jaccs):
            updateRecommendations(img2, jacc, jaccs)

        if betterRecommendation(comb, combined):
            updateRecommendations(img2, comb, combined)

    print("For image:", img1)
    print("DeltaE:", *sorted([(pic, val)
                              for pic, val in deltas.items()], key=lambda x: x[1]))
    print("Jaccard:", *sorted([(pic, val)
                               for pic, val in jaccs.items()], key=lambda x: x[1]))
    print("Combined:", *sorted([(pic, val)
                                for pic, val in combined.items()], key=lambda x: x[1]))
    print()

    ''' Substitute print with eg. db inserts
    with db.connect_to_database() as cursor:
        for pic, val in deltas.items():
            cursor.execute("""INSERT INTO recommendations (image1, image2, method, value)
                             VALUES (%s %s %s %s %s)""", (img1, pic, "deltae", val))
        for pic, val in jaccs.items():
            cursor.execute("""INSERT INTO recommendations (image1, image2, method, value)
                             VALUES (%s %s %s %s %s)""", (img1, pic, "jaccard", val))
        for pic, val in combined.items():
            cursor.execute("""INSERT INTO recommendations (image1, image2, method, value)
                             VALUES (%s %s %s %s %s)""", (img1, pic, "combined", val))
    
    '''