#!/usr/local/bin/python

import feedparser
import nltk
from bs4 import BeautifulSoup

#script, filename = argv

d = feedparser.parse('http://metareddit.com/monitor/Bjqv2/nigger.rss')

#print "Opening the file."

#filename = 'reddit_nigger_TESTRUN.txt'
#target = open(filename, 'a')

for e in d.entries:
	raw_title = unicode.encode(e.title, "utf-8")
	raw_description = unicode.encode(e.description, "utf-8")
	#pubdate = unicode.encode(e.published, "utf-8")

	dsoup = BeautifulSoup(raw_description)

	description = dsoup.p
	title = dsoup.h1

	full = str(title) + str(description)
	final = full.replace('<p>', '').replace('</p>', '').replace('<h1>', '').replace('</h1>', '|')
	print final

	#dclean = nltk.clean_html(description)
	#tclean = nltk.clean_html(title)
	#tokens = nltk.word_tokenize(dclean)
	#print tokens

	#target.write(str(title))
	#target.write(str(description))
	#target.write('|')
	#target.write('\n')
	#target.write('\n')

#print "All done!"

