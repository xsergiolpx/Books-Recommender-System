from recommender.core.utils.export_import_tools import file_to_list
from recommender.scripts.item_based_similarity_matrix import item_based
from recommender.scripts.user_based_similarity_matrix import user_based
from recommender.scripts.cross_validation_item_based import cv_item_based
from recommender.scripts.cross_validation_user_based import cv_user_based
from recommender.core.association_rules.arules_utils import read_rules, find_matches
from recommender.core.utils.export_import_tools import import_dic, download_name
from recommender.core.content_based import ContentBased as cb
from recommender.core.utils.export_import_tools import load_books
import time
import sys
import pandas as pd

import sys

# load books to list

def test_content_based_similarity(isbn_list):
    books = pd.read_csv('data/content_based/processed_df.csv', delimiter=',', encoding='utf-8', index_col='ISBN')
    book_names = load_books(columns=['ISBN','Book-Title'])

    content_based = cb.ContentBased(books=books, query_list_isbn=isbn_list, k=15, sample_size=2000)
    sim_list = content_based.get_similar_books()

    print()
    print("You may also like:")
    for x in sim_list:
        print(x[0], book_names.loc[x[0]]['Book-Title'], '-- Similarity =', round(x[1],ndigits=3))


# TODO: add args
filename = sys.argv[1]
books = file_to_list(filename)

books_dict = import_dic("data/association_rules/isbn_to_books")

print("--- You like: ")

for x in books:
    try:
        print(x, books_dict[x])
    except KeyError:
        print("Using download ", x, download_name(x))

# Recommendation rules

rules = read_rules("data/association_rules/rules_0.00012.csv")

results = find_matches(rules, ','.join(books), query_type="ain")

for result in results:
    if result[5] == "in":
        print("[in] Book %s is recommended by: %s with support %0.2f confidence %0.2f and lift %0.2f" % (result[1],
                                                                                                    result[6],
                                                                                                    result[2],
                                                                                                    result[3],
                                                                                                    result[4]))
    else:
        print("[ain] Book %s is recommended by: %s with support %0.2f confidence %0.2f and lift %0.2f" % (result[1],
                                                                                                    result[6],
                                                                                                    result[2],
                                                                                                    result[3],
                                                                                                    result[4]))

# Content Based
print()
print("[Content Based]")
now = time.time()
test_content_based_similarity(books)
print()
print("Query processed in ", round(time.time() - now, ndigits=2), " seconds")

# item based
item_based(books)

# cross validation
cv_item_based(books)

#user based
user_based(books)

# cross validation
cv_user_based(books)

