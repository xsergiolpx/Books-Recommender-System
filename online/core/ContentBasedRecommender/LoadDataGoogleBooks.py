import pandas as pd
import requests
import hashlib


def save_processed_content_based_dataframe(books, filename='../../data/processed_df.csv'):
    with open(filename, "w") as fp:
        books.to_csv(fp)
    fp.close()


def hash_text(author):
    h = hashlib.sha256(author.encode('utf-8'))
    return int(h.hexdigest(), base=16)


class gbooks():
    googleapikey="AIzaSyCk8G1jzmc3ir982I7hqZ-9Y3hYs6u13Wk"

    def search(self, isbn):
        #parms = {"q":value, 'key':self.googleapikey, 'isbn':'0849901243'}
        #https://www.googleapis.com/books/v1/volumes?q=isbn=0849901243&key=AIzaSyCk8G1jzmc3ir982I7hqZ-9Y3hYs6u13Wk
        url = "https://www.googleapis.com/books/v1/volumes?q=isbn="+isbn+"&key="+self.googleapikey
        r = requests.get(url=url)
        rj = r.json()
        try:
            genre = str(rj["items"][0]["volumeInfo"]["categories"][0]).lower().split()[0]
        except:
            genre = ''
        return genre


if __name__ == "__main__":
    books = pd.read_csv('../../data/processed_df.csv', delimiter=',', encoding='utf-8', index_col='ISBN')
    already_processed = books.dropna(subset=["Popular-Shelves"], how="any")
    to_be_read = set(books.index) - set(already_processed.index)
    bk = gbooks()
    i = 0
    chunk_size = 500
    for isbn in to_be_read:
        print("Reading book ", i, " of ", len(to_be_read))
        i+=1
        # try:
        genre = bk.search(isbn=isbn)
        if genre != '':
            books.set_value(isbn, 'Popular-Shelves', hash_text(genre))
        else:
            print("Error in ISBN ", isbn)
            books.set_value(isbn, 'Popular-Shelves', 0)
        if i % chunk_size == 0:
            save_processed_content_based_dataframe(books)
        # except:
        #     continue
    save_processed_content_based_dataframe(books)


