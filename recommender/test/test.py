from online.core.utils.export_import_tools import file_to_list
from online.scripts.item_based_similarity_matrix import item_based
from online.scripts.user_based_similarity_matrix import user_based
from online.scripts.cross_validation_item_based import cv_item_based
from online.scripts.cross_validation_user_based import cv_user_based
import sys

# load books to list
# TODO: add args
filename = sys.argv[1]
books = file_to_list(filename)

print("To analyze: ", books)

# item based
item_based(books)

print("\nPress enter to continue\n")
input()

# cross validation
cv_item_based(books)
print("\nPress enter to continue\n")
input()

#user based
user_based(books)

print("\nPress enter to continue\n")
input()

# cross validation
cv_user_based(books)
