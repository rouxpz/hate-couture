#!/usr/local/bin/python

import feedparser
import nltk
from bs4 import BeautifulSoup
import nltk
import yaml

class Tokenizer(object):
	def __init__(self):
		self.nltk_splitter = nltk.data.load('tokenizers/punkt/english.pickle')
		self.nltk_tokenizer = nltk.tokenize.TreebankWordTokenizer()

	def split(self, text):
		sentences = self.nltk_splitter.tokenize(text)
		tokenized = [self.nltk_tokenizer.tokenize(sent) for sent in sentences]
		return tokenized


class POSTagger(object):

	def __init__(self):
		pass

	def pos_tag(self, sentences):
		pos = [nltk.pos_tag(sentence) for sentence in sentences]
		pos = [[(word, word, [postag]) for (word, postag) in sentence] for sentence in pos]
		return pos

class DictionaryTagger(object):

	def __init__(self, dictionary_paths):
		files = [open(path, 'r') for path in dictionary_paths]
		dictionaries = [yaml.load(dict_file) for dict_file in files]
		map(lambda x: x.close(), files)
		self.dictionary = {}
		self.max_key_size = 0
		for curr_dict in dictionaries:
			for key in curr_dict:
				if key in self.dictionary:
					self.dictionary[key].extend(curr_dict[key])
				else:
					self.dictionary[key] = curr_dict[key]
					self.max_key_size = max(self.max_key_size, len(key))

	def tag(self, tagged_sentences):
		return [self.tag_sentence(sentence) for sentence in tagged_sentences]

	def tag_sentence(self, sentence, tag_with_lemmas=False):
		tag_sentence = []
		N = len(sentence)
		if self.max_key_size == 0:
			self.max_key_size = N
		i = 0
		while (i < N):
			j = min(i + self.max_key_size, N)
			tagged = False
			while (j > i):
				expression_form = ' '.join([word[0] for word in sentence[i:j]]).lower()
				expression_lemma = ' '.join([word[1] for word in sentence[i:j]]).lower()
				if tag_with_lemmas:
					literal = expression_lemma
				else:
					literal = expression_form
				if literal in self.dictionary:
					is_single_token = j - i == 1
					original_position = i
					i = j
					taggings = [tag for tag in self.dictionary[literal]]
					tagged_expression = (expression_form, expression_lemma, taggings)
					if is_single_token:
						original_token_tagging = sentence[original_position][2]
						tagged_expression[2].extend(original_token_tagging)
					tag_sentence.append(tagged_expression)
					tagged = True
				else:
					j = j - 1
			if not tagged:
				tag_sentence.append(sentence[i])
				i += 1
		return tag_sentence

def value(sentiment):
	if sentiment == 'first': 
		return 0.5
	elif sentiment == 'second':
		return 1
	elif sentiment == 'third':
		return 1.5
	elif sentiment == 'fourth':
		return 2
	elif sentiment == 'positive':
		return -1.5
	else:
		return 0

def sentiment_total(review):
	return sum([value(tag) for sentence in review for token in sentence for tag in token[2]])

#script, filename = argv

def reddit_scrape(query):

	d = feedparser.parse(query)

	for e in d.entries:

		tokenizer = Tokenizer()
		postagger = POSTagger()
		tagger = DictionaryTagger(['positive.yml', 'tier1.yml', 'tier2.yml', 'tier3.yml', 'tier4.yml'])

		raw_title = unicode.encode(e.title, "utf-8")
		raw_description = unicode.encode(e.description, "utf-8")
		#pubdate = unicode.encode(e.published, "utf-8")

		dsoup = BeautifulSoup(raw_description)

		description = dsoup.p
		title = dsoup.h1

		full = str(title) + str(description)
		final = full.replace('<p>', '').replace('</p>', '').replace('<h1>', '').replace('</h1>', ':').replace('<em>', '').replace('<br/>', '')
	#print final
		tokens = tokenizer.split(final)
		pos = postagger.pos_tag(tokens)
		tagged = tagger.tag(pos)
		total = '%r' % sentiment_total(tagged)

		target.write(final)
		target.write('|')
		target.write(total)
		target.write('\n')

print "Opening the file."

filename = 'reddit_faggot.txt'
target = open(filename, 'a')

reddit_scrape('http://metareddit.com/monitor/gzoD0/fags.rss')
target.write('\n')
reddit_scrape('http://metareddit.com/monitor/S44U1/niggah.rss')
target.write('\n')

print "All done!"

