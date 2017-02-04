from export_import import *
from sklearn.metrics.pairwise import cosine_similarity

A = import_matrix("utility_matrix")

print(cosine_similarity(A, dense_output=False))