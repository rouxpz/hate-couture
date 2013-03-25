#!/usr/local/bin python

#"Hate Couture", thesis project at ITP-NYU
#this script scrapes youtube comment results from google and analyzes them according to a custom sentiment analysis library.

import sys # Used to add the BeautifulSoup folder the import path
import urllib2 # Used to read the html document
import json
import nltk
import yaml

from bs4 import BeautifulSoup

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


def youtube_scrape(query, j):

    ### Create opener with Google-friendly user agent
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    tokenizer = Tokenizer()
    postagger = POSTagger()
    tagger = DictionaryTagger(['positive.yml', 'tier3.yml', 'tier2.yml', 'tier1.yml', 'tier4.yml'])
    ### Open page & generate soup
    ### the "start" variable will be used to iterate through 10 pages.
    for start in range(0,j):
        url = query + str(start*10)
        page = opener.open(url)
        soup = BeautifulSoup(page)

        text = soup.find_all(class_="st")
        l = len(text)
        #print l

        for i in range(0,l):
            #coded = unicode.decode(text[i], "utf-8")
            coded = (str(text[i]))
            clean = coded.replace('<b>', '').replace('</b>', '').replace('<span class="st">', '').replace('</span>', '').replace('<br/>', '')
            tokens = tokenizer.split(clean)
            pos = postagger.pos_tag(tokens)
            tagged = tagger.tag(pos)
            total = '%r' % sentiment_total(tagged)
            target.write(clean)
            target.write('|')
            target.write(total)
            target.write('\n')

print "Opening the file..."

filename = 'youtube_muslim.txt'
target = open(filename, 'a')

youtube_scrape('http://www.google.com/search?q=raghead+site:youtube.com/all_comments&hl=en&authuser=0&biw=1532&bih=745&tbs=sbd:1,qdr:d&filter=0&start=', 1)
youtube_scrape('http://www.google.com/search?q=towelhead+site:youtube.com/all_comments&hl=en&authuser=0&biw=1532&bih=745&tbs=sbd:1,qdr:d&filter=0&start=', 1)
youtube_scrape('http://www.google.com/search?q="sand monkey"+site:youtube.com/all_comments&hl=en&authuser=0&biw=1532&bih=745&tbs=sbd:1,qdr:d&filter=0&start=', 1)
youtube_scrape('http://www.google.com/search?q=sandmonkey+site:youtube.com/all_comments&hl=en&authuser=0&biw=1532&bih=745&tbs=sbd:1,qdr:d&filter=0&start=', 1)
youtube_scrape('http://www.google.com/search?q="sand nigger"+site:youtube.com/all_comments&hl=en&authuser=0&biw=1532&bih=745&tbs=sbd:1,qdr:d&filter=0&start=', 1)
youtube_scrape('http://www.google.com/search?q=sandnigger+site:youtube.com/all_comments&hl=en&authuser=0&biw=1532&bih=745&tbs=sbd:1,qdr:d&filter=0&start=', 1)
target.write('\n')

print "All done!"