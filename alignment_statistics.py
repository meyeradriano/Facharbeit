#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Extract number of pages, words and letters to compute similarity
$ python alignment_statistics.py file
'''

from __future__ import division

import sys
import codecs
import itertools
import operator
from lxml import etree

#Read the TETML files to extract the informations
def doc_chars(filePath):
	parser = etree.XMLParser(ns_clean=True)
	tree = etree.parse(open(filePath),parser)
	root = tree.getroot()
	
	#Number of pages
	number_of_pages = len( tree.xpath('//x:Page', namespaces = {'x':'http://www.pdflib.com/XML/TET3/TET-3.0'}) )

	text = tree.xpath('//text()', namespaces = {'x':'http://www.pdflib.com/XML/TET3/TET-3.0'})
	text = [x for x in text if '\n' not in x and 'tetml={}' not in x]

	#Number of words
	number_of_words = len(text)

	#Number of letters
	number_of_chars = len( ''.join(text) )

	return number_of_pages, number_of_words, number_of_chars


#Check user input
try:
	filePath =  sys.argv[1]

except:
	sys.exit('No file given')

ox = codecs.open('alignment_results/'+filePath[-5:]+'_out3','w','utf-8')

#Iterate through the file
with codecs.open(filePath, 'r','utf-8') as ix:
	index=1
	for line in ix:
		print 'Line:', index
		line=line.strip()
		line=line.split('\t')
		pages_s, words_s, chars_s  = doc_chars(line[0])
		pages_t, words_t, chars_t = doc_chars(line[2])

		#Pages
		similarity_pages = min(pages_s, pages_t) / max(pages_s, pages_t)
		line.append(unicode(similarity_pages))

		#Words	
		similarity_words = min(words_s, words_t) / max(words_s, words_t)
		line.append(unicode(similarity_words))

		#Chars
		similarity_chars = min(chars_s, chars_t) / max(chars_s, chars_t)
		line.append(unicode(similarity_chars))

		ox.write( u'\t'.join(line)+u'\n' )
		index+=1

ox.close()
