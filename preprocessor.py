import re
import string
import emoji
import json
import pandas as pd
import nltk
import pickle
from os import path
import numpy as np
from nltk import word_tokenize, sent_tokenize, pos_tag
from nltk.tokenize import WordPunctTokenizer, RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import preprocessing
from collections import Counter, OrderedDict
from operator import itemgetter

# Da utilizzare solo per la prima esecuzione
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')

class Preprocessor:
	def __init__(self, filesName):
		self.fileNames = filesName
		self.tweets = {'tweets': {}, 'frequency': {}}
		self.freq_text = dict()
		self.freq_user = dict()
		self.freq_links = dict()
		self.freq_emoji = dict()
		self.freq_hashtags = dict()
		self.TFD = {}
		self.data = {}
		self.porter = PorterStemmer()
		stopwords.words('english')
		self.stop_words = nltk.corpus.stopwords.words('english')
		self.functional_words = ["ADP", "AUX", "CCONJ", "DET", "NUM", "PART", "PRON", "SCONJ", "PUNCT", "SYM", "X"]
	
	def filter(self, text):
		'''
		Parse the text parameter, consists in following steps: lowercaps, filter it removing numbers, special 
		characters, punctuation and text's tokenize.
		Remove from it all tweet's element that are not word.
		:param text: text of the tweet that must be filtered;
		:return: the new_text filtered and POS tag associated with token
		'''
		new_text = re.sub('http\S+', '', text)
		new_text = re.sub('@[^\s]+', '', new_text)
		new_text = new_text.lower()
		new_text = re.sub(r'—|’|’’|-|”|“|‘', ' ', new_text)
		new_text = new_text.strip()
		new_text = re.sub(r'\d+', '', new_text)
		new_text = new_text.translate(str.maketrans('', '', string.punctuation))
		new_text = WordPunctTokenizer().tokenize(new_text)
		
		tagged = nltk.pos_tag(new_text)
		
		return new_text, tagged
	
	def generate_tokens(self, tweet, text):
		'''
		Creates a unique set of tokens that were identified after processing, filtering and lemmatize the corpus text.:
		Remove from it functional and stop words and execute stemming's operation for each word.
		:param tweet: tweet id to identify the corresponding tweet and the corresponding text;
		:return: a list that contains the parsed text
		'''
		
		new_text, tagged = self.filter(text)
		
		for word in tagged:
			if word[0] not in self.stop_words and word[1] not in self.functional_words:
				lemma = self.porter.stem(word[0])
				if lemma not in self.stop_words:
					self.freq_text[self.data[tweet]['user_name']][lemma] += 1
					new_text.remove(word[0])
					new_text.append(lemma)
			else:
				new_text.remove(word[0])
		return new_text
	
	def identify_emoji(self, tweet, text):
		'''
		Identifies and return all emojis who are present inside the single tweet:
		:param tweet: tweet id to identify the corresponding tweet inside the tweets dictionary 'data';
		:return: a list that contains all emojis identified inside the text
		'''
		
		emojis = []
		for pos, c in enumerate(text):
			if c in emoji.UNICODE_EMOJI:
				# print("Matched!!", c, c.encode("ascii", "backslashreplace"))
				self.freq_emoji[self.data[tweet]['user_name']][c] += 1
				emojis.append(c)
		
		return emojis
	
	def identify_user(self, tweet, text):
		'''
		Identifies and return all user_id who are presents inside the single tweet:
		:param tweet: tweet id to identify the corresponding tweet inside the tweets dictionary 'data';
		:return: a list that contains all user_id identified inside the text
		'''
		users = []
		
		user = re.compile(r'@(\S+)')
		match_pattern = user.findall(text)
		for us in match_pattern:
			self.freq_user[self.data[tweet]['user_name']][us] += 1
			users.append(us)
		
		return users
	
	def identify_links(self, tweet, text):
		'''
		Identifies and return all URLs who are presents inside the single tweet:
		:param tweet: tweet id to identify the corresponding tweet inside the tweets dictionary 'data';
		:return: a list that contains all URLs identified inside the text
		'''
		group = []
		
		link = re.compile(r'http\S+')
		links = link.findall(text)
		for us in links:
			self.freq_links[self.data[tweet]['user_name']][us] += 1
			group.append(us)
		
		return group
	
	def identify_hashtags(self, tweet, hashtags):
		'''
		Identifies and return all hashtags who are present inside the single tweet:
		:param tweet: tweet id to identify the corresponding tweet inside the tweets dictionary 'data';
		:return: a list that contains all hashtags identified inside the text
		'''
		if not hashtags == [None]:
			for i in self.data[tweet]['hashtags'][0]:
				self.freq_hashtags[self.data[tweet]['user_name']][i] += 1
			return self.data[tweet]['hashtags']
	
	def parser(self):
		'''
		Transforms all the corpus in the filesName insert them into dictionary whit tweets ids as keys and their 
		attributes as values into a similar dictionary with more attributes for the same tweet as tokenized message, 
		emojis, URLs, and user_id that are contained into original tweet.

		:return: a list of dictionaries for each tweet, containing their id, author, original text, tokenized text, 
				 hashtags, user_ids, emoji, and URLs;
				 five corpus_counter of the words, emoji, hashtags, URLs and user_ids and their corresponding frequencies.
		'''
				for file in self.fileNames:
			self.data = json.load(open(file))
			for tweet in self.data:
				if not self.data[tweet]['user_name'] in self.freq_text:
					self.tweets['tweets'][self.data[tweet]['user_name']] = {}
					self.tweets['frequency'][self.data[tweet]['user_name']] = {}
					self.freq_text[self.data[tweet]['user_name']] = Counter()
					self.freq_emoji[self.data[tweet]['user_name']] = Counter()
					self.freq_links[self.data[tweet]['user_name']] = Counter()
					self.freq_hashtags[self.data[tweet]['user_name']] = Counter()
					self.freq_user[self.data[tweet]['user_name']] = Counter()
				
				tokenized = self.generate_tokens(tweet, self.data[tweet]['text'])
				emoji = self.identify_emoji(tweet, self.data[tweet]['text'])
				links = self.identify_links(tweet, self.data[tweet]['text'])
				hashtags = self.identify_hashtags(tweet, self.data[tweet]['hashtags'])
				user = self.identify_user(tweet, self.data[tweet]['text'])
				self.tweets['tweets'][self.data[tweet]['user_name']][tweet] = {'author': self.data[tweet]['user_name'],
																			   'date': self.data[tweet]['date'],
																		  'text': self.data[tweet]['text'],
																		  'tokenized': tokenized, 'user': user,
																		  'hashtags': hashtags, 'emoji': emoji,
																		  'links': links}
		
		self.tweets['frequency']= {'freq_text': self.freq_text,
								  'freq_user': self.freq_user,
								  'freq_hashtags': self.freq_hashtags,
								  'freq_links': self.freq_links,
								  'freq_emoji': self.freq_emoji}
		
		return self.tweets
	
	def preprocess_text(self, text):
		'''
		Creates a unique set of tokens that were identified after processing, filtering and lemmatize the corpus text.:
		Remove from it functional and stop words and execute stemming's operation for each word.
		:param text: tweet's text;
		:return: a list that contains the parsed text
		'''
		
		new_text, tagged = self.filter(text)
		
		for word in tagged:
			if word[0] in self.stop_words or word[1] in self.functional_words:
				new_text.remove(word[0])
			else:
				new_text.remove(word[0])
				new_text.append(self.porter.stem(word[0]))
		return new_text
	
	def get_similarity_score(self, corpus, cnews):
		'''
		Compute and return similarity scores between user's tweets and news's tweets
		:param corpus: user's tweet on whom will computed the tf-idf; cnews: news's text on whom will computed tf-idf
		:return: dataframe who contain the similarity score between tweet
		'''
		
		vectoriser = TfidfVectorizer(analyzer=self.preprocess_text, min_df=0.01)
		
		X = vectoriser.fit_transform(corpus)
		Y = vectoriser.transform(cnews)
		
		similarity = cosine_similarity(X, Y)
		
		Pnews = pd.DataFrame(Y.toarray())
		Pnews['score'] = similarity[0]
		
		return Pnews
	
	def personalize_query(self, news):
		'''
		Produce user_profile for each user and then filter news based on user_profile to personalize the search
		:param news: news's text derived by Elasticsearch
		:return: news's list with a new rank
		'''

		# Try to retrive pre-calculated user profiles
		pickle_path = './parser.pickle'
		try:
			if path.exists(pickle_path):
				self.tweets = pickle.load(open(pickle_path, 'rb'))
				print("User profiles loaded correctly from " + pickle_path)

		except:
			print("User profiles tweets not yet pre-processed.")
			a = self.parser()
			print("Saving preprocessed user profiles in " + pickle_path)
			pickle.dump(a, open(pickle_path, 'wb'))
		
		personalized = {}
		cnews = []
		hnews = []
		rex = re.compile(r'@(\S+)')


		# Elasticsearch scores normalization between 0 and 1
		scores = [n['_score'] for n in news['hits']['hits']]
		scores_r = preprocessing.minmax_scale(scores)
		
		for idx, n in enumerate(news['hits']['hits']):
			n['_score']=scores_r[idx]
			us = ""
			cnews.append(n['_source']['text'])
			match_pattern = rex.findall(n['_source']['text'])
			for u in match_pattern:
				us += " " + u
				hnews.append(us)
			if len(match_pattern) < 1:
				hnews.append(" ")

		
		for user in self.tweets['tweets']:
			st = ""
			hg = ""

			for tweet in self.tweets['tweets'][user]:
				st += " " + self.tweets['tweets'][user][tweet]['text']
				users = self.tweets['tweets'][user][tweet]['user']
				for u in users:
					hg += " " + u
			
			corpus = [st]
			corpus2 = [hg]
			
			Pnews = self.get_similarity_score(corpus, cnews)
			Hnews = self.get_similarity_score(corpus2, hnews)
			
			# Personalized scoring
			filtered = news['hits']['hits']
			for i, n in enumerate(filtered):
				n['new_score'] = np.around(0.2 * n['_score'] + 0.3 * Pnews['score'][i] + 0.5 * Hnews['score'][i], 
											decimals=6)

			
			# Re-ranking Elasticsearch query results
			ordered = sorted(filtered, key=itemgetter('new_score'), reverse=True)
			personalized[user] = {'news': ordered}
		
		return personalized

