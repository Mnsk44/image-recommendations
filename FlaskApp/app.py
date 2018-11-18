from flask import Flask, render_template, request
import json

app = Flask(__name__, static_url_path="/static", static_folder="static")

@app.route("/")
def render_home():
    return render_template('search.html')

@app.route("/search", methods=['POST'])
def search_images():
    if request.method == "POST":
        tags = request.form.getlist("data[]")
        print(tags)
       
        #tässä haettaisiin valituilla tageilla tietokannasta kuvien nimet/urlit
        #ja palautetaan ne ( + mahdollisesti kuvakohtaiset tagit? )
        return json.dumps(tags)

@app.route("/image/<id>", methods=['GET'])
def render_image(id):
    if request.method == "GET":
        #haetaan tietokannasta kaikki tiedot kuvalle
        return render_template('image.html', image=id)

@app.route("/image/recommend", methods=['POST'])
def recommend_images():
    if request.method == "POST":
        print(request.form['method'])
        print(request.form['id'])
        method = request.form['method']
        id = request.form['id']
        #tässä haettaisiin valitulla "mittapuulla" samankaltaisimmat kuvat (5 kpl?)
        #kyseiselle kuvalle + palautetaan ne listana.
        #return json.dumps( str(request.form['method'] + " " + request.form['id']))
        if method == "category":
                return json.dumps(["dragonfly", "moss", "mountain", "mountain2", "mountain3"])
        elif method == "colour":
                return json.dumps(["mountain2", "mountain3", "guitar", "dragonfly", "moss"])

if __name__ == "__main__":
    app.run(debug=True, port=5000)