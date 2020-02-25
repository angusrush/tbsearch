import sqlite3
import os
import urllib
import feedparser
import re
import requests


def enter_tb(title, author, location):
    conn = sqlite3.connect('/home/angus/programming/tbsearch/mathdoc.db')
    c = conn.cursor()

    c.execute("INSERT INTO textbooks (title, author, location) VALUES (?, ?, ?)",
            (title, author, location))
    conn.commit()

    c.close()
    conn.close()


def auto_enter(title, author, location):

    filename = author.split(' ')[-1] + '_' + title.replace(',', '').replace(' ', '_') + '.pdf'
    newpath = '/home/angus/Textbooks/math/' + filename
    #print("Path: " + newpath)
    os.rename(os.path.abspath(location), newpath)
    enter_tb(title, author, newpath)
    return newpath

# This doesn't work and I'm not sure why.
def rename_author(oldname, newname):
    c.execute("UPDATE textbooks SET author = replace(author, ?, ?)",
            (oldname, newname))

    #c.execute("UPDATE textbooks SET author = replace(author, \"" + oldname + "\", \"" + newname +"\")")
    conn.commit()

#def enter_data():
#    fo = open("authors")
#    lines = []
#    authors = []
#    titles = []
#    locations = []
#    for line in fo:
#        lines.append(line.rstrip())
#
#    for i in range(len(lines)):
#        if i%3 == 0:
#            authors.append(lines[i])
#        if i%3 == 1:
#            titles.append(lines[i])
#        if i%3 == 2:
#            locations.append(lines[i])
#
#    for i in range(len(authors)):
#        c.execute("INSERT INTO textbooks (title, author, location) VALUES (?, ?, ?)",
#            (titles[i], authors[i], locations[i]))
#
#    conn.commit()

def enter_from_arxiv(id):
    # Base api query url
    base_url = 'http://export.arxiv.org/api/query?';
    
    # Search parameters
    search_query = id
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
                pdf_link = link.href + '.pdf'
                #print(pdf_link)
    
        authorstring = ';'.join(author.name for author in entry.authors)
    
    print("Adding paper:")
    print(title)
    print("with author(s):")
    print(authorstring)
    answer = input("Is this correct? [y/n]")
    if answer == 'y':
        savefile = '/home/angus/Downloads/' + id + '.pdf'
        print('Downloading to ' + savefile)
        file_name, headers = urllib.request.urlretrieve(pdf_link, savefile)
        print('Downloaded. Moving to')
        fileloc = auto_enter(title, authorstring, file_name)
        print(fileloc)




def main():

    #enter_from_arxiv('0708.2832')
    #auto_enter("Model Categories and Their Localizations", "Philip Hirschhorn", "/home/angus/Downloads/hirschhornloc.pdf")

main()
