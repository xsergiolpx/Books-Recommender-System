from scipy import io
import numpy as np

# Save a dictionary
def export_dic(dic, filename):
    np.save("data/" + filename + '.npy', dic)

# Load a dictonary
def import_dic(filename):
    return np.load("data/" +filename + '.npy').item()


def export_matrix(m, filename):
    '''
    Exports a scipy matrix to a file
    :param m: scipy matrix
    :param filename: name of the file without extension
    :return: nothing
    '''
    io.mmwrite("data/" + filename + ".mtx", m)

def import_matrix(filename):
    '''
    imports a scipy matrix
    :param filename: filename without extension
    :return: the scipy matrix
    '''
    return io.mmread("data/" + filename + ".mtx").tocsr()


