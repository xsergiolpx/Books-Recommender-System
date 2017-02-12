import sklearn.metrics.pairwise as pw
import pandas as pd


def cosine_similarity_df(df, movie_isbn):
    df.dropna(axis=1, how='all', inplace=True)
    df.fillna(0, inplace=True)
    user_rates = df.loc[movie_isbn]
    sim_df = pd.DataFrame(pw.cosine_similarity(df.as_matrix(), user_rates),index=df.index, columns=['coef'])
    sim_df.to_csv("df.csv")
    return sim_df.sort_values(by='coef', ascending=False, axis=0)