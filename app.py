from scipy.sparse import data
from util import calculate_relatedness
from flask import Flask, render_template, request, url_for, Response
import os, json
import numpy as np

from phrase_extraction import phrase_extractor
from esa import run_esa

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", related_courses = {})

@app.route('/_autocomplete', methods=['GET'])
def autocomplete():
    SITE_ROOT = os.path.realpath(os.path.dirname("/Users/tapishgarg/Desktop/Course_Overlap/data"))
    json_url = os.path.join(SITE_ROOT, "data", "courses_name.json")
    json_data = json.loads(open(json_url).read())
    return Response(json.dumps(json_data), mimetype='application/json')

@app.route('/process', methods = ['POST'])
def process():
    if request.method == 'POST':

        esa_w = request.form['range1']
        print(esa_w)
        book_simi_w = request.form['range2']
        print(book_simi_w)
        course = request.form['search']
        print(course)

        course_detail_path = "./data/course_data.json"
        related_courses = calculate_relatedness(esa_w, book_simi_w, course_detail_path, course)
    return render_template("index.html", esa_w = esa_w, book_simi_w = book_simi_w, related_courses = related_courses)

  

if __name__ == "__main__":
    app.run(debug=True)