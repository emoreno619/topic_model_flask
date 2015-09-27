import ipdb
from flask import Flask
from flask import request
from flask import jsonify
app = Flask(__name__)


import os
import sys
import string
import json
import graphlab as gl
from graphlab import SArray
# from flask import url_for, redirect



def init():
	m = gl.load_model('topic_model_150_stopworded')
	jtopics = m.get_topics()
	return str(jtopics)
	# jtopics = topics.export_json()

def createSArray(arr):
	return SArray(arr)

@app.route("/")
def hello():
    return "Hello World!"

@app.route(u'/new', methods=[u'POST'])
def topify_doc():
	# ipdb.set_trace()
	print request.values
	doc = json.loads(request.form.get('data')) #needs to be array of string
	doc = gl.SFrame(doc)
	doc = gl.text_analytics.count_words(doc['X1'])
	doc = doc.dict_trim_by_keys(gl.text_analytics.stopwords(), True)
	doc = gl.SFrame(doc)
	
	pred = m.predict(doc) #alternatively, m.predict(doc, output_type='probability')
	
	result = m.get_topics(list(pred))

	# result = result.pack_columns()

	unstacked = result.unstack(['word', 'score'], 'ws')
	unstacked2 = unstacked.unstack(['topic', 'ws'], 'total')
	
	return jsonify(unstacked2['total'][0])

if __name__ == "__main__":
    m = gl.load_model('topic_model_150_stopworded')
    app.run()
    