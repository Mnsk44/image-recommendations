import ImageRecs.DBConnection as db

def searchImages(labels):
    labels = tuple(labels)
    with db.connect_to_database() as cursor:
        cursor.execute("""SELECT imagepath
                        FROM omaluokittelu
                        WHERE labels IN %s
                        ORDER BY validity DESC
                        LIMIT 25;""", (labels,))
        '''
        cursor.execute("""SELECT image1
                        FROM recommendations
                        WHERE EXISTS(SELECT 1
                                     FROM omaluokittelu
                                     WHERE labels IN %s
                                     AND recommendations.image1 = omaluokittelu.imagepath)
                        ORDER BY value DESC
                        LIMIT 25;""", (labels,))
        '''
        images = []
        for i in cursor:
            images.append({"url": i[0]})
    return images

def getLabels(url):
    with db.connect_to_database() as cursor:
        cursor.execute("""SELECT labels
                        FROM omaluokittelu
                        WHERE imagepath = %s;
                        """, (url,))
        labels = []
        for i in cursor:
            labels.append({"label": i[0]})
    return labels

def getRecommendations(img1, method):
    with db.connect_to_database() as cursor:
        cursor.execute("""SELECT DISTINCT(image2), value
                        FROM recommendations
                        WHERE image1 = %s
                        AND type = %s
                        AND value != 'NaN'
                        AND value != 1
                        ORDER BY value ASC
                        LIMIT 10;""", (img1, method))
        recs = []
        for i in cursor:
            recs.append({"url": i[0], "value": i[1]})
    return recs
