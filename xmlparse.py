import xml.etree.ElementTree as ET
from urllib.request import urlopen
import feedparser

url = 'http://export.arxiv.org/api/query?search_query=all:1212.3563&start=0&max_results=1'

tree = ET.parse('hssquery.xml')
root = tree.getroot()

#data = urlopen(url).read()
#tree = ET.fromstring(data)

for author in root.findall('name'): 
    print(author.text)



