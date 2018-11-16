from flask import Flask, render_template, request
import json

app = Flask(__name__, static_url_path="/static", static_folder="static")

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/search", methods=['POST'])
def search():
    if request.method == "POST":
        n = int(request.form['data'])
        #palautus esimerkki
        if n == 0: result = ["dragonfly.jpg", "moss.jpg", "mountain.jpg", "mountain2.jpg", "mountain3.jpg"]
        if n == 1: result = ["mountain.jpg", "mountain2.jpg", "mountain3.jpg"]
        if n == 2: result = ["dragonfly.jpg", "moss.jpg", "mountain.jpg", "mountain2.jpg", "mountain3.jpg", "guitar.jpg"]

        return json.dumps(result)

if __name__ == "__main__":
    app.run()