from online.core.utils.export_import_tools import import_matrix, export_matrix

# Load the matrix
A = import_matrix("data/collaborative_filtering/utility_matrix")

# transpose it to make the item based (if is for user based just comment this line)
A = A.transpose()

# Save
export_matrix(A, "data/collaborative_filtering/utility_matrix_prepared_item_based")

print("Done")