from online.core.ContentBasedRecommender import ContentBased as cb
import pandas as pd
import time
import sys


def load_books(filename='../../BX-CSV-Dump/BX-Books.csv', columns=['ISBN','Book-Title','Book-Author','Year-Of-Publication']):
    return pd.read_csv(filename, delimiter=';', encoding='ISO-8859-1', index_col='ISBN',
                        usecols=columns)


def test_content_based_similarity(isbn_list):
    books = pd.read_csv('../data/processed_df.csv', delimiter=',', encoding='utf-8', index_col='ISBN')
    book_names = load_books(columns=['ISBN','Book-Title'])

    print("You have seached for:")
    if len(isbn_list) > 1:
        for isbn in isbn_list:
            print(book_names.loc[isbn].loc['Book-Title'])
    else:
        print(book_names.loc[isbn_list[0]].loc['Book-Title'])

    sim_list = cb.content_based_similarity(isbn_list, books)

    print('\n')
    print("You may also like:")
    for x in sim_list:
        print(book_names.loc[x[0]]['Book-Title'], '-- Similarity =', round(x[1],ndigits=3))


def main():
    filename = sys.argv[1]
    file = open(filename)
    isbn_list = []
    for isbn in file.readlines():
        isbn_list.append(isbn.strip())
    now = time.time()
    test_content_based_similarity(isbn_list)
    print(round(time.time() - now, ndigits=2))


if __name__ == '__main__':
    main()