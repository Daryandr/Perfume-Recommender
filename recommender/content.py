import numpy as np
import pandas as pd
import ast
import re
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer, MinMaxScaler

# Подготовка данных
perfume = pd.read_csv("final_perfume.csv")
users = pd.read_csv("final_users.csv")
mlb = MultiLabelBinarizer()
transformed_data = mlb.fit_transform(perfume['accords'].str.split(','))
accords = pd.DataFrame(
    transformed_data,
    columns=mlb.classes_,
    index=perfume['perfume_id']).astype(float)


def get_notes_dict(notes_str):
    notes_dict = {}
    pattern = r'([a-zA-Z]+)(\d+)([a-zA-Z ]+)'
    for note in notes_str.split(','):
        note_parts = re.match(pattern, note.strip())
        note_type = note_parts.group(1)
        note_number = 40 - int(note_parts.group(2))
        note_name = note_parts.group(3).strip()
        notes_dict[f'{note_type}_{note_name}'] = note_number
    return notes_dict


df = pd.DataFrame({'notes': perfume['notes']})
notes_dicts = df['notes'].apply(get_notes_dict).tolist()
notes = pd.DataFrame(notes_dicts).fillna(0).astype(float)
scaler = MinMaxScaler()
normalized_df = scaler.fit_transform(notes.values)
notes = pd.DataFrame(
    normalized_df,
    columns=notes.columns,
    index=perfume.perfume_id)

accords_notes = pd.concat((accords, notes), axis=1)
perfume_similarities = cosine_similarity(accords_notes)
sim_matrix = pd.DataFrame(perfume_similarities, columns=perfume.perfume_id, index=perfume.perfume_id)


# Функция поиска похожих продуктов
def find_similar_perfumes(perfume_id, similarities_matrix, n_similar=20):
    similarities = similarities_matrix.loc[:, perfume_id].sort_values(ascending=False)[1:]
    similar_perfumes = [i for i in similarities.index
                        if similarities[i] != 0]
    return similar_perfumes[:n_similar]


# Функция формирования рекомендаций
def get_recommendations(users_df, user_id, similarities_matrix, top_n=20):
    liked_perfumes = ast.literal_eval(users_df.loc[users_df['userID'] == user_id, 'likes'].values[0])
    disliked_perfumes = ast.literal_eval(users_df.loc[users_df['userID'] == user_id, 'dislike'].values[0])
    similarities = similarities_matrix.loc[:, liked_perfumes].sum(axis=1).sort_values(ascending=False)
    rec_perfumes = [i for i in similarities.index
                    if i not in liked_perfumes
                    and i not in disliked_perfumes
                    and similarities[i] != 0]

    return rec_perfumes[:top_n]
