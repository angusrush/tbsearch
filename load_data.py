import sqlite3
import os

def enter_tb(title, author, location):
    c.execute("INSERT INTO textbooks (title, author, location) VALUES (?, ?, ?)",
            (title, author, location))
    conn.commit()

def auto_enter(title, author, location):
    filename = author.split(' ')[-1] + '_' + title.replace(' ', '_') + '.pdf'
    newpath = '/home/angus/Textbooks/math/' + filename
    #print("Path: " + newpath)
    os.rename(os.path.abspath(location), newpath)
    enter_tb(title, author, newpath)
    


# This doesn't work and I'm not sure why.
def rename_author(oldname, newname):
    c.execute("UPDATE textbooks SET author = replace(author, ?, ?)",
            (oldname, newname))

    #c.execute("UPDATE textbooks SET author = replace(author, \"" + oldname + "\", \"" + newname +"\")")
    conn.commit()

def enter_data():
    fo = open("authors")
    lines = []
    authors = []
    titles = []
    locations = []
    for line in fo:
        lines.append(line.rstrip())

    for i in range(len(lines)):
        if i%3 == 0:
            authors.append(lines[i])
        if i%3 == 1:
            titles.append(lines[i])
        if i%3 == 2:
            locations.append(lines[i])

    for i in range(len(authors)):
        c.execute("INSERT INTO textbooks (title, author, location) VALUES (?, ?, ?)",
            (titles[i], authors[i], locations[i]))

    conn.commit()


conn = sqlite3.connect('mathdoc.db')
c = conn.cursor()

#auto_enter("A Short Course on Infinity-categories", "Moritz Groth", "/home/angus/Short.pdf")

c.close()
conn.close()
