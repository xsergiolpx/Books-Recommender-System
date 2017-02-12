from export_import_tools import *

# Load the matrix
A = import_matrix("utility_matrix")

# transpose it to make the item based (if is for user based just comment this line)
A = A.transpose()

# Save
export_matrix(A, "utility_matrix_prepared_item_based")

print("Done")