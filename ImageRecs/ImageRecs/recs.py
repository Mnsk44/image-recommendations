import pandas as pd

def searchImages(labels):
    df = pd.read_csv("ImageRecs/static/data/test.csv", delimiter=";", names=["id", "url", "label"])
    df = df.loc[df['label'].isin(labels)]
    json_data = df.to_json(orient="records")
    return json_data