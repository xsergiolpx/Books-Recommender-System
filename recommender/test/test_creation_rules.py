from recommender.core.association_rules.arules_utils import read_rules, create_transactions, find_matches
from recommender.core.utils.export_import_tools import import_dic, download_name

#create_transactions(threshold=5)
rules = read_rules("data/association_rules/rules_0.00012.csv")
entry = "0439136369,0439064872,0747545111,0440224764,0613496744,0312282540, 044021145X"

books = import_dic("data/association_rules/isbn_to_books")

f = lambda x: books[x]

print("[Association] Using Association rules")
print("--- You like: ")

for x in entry.split(','):
    try:
        print(x, f(x))
    except KeyError:
        print("Using download ", x, download_name(x))

print("--- Then you may like:")

results = find_matches(rules, entry, query_type="ain")

for result in results:
    if result[5] == "in":
        print("Book %s is recommended by: %s with support %0.2f confidence %0.2f and lift %0.2f"%(result[1],
                                                                                                  result[6],
                                                                                                  result[2],
                                                                                                  result[3],
                                                                                                  result[4]))
    else:
        print("Book %s is recommended by: %s with support %0.2f confidence %0.2f and lift %0.2f" % (result[1],
                                                                                                    result[6],
                                                                                                    result[2],
                                                                                                    result[3],
                                                                                                    result[4]))

