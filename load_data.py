import sqlite3

conn = sqlite3.connect('mathdoc.db')
c = conn.cursor()

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
        c.execute("INSERT INTO textbooks (name, author, location) VALUES (?, ?, ?)",
            (titles[i], authors[i], locations[i]))

    conn.commit()

    enter_data()

c.close()
conn.close()
