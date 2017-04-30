#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Call moses scripts to preprocess data. User has to adapt the file paths according to where moses is installed.
$ python preprocess_titles.py de
'''

import os
import sys

#Make a list of files for a given path
def list_of(path):
	return [x for x in os.listdir(path) if os.path.isdir(path+'/'+x)]

#Return the filePath that matches the string
def take_(path):
	for f in os.listdir(path):
		if 'doc_titles.tok' in f:
			return path+f

#Set a new file name to save the results
def change_name(f):
	f=f.split('/')
	f[-1]='doc_titles.lower'
	return '/'.join(f)

#Moses Lowercaser
def lowercase(f, f_new)
	moses_lowercaser = './mosesdecoder/scripts/tokenizer/lowercase.perl '
	return moses_lowercaser+' < '+f+' > '+f_new

#Moses Truecaser
def truecaser(lang,f, f_new):
	truecase_model = './moses/working_de-fr/experiments_2/truecaser/truecase-model.1.'+lang
	moses_truecaser = './mosesdecoder/scripts/recaser/truecase.perl --model '
	returnmoses_truecaser+truecase_model+' < '+f+ ' > '+f_new

#Moses Tokenizer
def tokenizer(lang,f, f_new):
	moses_tokenizer = './mosesdecoder/scripts/tokenizer/tokenizer.perl -l '+lang
	return moses_tokenizer+' < '+f+' > '+f_new

#Check user input
available_langs = ['de','fr','it']
try:
	lang =  sys.argv[1]
	if lang not in available_langs:
		print 'Selected language is not available'
		sys.exit()

except:
	sys.exit('Select a language: de, fr or it')


path = '/mnt/storage/bender/users/meyeradriano/DATA_'+lang

#Iterate through files
for year in sorted(list_of(path)):
	for date in sorted(list_of(path+'/'+year)):
		#Prepare output filePath
		f= take_(path+'/'+year+'/'+date+'/')
		f_new = change_name(f)
		#Prepare Call
		call = lowercase(f, f_new)
		print call
		os.system(call)



