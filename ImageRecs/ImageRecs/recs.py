import ImageRecs.DBConnection as db

def searchImages(labels):
    labels = tuple(labels)
    with db.connect_to_database() as cursor:
        cursor.execute("""SELECT imagepath
                        FROM omaluokittelu
                        WHERE labels IN %s
                        ORDER BY validity DESC
                        LIMIT 25;""", (labels,))
        images = []
        for i in cursor:
            images.append({"url": i[0]})
    return images

'''
def getLabels(id):
    return id
'''

def getRecommendations(img1, method):
    with db.connect_to_database() as cursor:
        cursor.execute("""SELECT image2, value
                        FROM recommendations
                        WHERE image1 = %s
                        AND type = %s
                        AND value != 'NaN'
                        ORDER BY value DESC
                        LIMIT 10;""", (img1, method))
        recs = []
        for i in cursor:
            recs.append({"url": i[0], "value": i[1]})
    return recs