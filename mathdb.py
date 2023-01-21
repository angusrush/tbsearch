import os
import sqlite3
import arxiv
import argparse

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
    newpath = '/home/angus/Textbooks/arxiv/' + filename
    os.rename(os.path.abspath(location), newpath)
    enter_tb(title, author, newpath)
    return newpath

def rename_author(oldname, newname, connection, cursor):
    cursor.execute("UPDATE textbooks SET author = replace(author, ?, ?)",
            (oldname, newname))

    #c.execute("UPDATE textbooks SET author = replace(author, \"" + oldname + "\", \"" + newname +"\")")
    connection.commit()

def read_from_db(query, author):
    search_stem = "SELECT title, author, location FROM textbooks WHERE "
    conn = sqlite3.connect('/home/angus/programming/tbsearch/mathdoc.db')
    c = conn.cursor()

    search_string = None
    
    if query and author:
        search_string = search_stem + "author LIKE '%" + author + "%' AND title LIKE '%" + query + "%'"
    elif author:
        search_string = search_stem + "author LIKE '%" + author + "%'"
    else:
        search_string = search_stem + "title LIKE '%" + query + "%'"
    if search_string:
        c.execute(search_string)
    for row in c.fetchall():
        print(row[0])
        print(row[1])
        print(row[2])
        print("")

    c.close()
    conn.close()
        
def get_from_arxiv(query, arxiv_id):

    #Perform a search of the query passed as an argument to the program
    search = arxiv.Search(
        query = query,
        id_list = [arxiv_id],
        max_results=5,
        sort_by=arxiv.SortCriterion.Relevance,
    )

    results = list(search.results())
    for i, result in enumerate(results):
        print(
            f"[{i+1}] {result.title}\n"
            f"    {', '.join([author.name for author in result.authors])} to {', '.join(result.categories)}\n"
            f"    Uploaded {str(result.published).split()[0]}\n"
        )

    n = int(input("Enter a number 1-5 to download the corresponding article: "))

    article = results[n - 1]
    title = article.title
    authors = ', '.join([author.name for author in article.authors])
    categories = ', '.join(article.categories)

    print(f"\n"
          f"  {title}\n"
          f"  {authors} to {categories}\n"
          f"\n"
          f"  {article.summary}\n"
    )

    if not input("Would you like to download this article? [Y/n]") == 'n':
        downloadname = article.get_short_id() + 'test' + '.pdf'
        authorstring = ';'.join([author.name for author in article.authors])

        print("Downloading...")
        download_loc = article.download_pdf(dirpath="/home/angus/Downloads", filename=downloadname)
        final_loc = auto_enter(title, authorstring, download_loc)
        print(f"Downloaded to {final_loc}. Exiting.")
    else:
        print("You selected no. Aborting.")
        raise SystemExit
