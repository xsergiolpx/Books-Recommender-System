from math import log,sqrt
from collections import Counter


class ContentBased:
    def __init__(self, k, sample_size, query_list_isbn, books):
        self.k = k
        self.sample_size = sample_size
        self.query_list_isbn = query_list_isbn
        self.books = books

    def scalar(self, collection):
        total = 0
        for count in collection.values():
            total += count * count
        return sqrt(total)

    def text_similarity(self, text_1, text_2):
        A = dict(Counter(text_1.split()))
        B = dict(Counter(text_2.split()))
        total = 0
        for word in A:
            if word in B:
                total += A[word] * B[word]
        if total != 0:
            return float(total) / (self.scalar(A)*self.scalar(B))
        else:
            return 0

    def get_k_similar(self, query_isbn, w=[1,2,1]):
        book1 = self.books.loc[query_isbn]  # avoid more than one access to the dataframe 'books'

        # filter the books by genre, it doesn't calculate the similarity between books of different genres
        all_isbn = self.books.loc[self.books['Hashed-Genre'] == book1['Hashed-Genre']]

        # sample the books
        if len(all_isbn) >= self.sample_size:
            all_isbn = all_isbn.sample(self.sample_size)

        title_1 = book1['Book-Title']
        author_1 = book1['Book-Author']
        year_1 = book1['Year-Of-Publication']

        sim_list = []
        for isbn in set(all_isbn.index) - set(self.query_list_isbn):
            book2 = all_isbn.loc[isbn]

            title_2 = book2['Book-Title']
            title_sim = self.text_similarity(title_1, title_2)  # calculate the similarity between titles using cosine similarity

            author_sim = 0
            if author_1 == book2['Book-Author']:
                author_sim = 1

                # if the author and title are the same, we penalize the book (maybe just the edition is different)
                if title_sim >= 0.99:
                    title_sim = -7

            year_sim = 0
            query_year = year_1
            # we potentialize books in the range of 10 years
            if query_year-5 <= book2.loc['Year-Of-Publication'] <= query_year+5:
                year_sim = 1

            total_sim = (w[0]*title_sim + w[1]*author_sim + w[2]*year_sim)/sum(w)
            sim_list.append((isbn,total_sim))
        sim_list.sort(key=lambda tup: tup[1], reverse=True)
        return sim_list[:self.k]

    def get_similar_books(self):
        k_similars = []
        for query_isbn in self.query_list_isbn:
            k_similars = k_similars + self.get_k_similar(query_isbn)
        k_similars.sort(key=lambda tup: tup[1], reverse=True)
        return k_similars[:self.k]