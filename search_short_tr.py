#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Search small titles (<3 tokens)
'''

import os
import sys
import codecs
import operator

#Make a list of files for a given path
def list_of(path):
	return [x for x in os.listdir(path) if os.path.isdir(path+'/'+x)]

#Return the filePath that matches the string
def take(path):
	for f in os.listdir(path):
		if 'doc_titles.lower' in f:
			return path+'/'+f

#Extract the short Titles
def extract_short_titles(path):
	result=list()
	with codecs.open(path,'r','utf-8') as ix:
		for line in ix:
			line = line.strip()
			line_list = line.split()
			if len(line_list)<=3:
				result.append(line)
	return result

#Extract full titles
def extract_titles(path):
	result=list()
	with codecs.open(path,'r','utf-8') as ix:
		for line in ix:
			line = line.strip()
			result.append(line)
	return result

def update_dict(title_list, d):
	for t in title_list:
		if t not in d.keys():
			d[t] = 1
		else:
			d[t]+= 1

#Check user input
available_langs = ['de','fr','it']
try:
	lang_s =  sys.argv[1]
	if lang_s not in available_langs:
		print 'Selected language is not available'
		sys.exit()

except:
	sys.exit('Select a language: de, fr or it')

path_s = '/mnt/storage/bender/users/meyeradriano/DATA_'+lang_s

dict_s = dict()
dict_t = dict()

#Search for titles
for year in sorted(list_of(path_s)):
	for date in sorted(list_of(path_s+'/'+year)):
		#s
		file_s = take(path_s+'/'+year+'/'+date)
		short=extract_short_titles(file_s)
		update_dict(short, dict_s)

		
		

#Sort the titles by freq that were found
dict_s_sorted = sorted(dict_s.items(), key=operator.itemgetter(1), reverse=True)

#Write results in a file
with codecs.open(lang_s+'.short_all','w','utf-8') as ox:
	for e in dict_s_sorted[:50]:
		ox.write(e[0]+u'\t'+unicode(e[1])+u'\n')


