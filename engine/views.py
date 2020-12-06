from django.shortcuts import render
from search.models import Backward_Index
import re
from search.models import WebPage
import networkx as nx
import requests
from bs4 import BeautifulSoup

#make a class to store final dictionary
class FinalDict():
    final_dict = {}

    def save(self, key, value, title):
        self.final_dict[key] = {title: value}

# Create your views here.
def query(request):
    input = request.GET.get('input')
    inputs = re.split('\s', str(input))
    if input == None:
        return render(request, 'engine/query.html')
    else:
        l = []
        indexes = Backward_Index.objects.all()
        for input in inputs:
            for index in indexes:
                if re.search(input, index.data) is not None:
                    l.append(index.urls)
        final_list = []
        for item in l:
            urls = item.split(',')
            for url in urls:
                if url in final_list:
                    continue
                else:
                    final_list.append(url)

        #make a graph using networkx
        G = nx.DiGraph()

        for input in inputs:
            for url in final_list:
                webpage = WebPage.objects.filter(url=url)
                for page in webpage:
                    filename =  page.location
                    with open(filename, 'r') as f:
                        se = re.search(input, f.read())
                        G.add_node(url, location=filename, points=1)

        #adding edges between nodes
        for node in G.nodes():
            source = requests.get(node).text
            soup = BeautifulSoup(source, 'lxml')
            for l in soup.find_all('a'):
                other_links = l['href']
                links = ''
                webpages = WebPage.objects.filter(url=node)
                for webpage in webpages:
                    backslash_present_last = False
                    check = str(webpage.root)
                    splits = check.split('/')
                    if splits[-1] == '':
                        backslash_present_last = True
                    try:
                        if re.match(('/'), other_links) is not None:
                            if backslash_present_last:
                                links = str(webpage.root) + (other_links[1:])
                            else:
                                links = str(webpage.root) + other_links

                        elif re.match(('\?'), other_links) is not None:
                            links = str(webpage.root) + other_links

                        elif re.match(('#'), other_links) is not None:
                            continue

                        else:
                            links = str(webpage.root) + other_links

                    except Exception as e:
                        print(e)
                        pass

                if links in G.nodes():
                    G.add_edge(node, links)

        #implement page rank algorithm using point distribution
        for i in range(100):
            for edge in G.edges():
                G.nodes[edge[1]]['points'] += 1

        #sort the nodes according to its points
        di = {}
        for node in G.nodes():
            di[node] = G.nodes[node]['points']

        #sort the dictionary
        sorted_dict = {k:v for k,v in sorted(di.items(), key=lambda item: item[1], reverse=True)}

        for k,v in sorted_dict.items():
            webpages = WebPage.objects.filter(url=k)
            keyword_found_in_all = False
            for webpage in webpages:
                filename = webpage.location
                for input in inputs:
                    with open(filename, 'r') as f:
                        se = re.search(input, f.read())
                        if se is not None:
                            keyword_found_in_all = True
                        else:
                            keyword_found_in_all = False

            if keyword_found_in_all == True:
                G.nodes[k]['points'] += 10000

        #sort the nodes according to its points
        di = {}
        for node in G.nodes():
            di[node] = G.nodes[node]['points']

        #sort the dictionary
        sorted_dict = {k:v for k,v in sorted(di.items(), key=lambda item: item[1], reverse=True)}

        f1 = FinalDict()

        for key in sorted_dict.keys():
            source = requests.get(key).text
            soup = BeautifulSoup(source, 'lxml')
            title = soup.title.text
            f1.save(key, soup.text, title)
        return render(request, 'engine/result.html', {'dictionary':f1.final_dict})
