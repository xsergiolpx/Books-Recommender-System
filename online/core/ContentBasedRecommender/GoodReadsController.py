


class GoodReadsController():
    CONSUMER_KEY = 'gsyDVEcZ3ZOFqDvXxrA'
    CONSUMER_SECRET = 'U182SOVsGZRYY7IFJ7jqpltLyXkBvPwp9mUnLsWcek'
    gr = None
    count = None
    isbn_found = []
    isbn_not_found = []

    def __init__(self):
        self.gr = client.GoodreadsClient(self.CONSUMER_KEY, self.CONSUMER_SECRET)
        self.count = 0

    def get_shelves(self, isbn):
        while True:
            self.count += 1
            print(self.count)
            try:
                shelves = self.gr.book(isbn=isbn).popular_shelves
                self.isbn_found.append(isbn)
                if len(self.isbn_found) % 100 == 0:

                return shelves
            except Exception:
                self.isbn_not_found.append(isbn)
                print("Error in ISBN ", isbn)
                return []
