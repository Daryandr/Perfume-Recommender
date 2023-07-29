import numpy as np
import pandas as pd
import datetime

perfume = pd.read_csv("final_perfume.csv")


# вычисление взвешенного рейтинга
def weighted_rating(R, v, m, C):
    return (R * v + C * m) / (v + m)


mean_rating = perfume['average_rating_'].mean()
min_votes = perfume.ratings_count.quantile(0.7)
perfume['weighted_rating'] = perfume.apply(
    lambda x: weighted_rating(
        x['average_rating_'],
        x['ratings_count'],
        min_votes,
        mean_rating),
    axis=1)


def rated_top(perfumes, top_n=20):
    return list(perfumes.sort_values('weighted_rating',
                                     ascending=False)['perfume_id'].iloc[:top_n])


def season_top(perfumes, top_n=20):
    month = datetime.datetime.now().month
    if month in (12, 1, 2):
        season = "['winter']"
    elif month in (3, 4, 5):
        season = "['spring']"
    elif month in (6, 7, 8):
        season = "['summer']"
    else:
        season = "['autumn']"
    return list(perfumes[perfumes.season == season].sort_values(
        'weighted_rating', ascending=False)['perfume_id'].iloc[:top_n])


def popularity_top(perfumes, top_n=20):
    return list(perfumes.sort_values('ratings_count',
                                     ascending=False)['perfume_id'].iloc[:top_n])


def date_top(perfumes, top_n=20):
    return list(perfumes.sort_values('date', ascending=False)
                ['perfume_id'].iloc[:top_n])


def longevity_top(perfumes, top_n=20):
    return list(perfumes[perfumes.longevity == "['very_long']"].sort_values(
        'weighted_rating', ascending=False)['perfume_id'].iloc[:top_n])
