import os
import sys
import string
import bs4
from bs4 import BeautifulSoup
import nltk
from nltk import word_tokenize
from nltk.stem.snowball import SnowballStemmer
import graphlab as gl
from graphlab.toolkits.feature_engineering import TFIDF

from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

def main():


	porter = nltk.PorterStemmer()
	snow_stemmer = SnowballStemmer("english", ignore_stopwords=True)
	wordnet_lemmatizer = WordNetLemmatizer()

	docs = gl.SFrame.read_csv("/Users/eduardo/Downloads/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json", header=False)
	docs2 = gl.SFrame.read_csv("/Users/eduardo/my_scrape.json", header=False)

	docs = docs.unpack('X1', column_name_prefix='')
	docs2 = docs2.unpack('X1', column_name_prefix='')

	# CONCATENATE INTO ONE SARRAY TO SAVE WORK

	docs3 = docs['text'].append(docs2['review'])

	# check encoding

	docs4 = docs3.apply(encodeInsurance)

	# remove html

	docs4 = docs4.apply(soup_wrapper)


	# tokenize

	docs4 = docs4.apply(tokenize_wrapper)

	# stem or lemmatize

	# lem
	# requires pos tag first
	# docs4 = docs4.apply(nltk.pos_tag)
	# docs4 = docs4.apply(lem_wrapper)

	docs4 = docs4.apply(stem_wrapper)

	# join

	docs4 = docs4.apply(string.join)

	# check encoding again...

	docs4 = docs4.apply(encodeInsurance)
	
	# make into dic/bag of words

	bag = gl.text_analytics.count_words(docs4)

	# remove stopwords

	bag = bag.dict_trim_by_keys(gl.text_analytics.stopwords(), True)

	# convert to SFrame and run TFIDF

	sf = gl.SFrame(bag)

	encoder = gl.feature_engineering.create(sf, TFIDF('X1'))
	sf = encoder.transform(sf)
	sf = sf.dropna()

	def encodeInsurance(doc):
		res = ''
		for c in doc:
			if (ord(c) < 128):
				res += c
		return res

	def soup_wrapper(arr):
		soup = BeautifulSoup(arr, 'html.parser')
		return soup.get_text()

	def tokenize_wrapper(arr):
			return word_tokenize(arr)

	def stem_wrapper(array):
		return [snow_stemmer.stem(w) for w in array]

	def lem_wrapper(array):
	    res = []
	    for tup in array:
	            pos = get_wordnet_pos(tup[1])
	            if (pos == ''):
	                    res.append(wordnet_lemmatizer.lemmatize(tup[0]))
	            else:
	                    res.append(wordnet_lemmatizer.lemmatize(tup[0], pos))
	    return res

	def get_wordnet_pos(treebank_tag):
	    if treebank_tag.startswith('J'):
	        return wordnet.ADJ
	    elif treebank_tag.startswith('V'):
	        return wordnet.VERB
	    elif treebank_tag.startswith('N'):
	        return wordnet.NOUN
	    elif treebank_tag.startswith('R'):
	        return wordnet.ADV
	    else:
	        return ''
