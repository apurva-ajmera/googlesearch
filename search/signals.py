from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Website,WebPage,Backward_Index
from html.parser import HTMLParser
import requests
import os
from pathlib import Path
import re
from bs4 import BeautifulSoup
from .forward_indexing import Forward_Index
#from .backward_indexing import Backward_Index

#declare for collecting data from webpages
text_data = []

#is backslash present at last
backslash_present_last = False

#create a list to save other urls in one webpage
link_list = []

#define parser class and inherit HTMLParser class
class Parser(HTMLParser):

	def handle_starttag(self, tag, attr):
		pass

	def handel_data(self, data):
		text_data.append(data)

#perform backward indexing
def backward_indexing(name, list_of_words):
    #bi = Backward_Index()
    #bi.back_indexing(name, list_of_words)
	for words in list_of_words:
		if Backward_Index.objects.filter(data=words).exists():
			indexes = Backward_Index.objects.filter(data=words)
			for index in indexes:
				if name in index.urls:
					continue
				else:
					index.urls = index.urls + ',' + name
					index.save()

		else:
			Backward_Index.objects.create(data=words, urls=name)

#perform forward indexing
def forward_indexing(name, list_of_words):
    fi = Forward_Index()
    fi.for_indexing(name,list_of_words)
    backward_indexing(name, fi.forward_indexing_dict['data'][name])

#create object of Parser class
parser = Parser()

#function for extracting data from web pages
def extract_data(name, url):
    source = requests.get(name).text
    soup = BeautifulSoup(source, 'lxml')
    parser.handel_data(soup.text)
    data_in_webpage = re.split('\n+', text_data[0])
    list_of_words = []

    #extract the words from the sentence
    for data in data_in_webpage:
        if re.search('\s+',data) is not None:
            store = re.split('\s+', data)
            for s in store:
                if s == '':
                    pass
                else:
                    list_of_words.append(s)

        else:
            if data == '':
                pass
            else:
                list_of_words.append(data)

        forward_indexing(name, list_of_words)

#following the links
def follow_links(name, soup):
    split_name = name.split('/')
    backslash_present_last = False
    if split_name[-1] == '':
        backslash_present_last = True
    for l in soup.find_all('a'):
        other_links = l['href']
        try:
            if re.match(('/'), other_links) is not None:
                if backslash_present_last:
                    link_list.append(name+other_links[1:])
                else:
                    link_list.append(name+other_links)

            elif re.match(('\?'), other_links) is not None:
                link_list.append(name+other_links)

            elif re.match(('#'), other_links) is not None:
                continue

            else:
                link_list.append(name+other_links)

        except Exception as e:
            pass

#copy webpages
def copy_webpages(directory, root_url):
    for l in link_list:
        source = requests.get(l).text
        soup = BeautifulSoup(source, 'lxml')
        extract_data(l, soup)
        name = ''

        try:
            if soup.title.text is not None:
                my_file = Path('D:/googlesearch/media/{0}/{1}.html'.format(directory, soup.title.text))
                if my_file.is_file() == True:
                    if soup.legend is not None:
                        name = soup.legend.text
                    elif soup.find('a', class_='article-title') is not None:
                        name = soup.find('a', class_='article-title').text
                    elif soup.h1 is not None:
                        name = soup.h1.text
                    elif soup.h2 is not None:
                        name = soup.h2.text
                    elif soup.h3 is not None:
                        name = soup.h3.text
                    elif soup.h4 is not None:
                        name = soup.h4.text
                    elif soup.h5 is not None:
                        name = soup.h5.text
                    elif soup.h6 is not None:
                        name = soup.h6.text

                else:
                    name = soup.title.text

            elif soup.find('a', class_='article-title') is not None:
                name = soup.find('a', class_='article-title').text
            elif soup.h1 is not None:
                name = soup.h1.text
            elif soup.h2 is not None:
                name = soup.h2.text
            elif soup.h3 is not None:
                name = soup.h3.text
            elif soup.h4 is not None:
                name = soup.h4.text
            elif soup.h5 is not None:
                name = soup.h5.text
            else:
                if soup.h6 is not None:
                    name = soup.h6.text

        except Exception as e:
            print('exception is: ', e)
            continue

        with open('D:/googlesearch/media/{0}/{1}.html'.format(directory,name),'w') as f:
            f.write(soup.prettify())

        websites = Website.objects.filter(url=root_url)
        for website in websites:
            if WebPage.objects.filter(url=l, visited=True, root=website, location='D:/googlesearch/media/{0}/{1}.html'.format(directory,name)).exists():
                continue
            else:
                WebPage.objects.create(url=l, visited=True, root=website, location='D:/googlesearch/media/{0}/{1}.html'.format(directory,name))

@receiver(post_save, sender=Website)
def save_data(sender, instance, created, **kwargs):
    name = instance.url
    source = requests.get(name).text
    soup = BeautifulSoup(source, 'lxml')
    folder = soup.title.text
    websites = Website.objects.filter(url=name)
    for website in websites:
	    WebPage.objects.create(url=name, visited=True, scrapy=True, root=website, location='D:/googlesearch/media/{0}/{1}.html'.format(folder,folder))
    extract_data(name, soup)
    link_list.append(name)
    directory = soup.title.text

    #call for following links
    follow_links(name, soup)

    #copy webpages of remaining links
    copy_webpages(directory, name)
