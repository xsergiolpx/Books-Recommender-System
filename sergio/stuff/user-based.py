import pandas as pd
from scipy.sparse import coo_matrix
from scipy import io
import numpy as np


def common_books(user1_books, user2_books):
    '''
    Checks the books that two users have in common
    :param user1_books: list of books or dictionary that each key is a book from user 1
    :param user2_books: same for user 2
    :return: a list of the books in common
    '''
    return list(set(user1_books).intersection(set(user2_books)))

def cos_distance(user1_books, user2_books):
    '''
    Returns the cosine distance of two users
    :param user1_books: dictionary of books with ratings of user1, i.e: {"book1": "7", ...}
    :param user2_books: same for user 2
    :return: the cosine distance of the users as a numeric value
    '''
    a = np.sqrt((np.array([user1_books[book] for book in user1_books])**2).sum())
    b = np.sqrt((np.array([user2_books[book] for book in user2_books])**2).sum())
    same_books = common_books(user1_books, user2_books)
    c = np.array([user1_books[book]*user2_books[book] for book in same_books]).sum()
    if a == 0 or b == 0:
        return 0
    else:
        return c/(a*b)

def create_sim_matrix(dict, users):
    # Initialize matrix
    A = coo_matrix(([0], ([0], [0])), shape=(len(users), len(users)))

    # counter
    counter = 0
    for i in range(len(users)):
        print(counter/len(users)*100, "%")
        counter+=1
        user1_books = dict[users[i]]
        for j in range(len(users)):
            user2_books = dict[users[j]]
            if i < j and len(common_books(user1_books, user2_books)) > 0:
                sim_score = cos_distance(user1_books, user2_books)
                A += coo_matrix(([sim_score], ([i], [j])), shape=(len(users), len(users)))
    return A



'''
>>> row = array([0,0,1,2,2,2])
>>> col = array([0,2,2,0,1,2])
>>> data = array([1,2,3,4,5,6])
>>> csr_matrix( (data,(row,col)), shape=(3,3) ).todense()
'''

# Load the dataframe
#df = pd.read_csv("ratings-sample.csv", sep=";", encoding = "ISO-8859-1")
df = pd.read_csv("BX-Book-Ratings.csv", sep=";", encoding = "ISO-8859-1")

#store here the dictionary of the type: {user_1 :{book_A: rating_A}}
dict = {}

# List of users
users = df["User-ID"].unique()

# List of books
books = df["ISBN"].unique()

# create a counter
users_size = len(users)
counter = 0

# create the dicts of dicts
for user in users:
    print(round(counter/users_size*100), "%")
    counter += 1
    books_user = df.loc[df['User-ID'] == user]["ISBN"].values
    ratings_user = df.loc[df['User-ID'] == user]["Book-Rating"].values
    dict[user] = {books_user[i]: ratings_user[i] for i in range(len(books_user))}


m = create_sim_matrix(dict, users)
io.mmwrite("sim_matrix.mtx", m)
del m
'''
newm = io.mmread("test.mtx")
newm           # <3x3 sparse matrix of type '<type 'numpy.int32'>' with 2 stored elements in COOrdinate format>
newm.tocsr()   # <3x3 sparse matrix of type '<type 'numpy.int32'>' with 2 stored elements in Compressed Sparse Row format>
newm.toarray() # array([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=int32)
'''

