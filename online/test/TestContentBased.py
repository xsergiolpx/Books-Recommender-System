import online.core.ContentBasedRecommender.LoadData as ld



books = ld.load_books('../../BX-CSV-Dump/BX-Books.csv')
#print(len(books['Book-Author'].unique()))
books['Book-Author'] = books['Book-Author'].apply(lambda x: ld.hash_text(x))
#print(len(books['Book-Author'].unique()))

#print(len(books['Book-Title'].unique()))
books['Book-Title'] = books['Book-Title'].apply(lambda x: ld.process_book_name(x))
#print(len(books['Book-Title'].unique()))

print(books)