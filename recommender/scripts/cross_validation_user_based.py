from recommender.core.utils.export_import_tools import import_matrix, import_dic
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix, find
import numpy as np


def books_common(user_idx, user, A):
    '''
    :param user_idx: 894357943
    :param user: 34534334
    :param A: sparse matrix
    :return: books that both users have read with scores of the second
        {"324523": 9, "2342", 4}
    '''
    _ , books_first_user,_ = find(A[user_idx,:])
    _, books_second_user, _ = find(A[user,:])
    common_books =list(set(books_first_user).intersection(set(books_second_user)))
    _, local_index, rat = find(A[user,common_books])
    return {common_books[local_index[j]]: rat[j] for j in range(len(local_index))}



def cv_user_based(books):
    print("#### User Based RMSE of scores ####")
    # Load isbn to book title:
    isbn_to_book = import_dic("data/collaborative_filtering/isbn_to_books")

    # load the utility sparse matrix
    A = import_matrix("data/collaborative_filtering/utility_matrix")
    total_users = A.shape[1]
    total_books = A.shape[0]

    # Load the list of books
    books_to_index = import_dic("data/collaborative_filtering/books_to_index")
    index_to_books = import_dic("data/collaborative_filtering/index_to_books")

    # Change them to indices
    books_j = []
    for book in books:
        try:
            books_j.append(books_to_index[book])
        except KeyError:
            print(book, "not found in database")

    # store the book index and score in a dic
    book_and_scores = {}
    # run over all the books
    for book in books_j:
        rmse = []
        # take the vector of the book, each component is a rating from a user
        book_vector = A[:, book]
        # see who read that book
        users_idx,_, scores_real = find(book_vector)
        # create a dict of users and scores real
        users_scores_real = { users_idx[k]: scores_real[k] for k in range(len(users_idx))}
        for user_idx in users_scores_real:
            user_vector = A[user_idx, :]
            similarity = cosine_similarity(A, user_vector, dense_output=False)
            similarity_users_index, _, similarity_score = find(similarity)
            users_similar = min(5, len(similarity_score))
            ind = np.argpartition(similarity_score, -users_similar)[-users_similar:]
            # get the users index
            users_indices = similarity_users_index[ind]
            # select the similarities ratings
            similarity_selected_users = similarity_score[ind]

            similarity_selected_users_dic = {}
            for k in range(len(similarity_selected_users)):
                similarity_selected_users_dic[users_indices[k]] = similarity_selected_users[k]

            for user in similarity_selected_users_dic:
                common = books_common(user_idx, user, A)
                numerator = 0
                denom = 0
                if len(common) > 1:
                    for book_in_common in common:
                        numerator += similarity_selected_users_dic[user]*common[book_in_common]
                        denom += np.abs(similarity_selected_users_dic[user])
                    rmse.append((numerator/denom-users_scores_real[user_idx])**2)
        print("RMSE of ", isbn_to_book[index_to_books[book]], ":", round(np.sqrt(np.mean(rmse)),1))



