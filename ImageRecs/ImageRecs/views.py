from flask import render_template, request
from ImageRecs import app
from ImageRecs.recs import searchImages
import json

@app.route("/", methods=['GET'])
def render_home():
    if request.method == "GET":
        #get all labels
        with open('ImageRecs/static/data/labels.json') as json_file:
            labels = json.load(json_file)
        return render_template('search.html', labels=labels)

@app.route("/search", methods=['POST'])
def search_images():
    if request.method == "POST":
        labels = request.form.getlist("data[]")
        #search for images by their labels
        images = searchImages(labels)
        return images

@app.route("/image/<id>", methods=['GET'])
def render_image(id):
    if request.method == "GET":
        #retrieve all information about selected image
        return render_template('image.html', image=id)

@app.route("/image/recommend", methods=['POST'])
def recommend_images():
    if request.method == "POST":
        print(request.form['method'])
        print(request.form['id'])
        method = request.form['method']
        id = request.form['id']

        #retrieve similar images using selected method
        #suggestions = recommend(id, method)

        #example:
        category = [       
                        {"id":"0", "name":"dragonfly", "sim":0.72},
                        {"id":"1", "name":"moss", "sim":0.60},
                        {"id":"2", "name":"mountain", "sim":0.55},
                        {"id":"3", "name":"mountain2", "sim":0.32},
                        {"id":"4", "name":"mountain3", "sim":0.12}]
        colour = [       
                        {"id":"3", "name":"mountain2", "sim":0.92},
                        {"id":"2", "name":"mountain", "sim":0.85},
                        {"id":"4", "name":"mountain3", "sim":0.62},
                        {"id":"5", "name":"moss", "sim":0.40},
                        {"id":"1", "name":"guitar", "sim":0.30}]

        if method == "category":
                return json.dumps(category)
        elif method == "colour":
                return json.dumps(colour)
