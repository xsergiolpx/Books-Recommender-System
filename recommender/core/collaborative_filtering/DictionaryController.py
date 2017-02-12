import json
import os
import pandas as pd


def build_users_dictionary(isbn_dict):
    users_dict = {}
    j = 0
    for isbn in isbn_dict.keys():
        print("Reading book ", j, " from ", len(isbn_dict.keys()))
        users = list(isbn_dict[isbn].keys())
        for u in users:
            if u in users_dict:
                users_dict[u].append(isbn)
            else:
                users_dict[u] = [isbn]
        j += 1
    return users_dict


def build_isbn_dictionary(filename="/data/input/BX-Book-Ratings.csv", save_freq=300):
    df = pd.read_csv(filename, delimiter=';', encoding='ISO-8859-1', index_col='ISBN')
    df.sort_index(inplace=True)

    old_dict = load_dict_json('data/content_based/isbn_dict.json')
    books = list(set(df.index) - set(old_dict.keys()))   # list of all ISBNs/books not already processed
    new_dict = {}
    i = 0
    total_books = len(books)
    for b in books:
        print("Reading book ", i, " of ", total_books)
        i += 1
        b_values = df.loc[[b]].values
        new_dict[b] = {str(key): str(value) for (key, value) in b_values}
        if i%save_freq == 0:
            save_dict_json(merge_dict(old_dict, new_dict), 'data/content_based/isbn_dict.json')
    return merge_dict(old_dict, new_dict)


def merge_dict(d1, d2):
    d1.update(d2)
    return d1


def save_dict_json(dict, filename):
    with open(filename, 'w') as fp:
        json.dump(dict, fp)
    fp.close()


def load_dict_json(filename):
    if os.path.isfile(filename) is False:
        return {}
    with open(filename, 'r') as fp:
        return json.load(fp)