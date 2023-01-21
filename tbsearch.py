#! /usr/bin/python

import argparse as ap
import mathdb


def main():
    parser = ap.ArgumentParser(description="Search textbook database")

    parser.add_argument(
            '--add-from-arxiv',
            action='store_true',
            help="Query arxiv directly")

    parser.add_argument(
            '-a',
            dest='author',
            type=str,
            help="Author")

    parser.add_argument(
            '-t',
            dest='title_keyword',
            type=str,
            help="Title")

    parser.add_argument(
            'query',
            nargs='?',
            default='')

    parser.add_argument(
            '--id',
            dest='id',
            nargs='?',
            default='')


    args = parser.parse_args()

    if args.add_from_arxiv:
        mathdb.get_from_arxiv(args.query, args.id)
    else:
        mathdb.read_from_db(args.query, args.author)


main()


