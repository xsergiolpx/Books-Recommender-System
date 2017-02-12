from export_import_tools import *
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix, find
import numpy as np
import operator


#Harry Potter books
#books = ["0439567610", "0747545111", "0613496744", "0312282540"]

def item_based(books):
    # Load isbn to book title:
    isbn_to_book = import_dic("isbn_to_books")

    # load the utility sparse matrix
    A = import_matrix("utility_matrix_prepared_item_based")
    total_users = A.shape[1]
    total_books = A.shape[0]


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

        #compute the average rating of each book of the selected ones
        # with the weight of the similarity
        for jj in range(len(books_indices)):
            j = books_indices[jj]
            score = similarity_selected_books[jj]
            _, _, score_book_j = find(A[j,:])
            book_and_scores[j] = np.mean(score_book_j)*score/10

            '''
            # Uncomment to see the similarity values
            try:
                print(score, isbn_to_book[index_to_books[j]], isbn_to_book[index_to_books[book]])
            except Exception:
                pass
            '''

    # sort by scores
    sorted_book_and_scores = sorted(book_and_scores.items(), key=operator.itemgetter(1), reverse=True)


    # Show read books:
    print("#### Item Based Recommendations ####")
    print("\n--- You like:")
    for book in books_j:
        print(isbn_to_book[index_to_books[book]])

    print("\n--- Then you might like:")

    counter = 1
    for i in range(len(sorted_book_and_scores)):
        if counter > 5: #show only 5 in the output
            break
        book_index = sorted_book_and_scores[i][0]
        isbn = index_to_books[book_index]
        try:
            if isbn not in books: # check the book is not in the input list
                recommended_book = isbn_to_book[isbn]
                print(recommended_book,"(pseudoscore", round(sorted_book_and_scores[i][1], 2), ")")
                counter += 1
        except KeyError: # the isbn is not in the data set mapped to a title, get it from the internet
            name = download_name(isbn)
            if len(name) > 0:
                print(name,"(pseudoscore", round(sorted_book_and_scores[i][1], 2), ")")
                counter +=1
