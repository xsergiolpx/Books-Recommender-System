from online.core.content_based import ContentBased as cb
from online.core.utils.export_import_tools import load_books
import time
import sys
import pandas as pd
import requests
import hashlib
from nltk import word_tokenize
from nltk.corpus import stopwords
import string
import re
from goodreads import client


def test_content_based_similarity(isbn_list):
    books = pd.read_csv('data/content_based/processed_df.csv', delimiter=',', encoding='utf-8', index_col='ISBN')
    book_names = load_books(columns=['ISBN','Book-Title'])

    print("You have seached for:")
    if len(isbn_list) > 1:
        for isbn in isbn_list:
            print(book_names.loc[isbn].loc['Book-Title'])
    else:
        print(book_names.loc[isbn_list[0]].loc['Book-Title'])

    content_based = cb.ContentBased(books=books, query_list_isbn=isbn_list, k=15, sample_size=2000)
    sim_list = content_based.get_similar_books()

    print()
    print("You may also like:")
    for x in sim_list:
        print(x[0], book_names.loc[x[0]]['Book-Title'], '-- Similarity =', round(x[1],ndigits=3))


def main():
    filename = sys.argv[1]
    file = open(filename)
    isbn_list = []
    for isbn in file.readlines():
        isbn_list.append(isbn.strip())
    now = time.time()
    test_content_based_similarity(isbn_list)
    print()
    print("Query processed in ", round(time.time() - now, ndigits=2), " seconds")


if __name__ == '__main__':
    main()

# def process_book_name(orig_text):
#     """
#     Receives a text, which could be a single word or a sentence, and applies the natural language
#     process (using NLTK library) in the text, normalizing, tokenizing, removing stopwords and punctuations,
#     stemming and ignoring the duplicated tokens.
#     :param text: it is a string, which could be a word or a sentence
#     :return: a list containing the tokens
#     """
#
#     text = orig_text
#     if pd.isnull(text) or isinstance(text, bool):
#         return text
#
#     # normalize the text
#     text = text.lower()
#
#     # substitute a / for a space, in order that they will be split in two tokens
#     text = re.sub(r"/", ' ', text)
#
#     # take off strange characters
#     text = re.sub(r'[^a-z0-9\s]', '', text)
#
#     # Delete fractions
#     fractions = ['̶', '½', '¾', '¼', '⅓', '⅙', '⅛', '⅔', '⅝', '⅜', '—', '–', '‘', '”', '…', '.', '`', '’', '“']
#     text = re.sub(('[' + ','.join(map(lambda x: str(x), fractions)) + ']'), '', text)
#
#     # creates the tokens
#     text = word_tokenize(text)
#
#     # excludes tokens which contain numbers and punctuations
#     text = [t for t in text if t not in string.punctuation]
#
#     # Remove stopwords
#     stopset = set(stopwords.words('english'))
#     text = [t for t in text if not t in stopset]
#
#     # remove the strange character ' appearing before some words
#     text = [re.sub('[\'\"]', '', t) for t in text]
#
#     text = ' '.join(text)
#
#     if text == '':
#         return orig_text
#     return text
#
#
# books = load_books()
# processed_books = pd.read_csv('../data/processed_df.csv', delimiter=',', encoding='utf-8', index_col='ISBN')
# processed_books['Book-Title'] = books['Book-Title'].apply(lambda x: process_book_name(x))
# processed_books.to_csv('../data/processed_df.csv')