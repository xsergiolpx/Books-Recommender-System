import numpy as np
import ast
from math import log,sqrt
from textblob import TextBlob as tb
import pandas as pd
from collections import Counter


def scalar(collection):
  total = 0
  for count in collection.values():
    total += count * count
  return sqrt(total)


def similarity(text_1,text_2):
    A = dict(Counter(text_1.split()))
    B = dict(Counter(text_2.split()))
    total = 0
    for word in A:
        if word in B:
            total += A[word] * B[word]
    if total != 0:
        return float(total) / (scalar(A)*scalar(B))
    else:
        return 0


def item_based_similarity(query_isbn, books):
    book1 = books.loc[query_isbn]
    all_isbn = books.index
    sim_list = []
    i = 0
    for isbn in all_isbn:
        print("Reading ",i," of ",len(all_isbn))
        i+=1
        book2 = books.loc[isbn]

        title_1 = book1['Book-Title']
        title_2 = book2['Book-Title']
        title_sim = similarity(title_1, title_2)

        shelves_sim = 0
        if book1.loc['Popular-Shelves'] == book2.loc['Popular-Shelves']:
            shelves_sim = 1

        author_sim = 0
        if book1.loc['Book-Author'] == book2.loc['Book-Author']:
            author_sim = 1

        year_sim = 0
        if book1.loc['Year-Of-Publication'] == book2.loc['Year-Of-Publication']:
            year_sim = 1

        total_sim = (2*title_sim + 4*author_sim + year_sim + 4*shelves_sim)/9

        sim_list.append((isbn,total_sim))
    return sim_list


books = pd.read_csv('../../data/processed_df (5th copy).csv', delimiter=';', encoding='utf-8', index_col='ISBN')
sim_list = item_based_similarity('0375823468',books)
sim_list.sort(key=lambda tup: tup[1], reverse=True)
print(sim_list[0:12])