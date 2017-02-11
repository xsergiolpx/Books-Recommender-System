from recommendation.association_rules.utils import read_rules, create_transactions, find_matches
from sergio.export_import_tools import import_dic

#create_transactions(threshold=5)
rules = read_rules("data/rules_0.00012.csv")
entry = "0373483503,0515128554,0515132020"

books = import_dic("isbn_to_books")

f = lambda x: books[x]

print("Matches for: ", [x for x in map(f, entry.split(','))])
results = find_matches(rules, entry)
for result in results:
    print(result)

