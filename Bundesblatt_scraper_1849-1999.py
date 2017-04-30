#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Scraper to iterate through the PDFs in https://www.admin.ch from 1849 to 1999.

$ python Bundesblatt_scraper_1849-1999 de
'''
import sys
from lxml import etree
import urllib2
import os
import codecs
from selenium import webdriver
import time


def transform_date(date, lang):
	months_it = {	'gennaio':'01',
			'febbraio':'02',
			'marzo':'03',
			'aprile':'04',
			'maggio':'05',
			'giugno':'06',
			'luglio':'07',
			'agosto':'08',
			'settembre':'09',
			'ottobre':'10',
			'novembre':'11',
			'dicembre':'12'}

	months_de = {	'Januar':'01',
			'Februar':'02',
			u'M\xe4rz':'03',
			'April':'04',
			'Mai':'05',
			'Juni':'06',
			'Juli':'07',
			'August':'08',
			'September':'09',
			'Oktober':'10',
			'November':'11',
			'Dezember':'12'}

	months_fr = {	'janvier':'01',
			u'f\xc3\xa9vrier':'02',
			'mars':'03',
			'avril':'04',
			'mai':'05',
			'juin':'06',
			'juillet':'07',
			u'ao\xc3\xbbt':'08',
			'septembre':'09',
			'octobre':'10',
			'novembre':'11',
			u'd\xc3\xa9cembre':'12'}

	date=date.split()
	if lang == 'it':
		return date[0]+'-'+months_it[date[1]]+'-'+date[2]
	if lang == 'de':
		return date[0][:-1]+'-'+months_de[date[1]]+'-'+date[2]
	if lang == 'fr':
		return date[0]+'-'+months_fr[date[1]]+'-'+date[2]

def create_directory(name, path):
	if path[-1]=='/':
		path=path[:-1]
	if not os.path.exists(name):
		try:
			os.makedirs(path+'/'+name)
        		
   		except OSError, e:
       			if e.errno != 17:
           			raise   
     			# time.sleep might help here
     			pass
   		
available_langs = ['de','fr','it']

try:
	lang =  sys.argv[1]
	if lang not in available_langs:
		print 'Selected language is not available'
		sys.exit()

except:
	sys.exit('Select a language: de, fr or it')

main_url = 'https://www.admin.ch'

#Year-range depending on the language. For Italian only from 1979 to 2016
years = list()
if lang == 'it':
	years = [1999]
if lang == 'fr':
	#years = range(1850,1999)
	years = [1999]
if lang == 'de':
	#years = range(1921,1999)
	years = [1999]


#Itarate through the years
for year in years:
	print 'Downloading Year:', year, 'Language:', lang
	year=str(year)
	storage = '/mnt/storage/bender/users/meyeradriano'
	path = storage+'/DATA_'+lang+'/'
	create_directory(year,path)
	
	#Download website as html file
	print 'Downloading html index ...'
	url = main_url+'/opc/'+lang+'/federal-gazette/'+year+'/index_bar.html'
	call = 'curl '+url+' >> '+path+'index.html'

	os.system(call)
		
	#print 'Sleeping 3 sec ...'
	#time.sleep(3)
	print''


	#Open the downloades html index
	parser = etree.HTMLParser()
	tree = etree.parse(open(path+'index.html'),parser)
	root = tree.getroot()

	#Find Dates to create Folders
	for element in root.iter('table',{'class': 'table table-striped'}):
		for td in element.iter('td'):
			#For every date, get the date and get the link to the next page
			#Link:
			global link
			for a in td.iter('a'):
				link = a.attrib['href']
	
			#Date:
			
			if td.get('class')=='nowrap text-right':
				continue
			if td.xpath('boolean(a/@href)'):
				continue
			if td.xpath('boolean(@colspan)'):
				continue

	
			date = transform_date(td.text, lang)
			print 'Working on:', date, 'Year:', year
			print '--------------------------------------'
			print ''
			create_directory(date,path+year)
			path_2=path+year+'/'+date+'/'

			print 'Downloading index2 ... '
			call = 'curl '+main_url+link+' >> '+path_2+'index2.html'
			os.system(call)
		
			#print 'Sleeping 3 sec ...'
			#time.sleep(3)
			print''

			#Open the downloades html index
			tree2 = etree.parse(open(path_2+'index2.html'),parser)
			root2 = tree2.getroot()
		
			for element2 in root2.iter('table',{'class': 'table table-striped'}):
				#Extract info box and download links
				infos =unicode()
				download_links = list()
				for td2 in element2.iter('td'):
					for a2 in td2.iter('a'):
						download_links.append(a2.attrib['href'])
						file_name = a2.attrib['href'][-8:]
						for span in a2.iter('span'):
							l1= span.xpath('text()')
							l2=span.xpath('b/text()')
							l=l1[0]+l2[0]+l1[1]
							l=''.join(l.split())
							l=file_name+'\t'+l
							infos+=l
							
					if td2.text!= None:
						infos+='\t'+td2.text+'\n'

				#Write the Infos in a txt file
				o=codecs.open(path_2+date,'w', 'utf-8')
				o.write(infos)
				o.close()
				

				#Download PDF files
				print 'Downloading PDFs ...'
				for href in download_links:
					response = urllib2.urlopen(href)
					
					#Crate Name for PDF-file
					file_name = href[-8:]+'.pdf'
					file = open(path_2+file_name, 'w')
					file.write(response.read())
					file.close()
				
				print 'Sleeping 3 sec ...'
				time.sleep(3)
				print''
			
		
			

	os.system('rm '+storage+'/DATA_'+lang+'/index.html')
		
print 'Script terminated'
