# googlesearch - Search Engine
search engine where anyone can register website and this engine do crawling and index web pages developed using django.

Most of search engine have to perform following tasks:

<ul>
  <li>Crawling</li>
  <li>Scraping or Extracting Data</li>
  <li>Indexing</li>
  <li>PageRank</li>
</ul>

<h2>Crawling</h2>

There are many packages in python for crawling like BeautifulSoup, scrapy etc. Here we use BeautifulSoup to crawl a website.

<h4>Installing BeautifulSoup</h4>

<pre>
  pip install beautifulsoup4
</pre>

<h2>Crawling a website</h2>

For crawling a website you need a url of a website and then you have to generate request for that website.

<b>Generate a request</b>

first install requests library to generate request

<pre>
  pip install requests
</pre>

generate request and crawl a webpage

<pre>
  source = requests.get('enter your url here').text
  soup = BeautifulSoup(source, 'lxml')
</pre>

<h2>Scraping or extracting a data</h2>

Whenever crawling performs it stores a copy of a webpage and in database store the url of copied webpage and title of webpage and many more information. Below is the example of extracting data:-

<pre>
  title = soup.title.text
  h2 = soup.find('h2')
  #finding link
  link = soup.find('a')
  #finding href attribute from link
  href = link['href']
</pre>

<h2>Indexing</h2>

Indexing means store each and every word with it's url you can think as a dictionary where word is the key and value is url and this is called backward indexing if you want to know more about backward indexing and other search engine indexing <a href="https://en.wikipedia.org/wiki/Search_engine_indexing">follow</a>

Below is the database for backward indexing

<pre>
  class Backward_Index(models.Model):
      data = models.CharField(max_length=100)
      urls = models.TextField()

      def __str__(self):
          return self.data
</pre>

Code to performing backward indexing

<pre>
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
</pre>

<h2>PageRank Algorithm</h2>

Page rank algorithm is the heart of the every search engine to get best search results. There are many page ranking algorithm exists, here point distribution algorithm implemented.

To perform this algorithm you have to make graph of every url where search keyword exists and then distribute point. Making a graph using <b>networkx</b> library.

<b>Install networkx</b>

<pre>
  pip install networkx
</pre>

