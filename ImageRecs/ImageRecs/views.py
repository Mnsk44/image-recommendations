from flask import render_template, request
from ImageRecs import app
from ImageRecs.recs import searchImages, getRecommendations, getLabels
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
        return json.dumps(images)

@app.route("/image", methods=['GET'])
def render_links():
    if request.method == "GET":
        return render_template('links.html')


@app.route("/image/<url>", methods=['GET'])
def render_image(url):
    if request.method == "GET":
        labels = getLabels(url)
        return render_template('image.html', image=url, labels=labels)

@app.route("/image/recommend", methods=['POST'])
def recommend_images():
    if request.method == "POST":
        method = request.form['method']
        url = request.form['url']
        #retrieve similar images using selected method
        suggestions = getRecommendations(url, method)
        return json.dumps(suggestions)
