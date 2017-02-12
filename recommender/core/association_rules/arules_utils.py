import pandas as pd
from itertools import combinations
from recommender.core.utils.export_import_tools import import_dic
from time import time
import re


def create_transactions(threshold, filename="data/input/BX-Book-Ratings.csv"):
    df = pd.read_csv(filename, delimiter=';', encoding='ISO-8859-1')
    df.columns = ['user', 'isbn', 'rating']

    df = df[df["rating"] >= threshold]

    file = open('transactions.csv', 'w')

    for user in list(set(df["user"])):
        tran = []
        for isbn in df[df.user == user]["isbn"]:
            tran.append(str(isbn))
        file.write(';'.join([str(user), ','.join(tran)])+'\n')

    file.close()


def read_rules(filename):
    df = pd.read_csv(filename, delimiter=',', index_col=0)
    regex = r"\{(.*?)\}"

    lhs, rhs = [], []

    for rule in df["rules"]:
        left, right = re.findall(regex, rule)
        lhs.append(left)
        rhs.append(right)

    df["lhs"], df["rhs"] = lhs, rhs

    df.drop(["rules"], axis=1, inplace=True)

    return df


def find_matches(rules, lhs, query_type="ain"):
    isbns = lhs.split(',')
    results = []

    interest = set(isbns)

    books = import_dic("data/association_rules/isbn_to_books")

    tic = time()
    if query_type == "ain" or query_type == "all":
        for r in range(1, len(isbns)+1):
            for query in combinations(isbns, r):
                matchs = rules.loc[rules["lhs"] == ','.join(query)][["rhs", "support", "confidence", "lift"]]
                if matchs.shape[0]>0:
                    for rh, s, c, l in zip(matchs["rhs"], matchs["support"], matchs["confidence"], matchs["lift"]):
                        if rh not in interest:
                            results.append([r, rh, s, c, l, "ain", ','.join(query)])

    if query_type == "in" or query_type == "all":
        for isbn in isbns:
            # matchs = rules[rules.lhs.str.contains("|".join(isbns))==True][["rhs", "support", "confidence", "lift"]]
            matchs = rules[rules.lhs.str.contains(isbn)][["rhs", "support", "confidence", "lift"]]
            if matchs.shape[0] > 0:
                for rh, s, c, l in zip(matchs["rhs"], matchs["support"], matchs["confidence"], matchs["lift"]):
                    if rh not in interest:
                        results.append([0,rh, s, c, l, "in", books[isbn]])

    # Sort and filter
    results.sort(key=lambda x: (x[0], x[3], x[2]), reverse=True)

    retrieve = []

    for result in results:
        if result[1] not in interest:
            print(result[1], books[result[1]])
            interest.add(result[1])
            result[1] = books[result[1]]
            retrieve.append(result)

    print("[Association] Query time: %0.2f"%(time()-tic))

    return retrieve