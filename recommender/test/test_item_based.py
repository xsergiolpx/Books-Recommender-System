import time
import online.core.collaborative_filtering.DictionaryController as dc
import online.core.collaborative_filtering.ItemBasedCollaborativeFiltering as ib


def test_item_based_similarity():
    isbn_dict = dc.load_dict_json('/online/data/isbn_dict.json')
    users_dict = dc.load_dict_json('/online/data/users_dict.json')

    before = time.time()

    query_isbn = '0316666343'
    l = ib.item_based_similarity(query_isbn, isbn_dict, users_dict, 'cosine')
    l.sort(key=lambda tup: tup[1], reverse=True)
    print(l[0:10])

    after = time.time()
    print(after - before)


def test_build_isbn_dictionary():
    start_time = time.time()
    isbn_dict = dc.build_isbn_dictionary()
    dc.save_dict_json(isbn_dict, 'test_isbn_dict.json')
    elapsed_time = time.time() - start_time
    print(elapsed_time)
    return isbn_dict


def test_build_users_dictionary():
    isbn_dict = dc.load_dict_json('/online/data/isbn_dict.json')
    start_time = time.time()
    users_dict = dc.build_users_dictionary(isbn_dict)
    dc.save_dict_json(users_dict, 'test_users_dict.json')
    elapsed_time = time.time() - start_time
    print(elapsed_time)


def test_load_dict_json():
    isbn_dict = dc.load_dict_json('isbn_dict.json')
    users_dict = dc.build_users_dictionary(isbn_dict)


def test_get_most_rated():
    isbn_dict = ib.load_dict_json('../data/isbn_dict.json')
    most_read = None
    for k in isbn_dict.keys():
        if len(isbn_dict[k]) > 500:
            most_read = (k, len(isbn_dict[k]))
            break
    print(most_read)

test_get_most_rated()