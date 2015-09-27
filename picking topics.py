arrTopicId =[{'id':182,'category':'buffet','score':0}, {'id':3,'category':'pizza','score':0}, {'id':148,'category':'Mexican','score':0}, {'id':243,'category':'bar','score':0}, {'id':154,'category':'lunch','score':0}, {'id':326,'category':'sushi','score':0}, {'id':52,'category':'ice cream','score':0}, {'id':303,'category':'cafe','score':0}, {'id':202,'category':'Vietnamese','score':0}, {'id':249,'category':'Chinese','score':0}, {'id':150,'category':'Fried Chicken','score':0}, {'id':64,'category':'breakfast','score':0}, {'id':245,'category':'burger','score':0}, {'id':163,'category':'Thai','score':0}, {'id':156,'category':'seafood','score':0}, {'id':26,'category':'sandwich','score':0}, {'id':240,'category':'Greek / Gyro','score':0}, {'id':151,'category':'donuts','score':0}, {'id':187,'category':'cheap','score':0}, {'id':159,'category':'Good Food','score':0}, {'id':167,'category':'Good Service','score':0},
{'id':190,'category':'Bad Service','score':0}, {'id':176,'category':'Indian','score':0}, {'id':179,'category':'Good Atmosphere','score':0}, {'id':256,'category':'Bad Atmosphere','score':0}, {'id':42,'category':'Hair Salon','score':0}, 
{'id':155,'category':'Hotel','score':0}, {'id':18,'category':'Doctor','score':0}, {'id':152,'category':'Yoga','score':0}, {'id':198,'category':'Ramen','score':0}, {'id':252,'category':'Movies','score':0}, 
{'id':247,'category':'Venue','score':0}, {'id':242,'category':'Salad','score':0}, {'id':233,'category':'Dog Friendly','score':0}, {'id':238,'category':'Clothing','score':0}, {'id':315,'category':'Happy Hour','score':0}, 
{'id':327,'category':'Dance / Club','score':0}, {'id':340,'category':'Mechanic','score':0}, {'id':61,'category':'Bagel / Bakery','score':0}, {'id':66,'category':'Italian','score':0}, {'id':72,'category':'Bbq','score':0}, 
{'id':82,'category':'Hawaiian','score':0}, {'id':86,'category':'Nail Salon','score':0}, {'id':108,'category':'Beer','score':0}]


def main():

	# assume m is defined as model from topic_model_350_stopworded
	# and doc is defined as stop_worded text into SFrame
	prob = m.predict(doc, output_type='probability')

	lis = []

	for topic in arrTopicId:
		topic['score'] = prob[0][topic['id']]
		slis = []
        slis.append(th['category'])
        slis.append(th['score'])
        lis.append(slis)

    resultTopics = heapq.nlargest(5, lis, key=lambda x: x[1])

