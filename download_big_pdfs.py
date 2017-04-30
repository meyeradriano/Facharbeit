#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Download PDFs that were too big for Bundesblatt_scrape_1999-2016.py or Bundesblatt_scrape_1849-1999.py
$ python download_big_pdfs.py list_as_file
'''

import sys
import urllib2
import time
import os
from lxml import etree

#Crate a list from given File
def open_list(filePath):
	result=list()
	with open(filePath) as ix:
		for line in ix:
			result.append(line.strip())

	return result

#Extract file id from file-path
def extract_id(filePath):
	filePath = filePath.split('/')
	idd = filePath[-1][:-4]
	path = filePath[:-1]
	path = '/'.join(path)+'/'
	
	return idd, path

try:
	filePath =  sys.argv[1]
except:
	sys.exit('No external File given')

file_list = open_list(filePath)

#Iterate through files to download
for f in file_list:
	print f
	idd, path = extract_id(f)
	print idd, path
	url = 'https://www.amtsdruckschriften.bar.admin.ch/viewOrigDoc.do?id='+idd+'&action=open'
	

	print 'Downloading PDF ...'
	response = urllib2.urlopen(url)
	file_name = idd+'.pdf'
	file = open(path+file_name, 'w')
	file.write(response.read())
	file.close()

	print 'Converting to tetml and extracting text'
	f_new= idd+'.rawtext'
	extract_text_call = 'tet -o '+path+f_new+' '+path+file_name
	convert_tetml_call = 'tet --samedir -m word '+path+file_name

	os.system(extract_text_call)
	os.system(convert_tetml_call)

	#Sleep for 3 sec
	print 'Sleeping 3 sec ...'
	time.sleep(3)
	print''
	


