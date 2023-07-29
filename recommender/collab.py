import numpy as np
import pandas as pd
import ast
from surprise import (
    Reader,
    Dataset,
    SVD,
)

# Подготовка данных
users = pd.read_csv("final_users.csv")
df = users[['userID', 'likes', 'dislike']]
df['likes'] = df['likes'].apply(lambda r: ast.literal_eval(r))
df['dislike'] = df['dislike'].apply(lambda r: ast.literal_eval(r))
liked_df = df.explode('likes')[['userID', 'likes']]
liked_df.columns = ['user_id', 'perfume_id']
liked_df['rating'] = 1
disliked_df = df.explode('dislike')[['userID', 'dislike']]
disliked_df.columns = ['user_id', 'perfume_id']
disliked_df['rating'] = 0
df = pd.concat([liked_df, disliked_df],
               ignore_index=True).sort_values(by='user_id')
reader = Reader(rating_scale=(0, 1))
data = Dataset.load_from_df(df[['user_id', 'perfume_id', 'rating']], reader)
trainset = data.build_full_trainset()
# Обучение модели SVD
algo = SVD(n_factors=50, n_epochs=20, reg_all=0.1, lr_all=0.005)
algo.fit(trainset)
algo.save('svd_model')

# Обучение модели kNN
sim_options = {'user_based': False}
algo = KNNBasic(sim_options=sim_options)
algo.fit(trainset)
algo.save('knn_model')


# Функция для поиска наиболее похожих продуктов
def find_similar_perfumes(model, train, perfume_id, k=20):
    perfume_inner_id = train.to_inner_iid(perfume_id)
    neighbors = model.get_neighbors(perfume_inner_id, k=k)
    similar_perfumes = [train.to_raw_iid(inner_id) for inner_id in neighbors]
    return similar_perfumes


# Функция формирования рекомендаций
def get_top_recommendations(model, train, user_id, top_n=20):
    user_inner_id = train.to_inner_uid(user_id)
    user_ratings = train.ur[user_inner_id]
    user_iids = [item_id for (item_id, _) in user_ratings]
    all_iids = train.all_items()
    candidate_iids = list(set(all_iids) - set(user_iids))
    predictions = [model.predict(user_inner_id, item_id)
                   for item_id in candidate_iids]
    top_predictions = sorted(
        predictions,
        key=lambda x: x.est,
        reverse=True)[:top_n]
    recommended_item_ids = [train.to_raw_iid(prediction.iid)
                            for prediction in top_predictions]

    return recommended_item_ids
