from math import log,sqrt
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


def get_k_similar(query_isbn, books, k=5, sample_size=2000):
    book1 = books.loc[query_isbn]
    books = books.drop(query_isbn)
    all_isbn = books.loc[books['Hashed-Genre'] == book1['Hashed-Genre']]
    if len(all_isbn) >= sample_size:
        all_isbn = all_isbn.sample(sample_size)
    sim_list = []
    for isbn in all_isbn.index:
        book2 = all_isbn.loc[isbn]

        title_1 = book1['Book-Title']
        title_2 = book2['Book-Title']
        title_sim = similarity(title_1, title_2)

        author_sim = 0
        if book1.loc['Book-Author'] == book2.loc['Book-Author']:
            author_sim = 1

        year_sim = 0
        if book1.loc['Year-Of-Publication'] == book2.loc['Year-Of-Publication']:
            year_sim = 1

        total_sim = (title_sim + 8*author_sim + 2*year_sim)/11

        sim_list.append((isbn,total_sim))
    sim_list.sort(key=lambda tup: tup[1], reverse=True)
    return sim_list[:k]


def content_based_similarity(list_isbn, books):
    k_similars = []
    k = 5
    for isbn in list_isbn:
        k_similars = k_similars + get_k_similar(isbn, books, k=k, sample_size=1000)
    k_similars.sort(key=lambda tup: tup[1], reverse=True)
    return k_similars[:k]