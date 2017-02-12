from export_import_tools import *
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix, find
import numpy as np


def books_common(user_idx, books_idx, A):
    '''
    :param user_idx: 894357943
    :param books_idx: [34534, 345234, 43, 2]
    :param A: sparse matrix
    :return: books that user has read from the books_idx list and their ratings in a dict like
        {"324523": 9, "2342", 4}
    '''
    books_local_index, _, rat = find(A[books_idx, user_idx])
    return {books_idx[books_local_index[j]]: rat[j] for j in range(len(books_local_index))}


# Load isbn to book title:
isbn_to_book = import_dic("isbn_to_books")

# load the utility sparse matrix
A = import_matrix("utility_matrix_prepared_item_based")
total_users = A.shape[1]
total_books = A.shape[0]

#Harry Potter books
books = ["0439136369","0439567610", "0747545111", "0613496744", "0312282540"]

#Load the list of books
books_to_index = import_dic("books_to_index")
index_to_books = import_dic("index_to_books")

# Change them to indices
books_j = []
for book in books:
    try:
        books_j.append(books_to_index[book])
    except KeyError:
        print(book, "not found in database")

# store the book index and score in a dic
book_and_scores = {}
#run over all the books
for book in books_j:
    # take the vector of the book, each component is a rating from a user
    book_vector = A[book,:]
    _, users_idx, ratings = find(book_vector)
    user_rating_real = {}
    # create a dict of real ratings for the book
    for k in range(len(users_idx)):
        user_rating_real[users_idx[k]] = ratings[k]

    # calculate the similarity of books
    similarity = cosine_similarity(A,book_vector, dense_output=False)
    similarity_books_index, _, similarity_score = find(similarity)

    # select the top 6 books and store their local index of the previous array
    books_similar = min(6, len(similarity_score))
    ind = np.argpartition(similarity_score, -books_similar)[-books_similar:]
    # get the book index
    books_indices = similarity_books_index[ind]

    #select the similarities ratings
    similarity_selected_books = similarity_score[ind]

    #similarity dict of books with the book_j
    similarity_selected_books_dic = {}
    for k in range(len(similarity_selected_books)):
        similarity_selected_books_dic[books_indices[k]] = similarity_selected_books[k]

    # store here abs(expected_rating-real_rating)
    all_differences_predicted_real_ratings = []

    # predict the score for each user of the book of this loop
    for user in user_rating_real:
        # check books in common that users has rated and are recomended in the top 6
        common_books_dic = books_common(user, books_indices, A)

        # if there are more than 1 book in common proceed
        if len(common_books_dic) > 1:
            # apply formula of
            # http://cs229.stanford.edu/proj2008/Wen-RecommendationSystemBasedOnCollaborativeFiltering.pdf
            # page 2 bottom
            sum_numerator = 0
            sum_denominator = 0
            for key in common_books_dic.keys():
                sum_numerator += common_books_dic[key]*similarity_selected_books_dic[key]
                sum_denominator += np.abs(similarity_selected_books_dic[key])
            # add to the list the difference
            all_differences_predicted_real_ratings.append((sum_numerator/sum_denominator-user_rating_real[user])**2)
    print("RMSD of ", isbn_to_book[index_to_books[book]], ":",round(np.sqrt(np.mean(all_differences_predicted_real_ratings)), 2))


