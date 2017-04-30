#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Call the Program bleu-champ to align the titles
'''

import os
import sys

#Make a list of files for a given path
def list_of(path):
	return [x for x in os.listdir(path) if os.path.isdir(path+'/'+x)]

#Return the filePath that matches the string
def take_(path):
	for f in os.listdir(path):
		if 'doc_titles.lower' in f:
			return path+f

#Set a new file name to save the results
def change_name(f, lang_s, lang_t):
	f=f.split('/')
	f[-1]='alignment3_'+lang_s+'-'+lang_t
	return '/'.join(f)

#Prepare bleu-champ call
def bleuchamp_call(source, output):
	target = source.split('/')
	target[6]='DATA_'+lang_t
	target[-1]='doc_titles.trans3.'+lang_s
	target = '/'.join(target)
	call = 'bleu-champ -s '+source+' -t '+target+' --skip-2nd -i -u -b -p > '+output
	return call

#Check user input[1]
available_langs = ['de','fr','it']
try:
	lang_s =  sys.argv[1]
	if lang_s not in available_langs:
		print 'Selected language is not available'
		sys.exit()

except:
	sys.exit('Select a language: de, fr or it')

#Check user input[2]
try:
	lang_t =  sys.argv[2]
	if lang_t not in available_langs:
		print 'Selected language is not available'
		sys.exit()

except:
	sys.exit('Select a language: de, fr or it')

path = '/mnt/storage/bender/users/meyeradriano/DATA_'+lang_s

#Iterate through files
for year in sorted(list_of(path)):
	for date in sorted(list_of(path+'/'+year)):
		#Prepare output filePath
		f= take_(path+'/'+year+'/'+date+'/')
		f_new = change_name(f,lang_s, lang_t)
		#Prepare the call
		call = bleuchamp_call(f, f_new)	
		print call
		os.system(call)


	


