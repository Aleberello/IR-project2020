
import numpy as np
import time
import re
import string
from nltk.tokenize import WordPunctTokenizer
from collections import Counter
import numpy as np
import time
import re
import string
from nltk.tokenize import WordPunctTokenizer
from collections import Counter
import nltk
from nltk.tokenize import WordPunctTokenizer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from collections import Counter
from collections import OrderedDict
import emoji
import json
from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
import math
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import re, random
from nltk import word_tokenize, sent_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity,cosine_distances
import pickle
from nltk.stem.porter import PorterStemmer

#Da utilizzare solo per la prima esecuzione
#nltk.download('stopwords')
#nltk.download('wordnet')
#nltk.download('averaged_perceptron_tagger')

class Preprocessor:
	def __init__(self, filesName):
		self.fileNames = filesName
		self.tweets = {}
		self.freq_text = dict()
		self.freq_user = dict()
		self.freq_links = dict()
		self.freq_emoji = dict()
		self.freq_hashtags = dict()
		self.TFD= {}
	
	def generate_tokens(self, tweet, data):
		'''
		Creates a unique set of tokens that were identified after processing, filtering and lemmatize the corpus text.:
		:param tweet: tweet id to identify the corresponding tweet inside the tweets dictionary 'data';
		:return: a list that contains the parsed text
		'''
		stopwords.words('english')
		stop_words = nltk.corpus.stopwords.words('english')
		functional_words = ["ADP", "AUX", "CCONJ", "DET", "NUM", "PART", "PRON", "SCONJ", "PUNCT", "SYM", "X"]
		
		text = data[tweet]['text']
		new_text = text.lower()
		new_text = re.sub(r'—|’|’’|-|”|“|‘', ' ', new_text)
		new_text = new_text.strip()
		new_text = re.sub(r'\d+', '', new_text)
		new_text = new_text.translate(str.maketrans('', '', string.punctuation))
		new_text = WordPunctTokenizer().tokenize(new_text)
		porter = PorterStemmer()
		
		tagged = nltk.pos_tag(new_text)
		for word in tagged:
			if word[0] not in stop_words and word[1] not in functional_words:
				lemma = porter.stem(word[0])
				if lemma not in stop_words:
					self.freq_text[data[tweet]['user_name']][lemma] += 1
					new_text.remove(word[0])
					new_text.append(lemma)
			else:
				new_text.remove(word[0])
		return new_text
	
	def identify_emoji(self, tweet, data):
		'''
		Identifies and return all emojis who are present inside the single tweet:
		:param tweet: tweet id to identify the corresponding tweet inside the tweets dictionary 'data';
		:return: a list that contains all emojis identified inside the text
		'''
		text = data[tweet]['text']
		emojis = []
		for pos, c in enumerate(text):
			if c in emoji.UNICODE_EMOJI:
				# print("Matched!!", c, c.encode("ascii", "backslashreplace"))
				self.freq_emoji[data[tweet]['user_name']][c] += 1
				emojis.append(c)
		
		return emojis
	
	def identify_user(self, tweet, data):
		'''
		Identifies and return all user_id who are presents inside the single tweet:
		:param tweet: tweet id to identify the corresponding tweet inside the tweets dictionary 'data';
		:return: a list that contains all user_id identified inside the text
		'''
		users = []
		text = data[tweet]['text']
		user = re.compile(r'@(\S+)')
		match_pattern = user.findall(text)
		for us in match_pattern:
			self.freq_user[data[tweet]['user_name']][us] += 1
			users.append(us)
		
		return users
	
	def identify_links(self, tweet, data):
		'''
		Identifies and return all URLs who are presents inside the single tweet:
		:param tweet: tweet id to identify the corresponding tweet inside the tweets dictionary 'data';
		:return: a list that contains all URLs identified inside the text
		'''
		group = []
		text = data[tweet]['text']
		link = re.compile(r'http\S+')
		links = link.findall(text)
		for us in links:
			self.freq_links[data[tweet]['user_name']][us] += 1
			group.append(us)
		
		return group
	
	def identify_hashtags(self, tweet, data):
		'''
		Identifies and return all hashtags who are present inside the single tweet:
		:param tweet: tweet id to identify the corresponding tweet inside the tweets dictionary 'data';
		:return: a list that contains all hashtags identified inside the text
		'''
		if not data[tweet]['hashtags'] == [None]:
			for i in data[tweet]['hashtags'][0]:
				self.freq_hashtags[data[tweet]['user_name']][i] += 1
			return data[tweet]['hashtags']
	
	def parser(self):
		'''
		Transforms all the corpus in the filesName insert them into dictionary whit tweets ids as keys and their attributes as values
		into a similar dictionary with more attributes for the same tweet as tokenized message, emojis, URLs, and user_id that are contained into original tweet.

		:return: a list of dictionaries for each tweet, containing their id, author, original text, tokenized text, hashtags, user_ids, emoji, and URLs;
				 five corpus_counter of the words, emoji, hashtags, URLs and user_ids and their corresponding frequencies.
		'''
		for file in self.fileNames:
			data = json.load(open(file))
			for tweet in data:
				if not data[tweet]['user_name'] in self.freq_text:
					self.tweets[data[tweet]['user_name']]= {}
					self.tweets[data[tweet]['user_name']]['tweets']= {}
					self.tweets[data[tweet]['user_name']]['frequency'] = {}
					self.freq_text[data[tweet]['user_name']]= Counter()
					self.freq_emoji[data[tweet]['user_name']] = Counter()
					self.freq_links[data[tweet]['user_name']] = Counter()
					self.freq_hashtags[data[tweet]['user_name']] = Counter()
					self.freq_user[data[tweet]['user_name']] = Counter()
					
				tokenized = self.generate_tokens(tweet, data)
				emoji = self.identify_emoji(tweet, data)
				links = self.identify_links(tweet, data)
				hashtags = self.identify_hashtags(tweet, data)
				user = self.identify_user(tweet, data)
				self.tweets[data[tweet]['user_name']]['tweets'][tweet] = {'author': data[tweet]['user_name'], 'text': data[tweet]['text'],
									  'tokenized': tokenized, 'user': user, 'hashtags': hashtags, 'emoji': emoji,
									  'links': links}
		for user in self.tweets:
			self.tweets[user]['frequency'] = {'freq_text': self.freq_text,
																			'freq_user': self.freq_user,
																			'freq_hashtags': self.freq_hashtags,
																			'freq_links': self.freq_links,
																			'freq_emoji': self.freq_emoji}
				
		
		return self.tweets

	def preprocess_text(self, text):
		stopwords.words('english')
		stop_words = nltk.corpus.stopwords.words('english')
		porter = PorterStemmer()
		functional_words = ["ADP", "AUX", "CCONJ", "DET", "NUM", "PART", "PRON", "SCONJ", "PUNCT", "SYM", "X"]
		
		new_text=re.sub('http\S+', '', text)
		new_text= re.sub('@[^\s]+', '', new_text)
		new_text = text.lower()
		new_text = re.sub(r'—|’|’’|-|”|“|‘', ' ', new_text)
		new_text = new_text.strip()
		new_text = re.sub(r'\d+', '', new_text)
		new_text = new_text.translate(str.maketrans('', '', string.punctuation))
		new_text = WordPunctTokenizer().tokenize(new_text)
		
		
		tagged = nltk.pos_tag(new_text)
		for word in tagged:
			if word[0] in stop_words or word[1] in functional_words:
				new_text.remove(word[0])
			else:
				new_text.remove(word[0])
				new_text.append(porter.stem(word[0]))
		return new_text
	
	def user_profile(self, news):
		try:
			self.tweets = pickle.load(open('parser.pickle', 'rb'))
		
		except:
			a= self.parser()
			pickle.dump(a, open('parser.pickle', 'wb'))
		
		personalized = {}
		cnews=[]
		hnews=[]
		rex = re.compile(r'@(\S+)')
		
		for n in news['hits']['hits']:
			us= ""
			cnews.append(n['_source']['text'])
			match_pattern = rex.findall(n['_source']['text'])
			for u in match_pattern:
				us += " " + u
				hnews.append(us)
			if len(match_pattern)<1:
				hnews.append(" ")
			
		
		for user in self.tweets:
			st = ""
			hg = ""
			
			for tweet in self.tweets[user]['tweets']:
				st += " " + self.tweets[user]['tweets'][tweet]['text']
				users= self.tweets[user]['tweets'][tweet]['user']
				for u in users:
					hg += " " + u
		
			vectoriser = TfidfVectorizer(analyzer=self.preprocess_text, min_df=0.01)
			vectoriser2 = TfidfVectorizer(analyzer=self.preprocess_text, min_df=0.01)
			
			corpus = [st]
			corpus2 = [hg]
			
			X = vectoriser.fit_transform(corpus)
			Y = vectoriser.transform(cnews)
			
			X2 = vectoriser2.fit_transform(corpus2)
			Y2 = vectoriser2.transform(hnews)
			
			similarity = cosine_similarity(X, Y)
			similarity2 = cosine_similarity(X2, Y2)
			
			
			Pnews= pd.DataFrame(Y.toarray())
			Hnews= pd.DataFrame(Y2.toarray())
			
			Pnews['score']= similarity[0]
			Hnews['score']= similarity2[0]
			
			filtered= news['hits']['hits']
			i=0
			for n in filtered:
				n['new_score']= 0.2*n['_score']+0.3*Pnews['score'][i]+0.5*Hnews['score'][i]
				i+=1
				
			
			from operator import itemgetter
			ordered = sorted(filtered, key=itemgetter('new_score'), reverse=True)
			personalized[user]={'news': ordered}
	
		return personalized
