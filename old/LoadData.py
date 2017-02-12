import random

import pandas as pd

from online.core.collaborative_filtering import ItemBasedCollaborativeFiltering as sc


def load_sample_data(filename, size):
    n = 1149780
    #n = sum(1 for line in open(filename, mode='r', encoding='ISO-8859-1').read()) - 1
    skip = sorted(random.sample(range(1,n+1),n-size))  # the 0-indexed header will not be included in the skip list
    df = pd.read_csv(filename, skiprows=skip, delimiter=';', encoding='ISO-8859-1')
    return df


def build_utility_matrix(df):
    df = df.pivot(index='ISBN', columns='User-ID', values='Book-Rating')
    df.dropna(axis=0, inplace=True, thresh=2)
    return df




def main():
    filename = "./BX-CSV-Dump/BX-Book-Ratings.csv"
    df = load_sample_data(filename, size=25000)
    df = build_utility_matrix(df)
    target_movie = df.sample(n=1).index
    most_sim = sc.cosine_similarity(df, target_movie)[1:6]
    print(most_sim.head())

if __name__ == "__main__":
    main()