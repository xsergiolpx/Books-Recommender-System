import pandas as pd
import numpy as np
from scipy.sparse import coo_matrix
from sklearn.metrics.pairwise import cosine_similarity
import online.core.CollaborativeFilteringRecommender.DictionaryController as dc
from scipy import io


def item_based_similarity(isbn, isbn_dict, users_dict, type='cosine'):
    book1 = isbn_dict[isbn]
    isbn_union = set()
    users = list(isbn_dict[isbn].keys())
    for u in users:
        isbn_union |= set(users_dict[u])
    l = []
    for k in isbn_union:
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