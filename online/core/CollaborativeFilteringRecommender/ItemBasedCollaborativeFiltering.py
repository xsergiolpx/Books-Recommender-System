import pandas as pd
import numpy as np
from scipy.sparse import coo_matrix
from sklearn.metrics.pairwise import cosine_similarity
import online.core.CollaborativeFilteringRecommender.DictionaryController as dc
from scipy import io


def item_based_similarity(isbn, isbn_dict, users_dict, type='cosine'):
    book1 = isbn_dict[isbn]
    isbn_inters = set()
    users = list(isbn_dict[isbn].keys())
    for u in users:
        isbn_inters |= set(users_dict[u])
    l = []
    for k in isbn_inters:
        book2 = isbn_dict[k]
        if type == "cosine":
            similarity = cosine_similarity(book1, book2)
        l.append((k, similarity))
    return l


def cosine_similarity(book1, book2):
    similarity = 0
    users_inters = set(book1.keys()) & set(book2.keys())
    if len(users_inters) != 0:
        dot = sum(float(book1[key]) * float(book2[key]) for key in users_inters)
        norm1 = np.linalg.norm(np.array(list(book1.values())))
        norm2 = np.linalg.norm(np.array(list(book2.values())))
        similarity = dot/(norm1*norm2)
        if np.isnan(similarity):
            similarity = 0
    return similarity


def sergios_cosine_similarity():
    isbn_dict = dc.load_dict_json('../../data/isbn_dict.json')
    df = pd.read_csv("../../../BX-CSV-Dump/BX-Book-Ratings.csv", sep=";", encoding="ISO-8859-1")

    # List of users
    users = df["User-ID"].unique()

    # Asign each user a index for the utility matrix
    users_to_index = {users[i]: i for i in range(0, len(users))}

    # List of books
    books = df["ISBN"].unique()

    # Asign each book an index for the utility matrix
    index_to_books = {i: books[i] for i in range(0, len(books))}

    # create sparse utility matrix (users in rows, books in columns)
    # inizialize
    A = coo_matrix(([0], ([0], [0])), shape=(len(books), len(users)))

    # create the utility matrix
    j = 0
    for i in range(len(books)):
        print("reading ",j," from ",len(books))
        j+=1
        # create list of scores like [5, 3, 9]
        scores_list = list(isbn_dict[index_to_books[i]].values())

        # create list of books using the indices like [234, 4532, 3453]
        users_j = []
        isbn = index_to_books[i]
        for user in list(isbn_dict[isbn].keys()):
            users_j.append(users_to_index[int(user)])

        # all the books in one iteration are from the same user like [3,3,3]
        books_i = np.repeat(i, len(users_j))

        # place them in the matrix
        A += coo_matrix((np.array(scores_list).astype(np.int), (books_i, users_j)), shape=(len(books), len(users)))


    print(cosine_similarity(A, dense_output=False))
    io.mmwrite("cosine_sim.mtx", A)


sergios_cosine_similarity()