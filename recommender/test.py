import numpy as np
import pandas as pd
from surprise import (
    Reader,
    Dataset,
    SVD,
    accuracy
)
from surprise.model_selection import cross_validate, KFold, train_test_split
from collections import defaultdict
from surprise.accuracy import rmse, mae, fcp
import ast
from sklearn.metrics import roc_curve, roc_auc_score


# Вычисление метрик для коллаборативной фильтрации
def get_metrics_at_k(predictions, k=10, threshold=0.5):
    user_est_true = defaultdict(list)
    for uid, _, true_r, est, _ in predictions:
        user_est_true[uid].append((est, true_r))
    precisions = dict()
    recalls = dict()
    reciprocal_ranks = dict()
    ndcgs = dict()
    for uid, user_ratings in user_est_true.items():
        user_ratings.sort(key=lambda x: x[0], reverse=True)
        n_rel = sum((true_r >= threshold) for (_, true_r) in user_ratings)
        n_rec_k = sum((est >= threshold) for (est, _) in user_ratings[:k])
        n_rel_and_rec_k = sum(
            ((true_r >= threshold) and (est >= threshold))
            for (est, true_r) in user_ratings[:k]
        )
        precisions[uid] = n_rel_and_rec_k / n_rec_k if n_rec_k != 0 else 0
        recalls[uid] = n_rel_and_rec_k / n_rel if n_rel != 0 else 0
        rank = next((i + 1 for i, (est, true_r) in enumerate(user_ratings[:k]) if true_r >= threshold), 0)
        reciprocal_ranks[uid] = 1 / rank if rank != 0 else 0
        dcg = sum((2 ** true_r - 1) / np.log2(i + 2) for i, (est, true_r) in enumerate(user_ratings[:k]))
        idcg = sum((2 ** true_r - 1) / np.log2(i + 2) for i, (_, true_r) in
                   enumerate(sorted(user_ratings[:k], key=lambda x: x[1], reverse=True)))
        ndcgs[uid] = dcg / idcg if idcg != 0 else 0

    return precisions, recalls, reciprocal_ranks, ndcgs


k = 5
kf = KFold(n_splits=k)
algo = SVD(n_factors=50, n_epochs=20, reg_all=0.1, lr_all=0.005)
total_precision = 0
total_recall = 0
total_rmse = 0
total_mae = 0
total_fcp = 0
total_f1 = 0
total_mrr = 0
total_ndcg = 0
total_roc = 0
for trainset, testset in kf.split(data):
    algo.fit(trainset)
    predictions = algo.test(testset)
    precisions, recalls, reciprocal_ranks, ndcgs = get_metrics_at_k(predictions)
    y_true = [pred.r_ui for pred in predictions]
    y_scores = [pred.est for pred in predictions]
    precision_avg = sum(prec for prec in precisions.values()) / len(precisions)
    recall_avg = sum(rec for rec in recalls.values()) / len(recalls)
    total_ndcg += sum(ndcg for ndcg in ndcgs.values()) / len(ndcgs)
    total_precision += precision_avg
    total_recall += recall_avg
    total_rmse += rmse(predictions)
    total_mae += mae(predictions)
    total_fcp += fcp(predictions)
    total_f1 += 2 * (precision_avg * recall_avg) / (precision_avg + recall_avg)
    total_mrr += sum(rank for rank in reciprocal_ranks.values()) / len(reciprocal_ranks)
    total_roc += roc_auc_score(y_true, y_scores)
avg_precision = total_precision / k
avg_recall = total_recall / k
avg_rmse = total_rmse / k
avg_mae = total_mae / k
avg_fcp = total_fcp / k
avg_f1 = total_f1 / k
avg_mrr = total_mrr / k
avg_ndcg = total_ndcg / k
avg_roc = total_roc / k


# Вычисление метрик для контентной фильтрации
def calculate_precision_recall(user_likes, recommendations):
    intersection = set(user_likes) & set(recommendations)
    precision = len(intersection) / len(recommendations) if len(recommendations) > 0 else 0
    recall = len(intersection) / len(user_likes) if len(user_likes) > 0 else 0
    return precision, recall


def calculate_f1_score(precision, recall):
    if precision + recall == 0:
        return 0
    f1_score = 2 * (precision * recall) / (precision + recall)
    return f1_score


def calculate_mrr(user_likes, recommendations):
    for rank, item in enumerate(recommendations, start=1):
        if item in user_likes:
            return 1 / rank
    return 0


def calculate_ndcg(liked, recs, top_n):
    if not liked or not recs:
        return 0.0
    relevance = np.zeros(top_n)
    for i, rec in enumerate(recs):
        if rec in liked:
            relevance[i] = 1.0
    dcg = relevance[0] + np.sum(relevance[1:] / np.log2(np.arange(2, top_n + 1)))
    ideal_relevance = np.sort(relevance)[::-1]
    idcg = ideal_relevance[0] + np.sum(ideal_relevance[1:] / np.log2(np.arange(2, top_n + 1)))
    ndcg = dcg / idcg if idcg > 0.0 else 0.0
    return ndcg


def evaluate_model(train_data, test_data, sim_matrix, top_n=10):
    p = []
    r = []
    f1 = []
    mrr = []
    ndcg = []

    for user_id in users.iloc[:25000].userID:
        disliked = ast.literal_eval(users.loc[users['userID'] == user_id, 'dislike'].values[0])
        liked = test_data.loc[test_data['userID'] == user_id, 'likes'].values[0]
        recs = get_recommendations(train_data, user_id, sim_matrix, list(set(liked + disliked)), top_n)
        precision, recall = calculate_precision_recall(liked, recs)
        p.append(precision)
        r.append(recall)
        f1.append(calculate_f1_score(precision, recall))
        mrr.append(calculate_mrr(liked, recs))
        ndcg.append(calculate_ndcg(liked, recs, top_n))

    average_precision = sum(p) / len(p)
    average_recall = sum(r) / len(r)
    average_f1 = sum(f1) / len(f1)
    average_mrr = sum(mrr) / len(mrr)
    average_ndcg = sum(ndcg) / len(ndcg)

    return average_precision, average_recall, average_f1, average_mrr, average_ndcg


average_precision1, average_recall1, average_f1_1, average_mrr1, average_ndcg1 = evaluate_model(train1, test1,
                                                                                                sim_matrix, 10)
average_precision2, average_recall2, average_f1_2, average_mrr2, average_ndcg2 = evaluate_model(train2, test2,
                                                                                                sim_matrix, 10)
average_precision3, average_recall3, average_f1_3, average_mrr3, average_ndcg3 = evaluate_model(train3, test3,
                                                                                                sim_matrix, 10)

average_precision = (average_precision1 + average_precision2 + average_precision3) / 3
average_recall = (average_recall1 + average_recall2 + average_recall3) / 3
average_f1 = (average_f1_1 + average_f1_2 + average_f1_3) / 3
average_mrr = (average_mrr1 + average_mrr2 + average_mrr3) / 3
average_ndcg = (average_ndcg1 + average_ndcg2 + average_ndcg3) / 3
