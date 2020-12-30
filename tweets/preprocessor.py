
from numpy import *
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
import emoji
import json

#nltk.download('stopwords')
#nltk.download('wordnet')
#nltk.download('averaged_perceptron_tagger')

class Preprocessor:
	def __init__(self, filesName):
		self.fileNames = filesName
		self.tweets= {}
		self.freq_text= Counter()
		self.freq_user=Counter()
		self.freq_links=Counter()
		self.freq_emoji=Counter()
		self.freq_hashtags=Counter()

	def generate_tokens(self, tweet, data):
		'''
		Creates a unique set of tokens that were identified after processing, filtering and lemmatize the corpus text.:
		:param tweet: tweet id to identify the corresponding tweet inside the tweets dictionary 'data';
		:return: a list that contains the parsed text
		'''
		stopwords.words('english')
		stop_words = nltk.corpus.stopwords.words('english')
		functional_words = ["ADP", "AUX", "CCONJ", "DET", "NUM", "PART", "PRON", "SCONJ", "PUNCT", "SYM", "X"]
		wordnet_lemmatizer = WordNetLemmatizer()
		
		text = data[tweet]['text']
		new_text = text.lower()
		new_text = re.sub(r'—|’|’’|-|”|“', ' ', new_text)
		new_text = new_text.strip()
		new_text = re.sub(r'\d+', '', new_text)
		new_text = new_text.translate(str.maketrans('', '', string.punctuation))
		new_text = WordPunctTokenizer().tokenize(new_text)

		tagged = nltk.pos_tag(new_text)
		for word in tagged:
			if word[0] not in stop_words and word[1] not in functional_words:
				lemma = wordnet_lemmatizer.lemmatize(word[0], pos="v")
				if lemma not in stop_words:
					self.freq_text[lemma] += 1
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
		emojis= []
		for pos, c in enumerate(text):
			if c in emoji.UNICODE_EMOJI:
				# print("Matched!!", c, c.encode("ascii", "backslashreplace"))
				self.freq_emoji[c] += 1
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
			self.freq_user[us] += 1
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
			self.freq_links[us] += 1
			group.append(us)
 
		return group
			
	def identify_hashtags(self, tweet, data):
		'''
		Identifies and return all hashtags who are present inside the single tweet:
		:param tweet: tweet id to identify the corresponding tweet inside the tweets dictionary 'data';
		:return: a list that contains all hashtags identified inside the text
		'''
		if not data[tweet]['hashtags'] == [None]:
			self.freq_hashtags[data[tweet]['hashtags'][0][0]] += 1
			return data[tweet]['hashtags'][0][0]
	
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
				
				tokenized= self.generate_tokens(tweet, data)
				emoji= self.identify_emoji(tweet, data)
				links = self.identify_links(tweet, data)
				hashtags= self.identify_hashtags(tweet, data)
				user= self.identify_user(tweet, data)
				self.tweets[tweet]= {'author': data[tweet]['user_name'], 'text': data[tweet]['text'], 'tokenized': tokenized, 'user': user, 'hashtags': hashtags, 'emoji': emoji, 'links': links}
				
		return self.tweets, self.freq_text, self.freq_user, self.freq_hashtags, self.freq_links, self.freq_emoji

processor = Preprocessor(["group_one.json", "group_two.json"])
processor.parser()

