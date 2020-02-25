import urllib
import feedparser

# Base api query url
base_url = 'http://export.arxiv.org/api/query?';

# Search parameters
search_query = '2002.08328' 
start = 0                     # retreive only the first result
max_results = 1

query = 'id_list=%s&start=%i&max_results=%i' % (search_query, start, max_results)

# Opensearch metadata such as totalResults, startIndex, 
# and itemsPerPage live in the opensearch namespase.
# Some entry metadata lives in the arXiv namespace.
# This is a hack to expose both of these namespaces in
# feedparser v4.1
feedparser._FeedParserMixin.namespaces['http://a9.com/-/spec/opensearch/1.1/'] = 'opensearch'
feedparser._FeedParserMixin.namespaces['http://arxiv.org/schemas/atom'] = 'arxiv'

# perform a GET request using the base_url and query
response = urllib.request.urlopen(base_url+query).read()

# What data do I need?
# 1) An array with author's names

# parse the response using feedparser
feed = feedparser.parse(response)

authorstring = []

for entry in feed.entries:
    #authors = ';'.join(author.name.split(' ')[-1] for author in entry.authors)
    #print(entry.authors)

    title = entry.title
    #print(title)

    for link in entry.links:
        if link.rel == 'alternate':
            pass
        elif link.title == 'pdf':
            pdf_link = link.href
            #print(pdf_link)

    authorstring = ';'.join(author.name for author in entry.authors)

print(title)
print(authorstring)
print(pdf_link)
