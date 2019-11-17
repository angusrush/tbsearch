import xml.etree.ElementTree as ET
from urllib.request import urlopen

url = 'http://export.arxiv.org/api/query?search_query=all:electron&start=0&max_results=1'

tree = ET.parse('query.xml')

#data = urlopen(url).read()
#root = ET.fromstring(data)

root = tree.getroot()

