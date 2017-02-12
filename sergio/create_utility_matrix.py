# here we just create the utility matrix
# and export it

import pandas as pd
from scipy.sparse import coo_matrix
from export_import_tools import *
import numpy as np

# Load the dataframe
df = pd.read_csv("BX-Book-Ratings.csv", sep=";", encoding = "ISO-8859-1")

# Drop reviews that are zero
#df= df[df["Book-Rating"] != 0]
# Drop users with only one review
#df = df.groupby('User-ID').filter(lambda x: len(x) > 1)

# List of users
users = df["User-ID"].unique()

# Asign each user a index for the utility matrix
users_to_index = {users[i]: i for i in range(0,len(users))}
index_to_users = {i: users[i] for i in range(0,len(users))}

# List of books
books = df["ISBN"].unique()

# Asign each book an index for the utility matrix
books_to_index = {str(books[i]): i for i in range(0,len(books))}
index_to_books = {i: str(books[i]) for i in range(0,len(books))}

# create dictionary of the type
# {user1: {book1: rating1, book2: rating2}, user2: {book1: rating1}}
dic = {}
# create a counter
users_size = len(users)
counter = 0
for user in users:
    # nice counter
    print(round(counter/users_size*100), "%")
    counter += 1

    # Find all the read books by the user and its ratings
    user_df = df.loc[df['User-ID'] == user]
    books_user = user_df["ISBN"].values
    ratings_user = user_df["Book-Rating"].values
    # replace the scores 0 by 0.01
    ratings_user = [ 0.01 if (x == 0) else x for x in ratings_user]
    # pute them in the dic
    dic[user] = {books_user[i]: ratings_user[i] for i in range(len(books_user))}

# create sparse utility matrix (users in rows, books in columns)
#inizialize it
A = coo_matrix(([0], ([0], [0])), shape=(len(users), len(books)))

counter = 0
# create the utility matrix
for i in range(len(users)):
    # nice counter
    print(round(counter / users_size * 100), "%")
    counter += 1
    # create list of scores
    scores_list = list(dic[index_to_users[i]].values())

    # create list of books using the indices
    books_j = [books_to_index[book] for book in list(dic[index_to_users[i]].keys())]

    # all the books in one iteration are from the same user
    users_i = np.repeat(i, len(books_j))

    # place them in the matrix
    A += coo_matrix((scores_list, (users_i, books_j)), shape=(len(users), len(books)))

# Export the data
export_matrix(A, "utility_matrix")
export_dic(users_to_index, "users_to_index")
export_dic(index_to_users, "index_to_users")
export_dic(books_to_index, "books_to_index")
export_dic(index_to_books, "index_to_books")
export_dic(dic, "dic_users_and_books")

print("Done")