from export_import_tools import file_to_list
from item_based_similarity_matrix import item_based
from user_based_similarity_matrix import user_based
from cross_validation_item_based import cv_item_based
from cross_validation_user_based import cv_user_based

# load books to list
books = file_to_list("isbns.txt")

# item based
#item_based(books)

#print("\nPress enter to continue\n")
#input()

# cross validation
cv_user_based(books)
exit()
print("\nPress enter to continue\n")
input()

#user based
user_based(books)

