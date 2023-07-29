import random
import datetime
import pandas as pd
import ast


# Лучшие ароматы
def rated_top(perfumes, top_n=20):
    return list(perfumes.sort_values('weighted_rating', ascending=False)['id'].iloc[:top_n])


# Лучшие весенние ароматы
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
    return list(perfumes[perfumes.season == season].sort_values('weighted_rating', ascending=False)['id'].iloc[:top_n])


# Самые популярные
def popularity_top(perfumes, top_n=20):
    return list(perfumes.sort_values('ratings_count', ascending=False)['id'].iloc[:top_n])


# Новинки
def date_top(perfumes, top_n=20):
    return list(perfumes.sort_values('date', ascending=False)['id'].iloc[:top_n])


# Самые стойкие
def longevity_top(perfumes, top_n=20):
    return list(perfumes[perfumes.longevity == "['very_long']"].sort_values('weighted_rating', ascending=False)['id'].iloc[:top_n])


# Может вам понравиться
def get_SVD_recommendations(users, user_id, top_n=20):
    all_perfume_ids = set()
    for likes in users['likes']:
        all_perfume_ids.update(ast.literal_eval(likes))
    random_perfume_ids = random.sample(all_perfume_ids, top_n)
    return random_perfume_ids

# На основе ваших предпочтений
def get_content_recommendations(users, perfumes, user_id, top_n=20):
    all_perfume_ids = set()
    for likes in users['likes']:
        all_perfume_ids.update(ast.literal_eval(likes))
    random_perfume_ids = random.sample(all_perfume_ids, top_n)
    return random_perfume_ids


# Похожие ароматы
def find_similar_content(perfumes, perfume_id, top_n=20):
    all_perfume_ids = perfumes['id'].tolist()
    random_perfume_ids = random.sample(all_perfume_ids, top_n)
    return random_perfume_ids


# С этим также выбирают
def find_similar_SVD(users, perfume_id, top_n=20):
    all_perfume_ids = set()
    for likes in users['likes']:
        all_perfume_ids.update(ast.literal_eval(likes))
    random_perfume_ids = random.sample(all_perfume_ids, top_n)
    return random_perfume_ids
