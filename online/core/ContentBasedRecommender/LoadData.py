import pandas as pd
import requests
import hashlib
from nltk import word_tokenize
from nltk.corpus import stopwords
import string
import re
from goodreads import client
import numpy as np


def hash_text(text):
    h = hashlib.sha256(text.encode('utf-8'))
    return int(h.hexdigest(), base=16)


def load_books(filename='../../../BX-CSV-Dump/BX-Books.csv', columns=['ISBN','Book-Title','Book-Author','Year-Of-Publication']):
    return pd.read_csv(filename, delimiter=';', encoding='ISO-8859-1', index_col='ISBN',
                        usecols=columns)


def save_processed_dataframe(books, filename='../../data/processed_df.csv'):
    with open(filename, "w") as fp:
        books.to_csv(fp)
    fp.close()


def process_book_name(orig_text):
    """
    Receives a text, which could be a single word or a sentence, and applies the natural language
    process (using NLTK library) in the text, normalizing, tokenizing, removing stopwords and punctuations,
    stemming and ignoring the duplicated tokens.
    :param text: it is a string, which could be a word or a sentence
    :return: a list containing the tokens
    """

    text = orig_text
    if pd.isnull(text) or isinstance(text, bool):
        return text

    # normalize the text
    text = text.lower()

    # substitute a / for a space, in order that they will be split in two tokens
    text = re.sub(r"/", ' ', text)

    # take off strange characters
    text = re.sub(r'[^a-z0-9\s]', '', text)

    # Delete fractions
    fractions = ['̶', '½', '¾', '¼', '⅓', '⅙', '⅛', '⅔', '⅝', '⅜', '—', '–', '‘', '”', '…', '.', '`', '’', '“']
    text = re.sub(('[' + ','.join(map(lambda x: str(x), fractions)) + ']'), '', text)

    # creates the tokens
    text = word_tokenize(text)

    # excludes tokens which contain numbers and punctuations
    text = [t for t in text if bool(re.search(r'\d', t)) == False and t not in string.punctuation]

    # Remove stopwords
    stopset = set(stopwords.words('english'))
    text = [t for t in text if not t in stopset]

    # remove the strange character ' appearing before some words
    text = [re.sub('[\'\"]', '', t) for t in text]

    text = ' '.join(text)

    if text == '':
        return orig_text
    return text


def set_genre_goodreads(books):
    CONSUMER_KEY = 'gsyDVEcZ3ZOFqDvXxrA'
    CONSUMER_SECRET = 'U182SOVsGZRYY7IFJ7jqpltLyXkBvPwp9mUnLsWcek'
    gr = client.GoodreadsClient(CONSUMER_KEY, CONSUMER_SECRET)
    i = 0
    chunk_size = 500

    already_processed = books.dropna(subset=['Hashed-Genre'], how='any')
    to_be_read = set(books.index) - set(already_processed.index)
    for isbn in to_be_read:
        print("Reading book ", i, " of ", len(to_be_read))
        i += 1
        try:
            shelves = gr.book(isbn=isbn).popular_shelves
            shelves = [str(x) for x in shelves]
        except Exception:
            print("Error in ISBN ", isbn)
            continue

        undesired_shelves = set(
            ['to-read', 'own', 'books-i-own', 'currently-reading', 'owned-books', 'default', 're-read',
             'my-books', 'owned', 'favorite', 'favorites', 'wishlist', 'kindle', 'to-buy', 'library',
             'ebook', 'maybe', 'my-book', 'e-book', 'e-books', 'books', 'my-library', 'want-to-read',
             'have', 'own-it', 'own-to-read', 'giller-winners', 'recommended', 'wish-list', 'my-booshelf',
             'short-stories', 'didn-t-finish', 'read-in-2015', 'coming-of-age', 'read-in-2009',
             'read-in-2016', 'gave-up', 'dnf', 'personal-library', 'book-club', 'not-available-on-overdrive',
             'abandoned', 'single-books', 'must-read'])
        for x in set(shelves).intersection(undesired_shelves):
            shelves.remove(x)
        if len(shelves) != 0:
            genre = shelves[0]
            books.set_value(isbn, 'Hashed-Genre', hash_text(genre))
        else:
            books.set_value(isbn, 'Hashed-Genre', 0)

        # save constantly the books dataset
        if i % chunk_size == 0:
            save_processed_dataframe(books, '../../data/processed_df.csv')
    save_processed_dataframe(books)


def search_googlebooks(self, isbn):
    googleapikey = "AIzaSyCk8G1jzmc3ir982I7hqZ-9Y3hYs6u13Wk"
    url = "https://www.googleapis.com/books/v1/volumes?q=isbn="+isbn+"&key="+googleapikey
    try:
        r = requests.get(url=url)
        rj = r.json()
        genre = str(rj["items"][0]["volumeInfo"]["categories"][0]).lower().split()[0]
    except:
        genre = ''
    return genre


def set_genre_googlebooks(books):
    already_processed = books.dropna(subset=['Hashed-Genre'], how='any')
    to_be_read = set(books.index) - set(already_processed.index)
    i = 0
    for isbn in to_be_read:
        print("Reading book ", i, " of ", len(to_be_read))
        i += 1
        genre = search_googlebooks(isbn=isbn)
        if genre != '':
            books.set_value(isbn, 'Hashed-Genre', hash_text(genre))
        else:
            print("Error in ISBN ", isbn)
            books.set_value(isbn, 'Hashed-Genre', 0)

        # request daily limit of Google Books
        if i == 1000:
            break
    save_processed_dataframe(books)


def build_processed_content_based_dataframe():
    books = load_books()
    books['Year-Of-Publication'] = books['Year-Of-Publication'].apply(lambda x: int(x))
    books['Year-Of-Publication'].replace(to_replace=0, value=books['Year-Of-Publication'].mean(), inplace=True)
    books['Year-Of-Publication'] = (books['Year-Of-Publication'] - books['Year-Of-Publication'].mean())/books['Year-Of-Publication'].std()
    books['Book-Title'] = books['Book-Title'].apply(lambda x: process_book_name(x))
    books = books.round(3)
    return books


books = build_processed_content_based_dataframe()
save_processed_dataframe(books)
books = pd.read_csv('../../data/processed_df.csv', delimiter=',', encoding='utf-8', index_col='ISBN')
set_genre_goodreads(books)
books = pd.read_csv('../../data/processed_df.csv', delimiter=',', encoding='utf-8', index_col='ISBN')
set_genre_googlebooks()
