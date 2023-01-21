#!/usr/bin/python

from enum import auto
import arxiv
import argparse
import sqlite3
import os


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


if __name__ == '__main__':
    main()

