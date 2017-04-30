#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Translate the titles with moses. Start first in a separate tmux-session the moses-server and load your Translationmodel (moses.ini)
Ex: 
$ ./mosesdecoder/bin/moses -f moses/working_fr-it/experiments_3/binarised-model/moses.ini.1 --server --server-port 12345

Make sure that you start the script giving the correct port
Ex:
$ python mosesclient_titles.py fr it 12345

'''
import os
import sys
import codecs
import xmlrpclib

#Make a list of files for a given path
def list_of(path):
	return [x for x in os.listdir(path) if os.path.isdir(path+'/'+x)]

#Return the filePath that matches the string
def take_(path):
	for f in os.listdir(path):
		if 'doc_titles.lower' in f:
			return path+f

#Extract the text from a given path
def extract_text(path):
	result=list()
	with codecs.open(path,'r','utf-8') as ix:
		for line in ix:
			result.append(line.strip())
	return result

#Set a new file name to save the results
def change_name(f, lang2):
	f=f.split('/')
	f[-1]='doc_titles.trans3.'+lang2
	return '/'.join(f)

#Check user input[1]
available_langs = ['de','fr','it']
try:
	lang =  sys.argv[1]
	if lang not in available_langs:
		print 'Selected language is not available'
		sys.exit()

except:
	sys.exit('Select a language: de, fr or it')

#Check user input[2]
try:
	lang2 =  sys.argv[2]
	if lang2 not in available_langs:
		print 'Selected language is not available'
		sys.exit()

except:
	sys.exit('Select a language: de, fr or it')

#Check user input[3]
try:
	port =  sys.argv[3]

except:
	sys.exit('No Port given')


path = '/mnt/storage/bender/users/meyeradriano/DATA_'+lang

#Connect with the moses-server
url = 'http://localhost:'+port+'/RPC2'
server = xmlrpclib.ServerProxy(url, verbose=False)

#Iterate through files and Translate
for year in sorted(list_of(path)):
	for date in sorted(list_of(path+'/'+year)):
		print 'Translating:',date

		#Prepare output filePath
		f= take_(path+'/'+year+'/'+date+'/')
		f_new = change_name(f, lang2)
		#Extract text
		texts=extract_text(f)
		ox = codecs.open(f_new,'w','utf-8')
		#Translate
		for text in texts:
			answer = server.translate({u'text':text})
			ox.write(answer[u'text']+u'\n')
		ox.close()

	
		
	

	
	


