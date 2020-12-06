from django.shortcuts import render
from .models import Website
from crawler.crawler.spiders.crawling import WebsiteScrawler
import requests
from bs4 import BeautifulSoup
import os

def register(request):
    if request.method == 'POST':
        name = request.POST.get('website_name')
        source = requests.get(name).text
        soup = BeautifulSoup(source, 'lxml')
        directory = '{0}'.format(soup.title.text)
        parent = 'D:/googlesearch/media/'
        path = os.path.join(parent,directory)
        os.mkdir(path)
        filename = 'D:/googlesearch/media/{0}/{1}.html'.format(soup.title.text, soup.title.text)
        with open(filename, 'w') as f:
            f.write(soup.prettify())
        w1 = Website.objects.create(url=name)
        #ws = WebsiteScrawler()
        #ws.start_urls.append(name)
        #ws.start_requests()
        #res = requests.get(name)

        #txtres = scrapy.http.TextResponse(w1.url)
        #print(req)
        #ws.__init__(w1.url)
        #ws.parse(res)
        #cap = subprocess.run('scrapy crawl domains', shell=True, capture_output=True)
    return render(request, 'search/register.html')
