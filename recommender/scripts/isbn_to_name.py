from recommender.core.utils.export_import_tools import export_dic
import pandas as pd


# Read and delete all columns but isbn and title
df = pd.read_csv("data/input/BX-Books.csv", sep=";", encoding = "ISO-8859-1", error_bad_lines=False)

df.drop(['Book-Author', 'Year-Of-Publication', 'Publisher',
       'Image-URL-S', 'Image-URL-M', 'Image-URL-L'], 1, inplace=True)

isbn = df["ISBN"].values
books = df["Book-Title"].values

# create the dict like {0583492: "100 years of solitude", ...}
isbn_to_books = {isbn[i]: books[i] for i in range(len(isbn))}

# save
export_dic(isbn_to_books, "data/collaborative_filtering/isbn_to_books")

print("Done")