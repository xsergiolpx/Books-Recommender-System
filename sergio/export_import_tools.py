from scipy import io
import numpy as np
import requests
from bs4 import BeautifulSoup

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


def download_name(isbn):
    '''
    if the name of the ISBN book is not present, downloads the name from the internet
    :param isbn: isbn
    :return: name of the book if is found, or "" if not
    '''
    url = "http://www.lookupbyisbn.com/Search/Book/"+ isbn + "/1"
    result = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/5Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.3637.36 (KHTML, like Gecko) Chrome/55.0.2883.91 Mobile Safari/537.36'})

    if result.status_code == 200:
        soup = BeautifulSoup(result.content, "lxml")
        return soup.find_all(style="font-size: 0.9em;")[0].text
    else:
        return ""



