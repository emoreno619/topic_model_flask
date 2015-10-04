import ipdb
from flask import Flask
from flask import request
from flask import jsonify
app = Flask(__name__)

# import matplotlib.pyplot as plt
import os
import sys
import string
import json
import heapq
import graphlab as gl
from graphlab import SArray
import base64
import StringIO
# import Image
# from wordcloud import WordCloud
# from flask import url_for, redirect

# corpus = ''
# for c in documents:
#	corpus += c if ord(c) < 128

# ''.join([ c for c in word if ord(c) < 128 ])

def createSArray(arr):
	return SArray(arr)

@app.route("/")
def hello():
    return "Hello World!"

@app.route(u'/location', methods=[u'POST'])
def topify_doc():

	# ipdb.set_trace()
	print request.values
	doc = json.loads(request.form.get('data')) #needs to be array of string
	doc = gl.SFrame(doc)
	doc = gl.text_analytics.count_words(doc['X1'])
	doc = doc.dict_trim_by_keys(gl.text_analytics.stopwords(), True)
	doc = gl.SFrame(doc)
	
	prob = m.predict(doc, output_type='probability') #alternatively, m.predict(doc, output_type='probability')

	# new addition

	# lis = []

	# for topic in arrTopicId:
	# 	topic['score'] = prob[0][topic['id']]
	# 	slis = []
	# 	slis.append(topic['category'])
	# 	slis.append(topic['score'])
	# 	lis.append(slis)

	# resultTopics = heapq.nlargest(5, lis, key=lambda x: x[1])

	resultTopics = heapq.nlargest(50, enumerate(prob[0]), key=lambda x: x[1])

	toSend = []

	# ipdb.set_trace()

	for res in resultTopics:
		slis = []
		i = 0
		while i < 5:
			if i == 0:
				slis.append(res[1])
			slis.append([topic_frame[res[0]*5 + i]['word'], topic_frame[res[0]*5 + i]['score']])
			i = i + 1
		toSend.append(slis)

	# ipdb.set_trace() 
	
	return jsonify({'topics':toSend})

@app.route(u'/reviews', methods=[u'POST'])
def topify_doc2():

	# ipdb.set_trace()
	print request.values
	doc = json.loads(request.form.get('data')) #needs to be array of string
	doc = gl.SFrame(doc)
	doc = gl.text_analytics.count_words(doc['X1'])
	doc = doc.dict_trim_by_keys(gl.text_analytics.stopwords(), True)
	doc = gl.SFrame(doc)
	
	prob = m.predict(doc, output_type='probability')

	# new addition

	resultTopics = []

	for scoreSet in prob:

		arrTopicId =[{'id':182,'category':'buffet','score':0}, {'id':3,'category':'pizza','score':0}, 
		{'id':148,'category':'Mexican','score':0}, {'id':243,'category':'bar','score':0}, {'id':154,'category':'lunch','score':0}, {'id':326,'category':'sushi','score':0}, {'id':52,'category':'ice cream','score':0}, {'id':303,'category':'cafe','score':0}, 
		{'id':202,'category':'Vietnamese','score':0}, {'id':249,'category':'Chinese','score':0}, {'id':150,'category':'Fried Chicken','score':0}, {'id':64,'category':'breakfast','score':0}, {'id':245,'category':'burger','score':0}, 
		{'id':163,'category':'Thai','score':0}, {'id':156,'category':'seafood','score':0}, {'id':26,'category':'sandwich','score':0}, {'id':240,'category':'Greek / Gyro','score':0}, {'id':151,'category':'donuts','score':0}, {'id':187,'category':'cheap','score':0}, 
		{'id':159,'category':'Good Food','score':0}, {'id':167,'category':'Good Service','score':0},
		{'id':190,'category':'Bad Service','score':0}, {'id':176,'category':'Indian','score':0}, {'id':179,'category':'Good Atmosphere','score':0}, {'id':256,'category':'Bad Atmosphere','score':0}, {'id':42,'category':'Hair Salon','score':0}, 
		{'id':155,'category':'Hotel','score':0}, {'id':18,'category':'Doctor','score':0}, {'id':152,'category':'Yoga','score':0}, {'id':198,'category':'Ramen','score':0}, {'id':252,'category':'Movies','score':0}, 
		{'id':247,'category':'Venue','score':0}, {'id':242,'category':'Salad','score':0}, {'id':233,'category':'Dog Friendly','score':0}, {'id':238,'category':'Clothing','score':0}, {'id':315,'category':'Happy Hour','score':0}, 
		{'id':327,'category':'Dance / Club','score':0}, {'id':340,'category':'Mechanic','score':0}, {'id':61,'category':'Bagel / Bakery','score':0}, {'id':66,'category':'Italian','score':0}, {'id':72,'category':'Bbq','score':0}, 
		{'id':82,'category':'Hawaiian','score':0}, {'id':86,'category':'Nail Salon','score':0}, {'id':108,'category':'Beer','score':0}]

		lis = []

		for topic in arrTopicId:
			topic['score'] = scoreSet[topic['id']]
			slis = []
			slis.append(topic['category'])
			slis.append(topic['score'])
			lis.append(slis)

		resultTopics.append(heapq.nlargest(5, lis, key=lambda x: x[1]))

	# ipdb.set_trace()

	returnDict = {"reviewTopics": resultTopics}
	
	return jsonify(returnDict)
	
    # old working version

    # result = m.get_topics(list(pred))

	# unstacked = result.unstack(['word', 'score'], 'ws')
	# unstacked2 = unstacked.unstack(['topic', 'ws'], 'total')
	
	# return jsonify(unstacked2['total'][0])

if __name__ == "__main__":
    m = gl.load_model('/Users/eduardo/gSchool/week20/playing_w_python/topics_1000')
    topic_frame = m.get_topics()
    app.run()
    