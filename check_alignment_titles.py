#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Check the alignment files from bleuchamp.py to extract those titles that are aligned from both sides
$ python check_alignment_titles.py de fr
'''

from __future__ import division

import sys
import os
import itertools
import codecs

#Open a txt file
def open_file(path):
	result=list()
	with codecs.open(path, 'r', 'utf-8') as ix:
		for line in ix:
			result.append(line.strip())
	return result

#Open bleu-champ file
def open_bleuchamp_file(path):
	result=list()
	with codecs.open(path, 'r', 'utf-8') as ix:
		for line in ix:
			infos=dict()
			line=line.split(u'\t')
			#Save the alignment indexes, beads and scores
			infos['alignment']= line[0]
			infos['bead']= line[1]
			infos['score']=float(line[2])
			result.append( infos )
	return result

#Prepare data to compare alingment
def take_alignments(A,B):
	aligned=list()
	scores=list()
	rest = list()
	for element in A:
		if element['bead'] == u'1-1':
			check,score = check_alignment(B, element['alignment'], element['bead'])
			if check:
				subresult=list()
				subresult.append(element['alignment'])
				subresult.append((score+element['score'])/2)
				aligned.append(subresult)
			else:
				rest.append(element['alignment'])
		else:
			rest.append(element['alignment'])
	return aligned

#Check if a given alignment is aligned from both sides
def check_alignment(S, alignment, bead):
	alignment_L = alignment.split()
	bead_L = bead.split(u'-')

	for element in S:
		alignment_S = element['alignment'].split()
		bead_S = element['bead'].split(u'-')
		
		#bidirectional check
		if bead_L[0] == bead_S[1] and bead_L[1] == bead_S[0] and alignment_L[0] == alignment_S[1] and alignment_L[1] == alignment_S[0]:
			return True, element['score']
	return False, 0

#Make a list of files for a given path
def list_of(path):
	return [x for x in os.listdir(path) if os.path.isdir(path+'/'+x)]

#Return the filePath that matches the string
def take_(path,fileName):
	for f in os.listdir(path):
		if fileName in f:
			return path+f

#Set a new file name to save the results
def change_name(f, lang_s, lang_t):
	f=f.split('/')
	f[-1]='alignment3_'+lang_t+'-'+lang_s
	f[6] = 'DATA_'+lang_t
	return '/'.join(f)

#Prepare output file with alignments
def make_info_list(A,B,path_s, path_t):
	result=list()

	infos_s=open_file(path_s)
	infos_t=open_file(path_t)

	path_s=path_s.split('/')
	path_s=path_s[:-1]
	path_s='/'.join(path_s)+'/'

	path_t=path_t.split('/')
	path_t=path_t[:-1]
	path_t='/'.join(path_t)+'/'

	
	a = take_alignments(A,B)
	
	if len(a) == 0:
		return result
	else:
		
		for align in a:
			subresult=list()

			index_s, index_t = align[0].split()
			s=infos_s[int(index_s)].split(u'\t')
			subresult.append(path_s+s[0]+'.tetml')
			subresult.append(s[2])
			t=infos_t[int(index_t)].split(u'\t')
			subresult.append(path_t+t[0]+'.tetml')
			subresult.append(t[2])
			subresult.append(str(align[1]))
		
			result.append( u'\t'.join(subresult) )
		
		return result

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

#Crate Folder for results
directory= 'alignment_results'
if not os.path.exists(directory):
	os.makedirs(directory)

path_s = '/mnt/storage/bender/users/meyeradriano/DATA_'+lang_s
path_t = '/mnt/storage/bender/users/meyeradriano/DATA_'+lang_t

#Two Output files, one for the alignments, the other for errors
ox_err = codecs.open(directory+'/out_err', 'w','utf-8')
ox= codecs.open(directory+'/out'+lang_s+'-'+lang_t, 'w','utf-8')

#Iterate through files
for year in sorted(list_of(path_s)):
	for date in sorted(list_of(path_s+'/'+year)):

		s= take_(path_s+'/'+year+'/'+date+'/' , 'alignment3_'+lang_s+'-'+lang_t)
		t = change_name(s, lang_s, lang_t)
		try:
			A = open_bleuchamp_file(s)
			B = open_bleuchamp_file(t)
		except: 
			ox_err.write(s+'\n')
			#ox_err.write(t+'\n')
			continue

		info_path_s= path_s+'/'+year+'/'+date+'/'+date
		info_path_t= path_t+'/'+year+'/'+date+'/'+date
		
		alignment_list=make_info_list(A,B,info_path_s, info_path_t)


		if len(alignment_list)!=0:
			for alignment in alignment_list:
				ox.write(alignment+u'\n')
		else:
			continue

		
	
ox.close()
ox_err.close()
