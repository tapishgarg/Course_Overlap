from flask import Flask, render_template, request, url_for, Response
import os, json

from phrase_extraction import phrase_extractor

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/_autocomplete', methods=['GET'])
def autocomplete():
    SITE_ROOT = os.path.realpath(os.path.dirname("/Users/tapishgarg/Desktop/Course_Overlap/data"))
    json_url = os.path.join(SITE_ROOT, "data", "courses_name.json")
    json_data = json.loads(open(json_url).read())
    return Response(json.dumps(json_data), mimetype='application/json')

@app.route('/process', methods = ['POST'])
def process():
    if request.method == 'POST':

        range1 = request.form['range1']
        print(range1)
        range2 = request.form['range2']
        print(range2)
        range3 = request.form['range3']
        print(range3)
        range4 = request.form['range4']
        print(range4)

        # results = phrase_extractor(raw_text)
    return render_template("index.html")
  

if __name__ == "__main__":
    app.run(debug=True)