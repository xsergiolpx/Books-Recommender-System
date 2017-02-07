import pandas as pd
import re
import hashlib
import numpy as np


def hash_text(author):
    h = hashlib.sha256(author.encode('utf-8'))
    return int(h.hexdigest(), base=16)


def clean_shelves1():
    books = pd.read_csv('../../data/processed_df.csv', delimiter=';', index_col='ISBN') #encoding='ISO-8859-1'
    already_processed = books.dropna(subset=["Popular-Shelves"], how="any")
    i = 0
    for isbn in already_processed.index:
        print("Correct book ", i, " (", isbn ,") of ", len(already_processed.index))
        shelves = books.loc[isbn]['Popular-Shelves']
        shelves = re.sub('[\'\"\[\]]', '', shelves)
        shelves = shelves.split()

        undesired_shelves = set(['to-read', 'own', 'books-i-own', 'currently-reading', 'owned-books', 'default', 're-read',
                                 'my-books', 'owned', 'favorite', 'favorites', 'wishlist', 'kindle', 'to-buy', 'library',
                                 'ebook','maybe', 'my-book', 'e-book','e-books','books','my-library','want-to-read',
                                 'have','own-it','own-to-read','giller-winners','recommended','wish-list','my-booshelf',
                                 'short-stories','didn-t-finish','read-in-2015','coming-of-age','read-in-2009',
                                 'read-in-2016','gave-up','dnf','personal-library','book-club','not-available-on-overdrive',
                                 'abandoned','single-books','must-read'])
        inters = set(shelves).intersection(undesired_shelves)
        for x in inters:
            shelves.remove(x)
        if len(shelves) != 0:
            shelves = shelves[0]
            books.set_value(isbn, 'Popular-Shelves', hash_text(shelves))
        else:
            books.set_value(isbn, 'Popular-Shelves', 0)
        i += 1

    books['Popular-Shelves'] = (books['Popular-Shelves'] - books['Popular-Shelves'].mean()) / books['Popular-Shelves'].std()
    books['Popular-Shelves'] = np.around(books['Popular-Shelves'].astype(np.float),3)
    books['Book-Author'] = np.around(books['Book-Author'].astype(np.float),3)
    books['Year-Of-Publication'] = np.around(books['Year-Of-Publication'].astype(np.float),3)
    books = books.round(3)
    books.to_csv('../../data/processed_shelves.csv')


def clean_shelves2():
    books = pd.read_csv('../../data/processed_df.csv', delimiter=';', index_col='ISBN')  # encoding='ISO-8859-1'
    books[books['Popular-Shelves'] < 100] = np.nan
    books.to_csv('../../data/processed_shelves2.csv')

clean_shelves2()