import numpy as np
import pandas as pd
import re

customers_df = pd.read_csv(
    "/kaggle/input/parisdata/profilesniche_prepared.csv")
perfume_df = pd.read_excel(
    "/kaggle/input/parisdata/all_checks_finished (1).xlsx",
    sheet_name='Sheet2')

perfume_df = perfume_df[~perfume_df.accords.isnull()]
perfume_df = perfume_df[perfume_df.date < 2024]
perfume_df = perfume_df[perfume_df.people > 4]
perfume_df = perfume_df[perfume_df.average_rating_ != 0]
fr = perfume_df[['longevity_poor',
                 'longevity_weak',
                 'longevity_moderate',
                 'longevity_long',
                 'longevity_very_long']]
fr.columns = ['poor', 'weak', 'moderate', 'long', 'very_long']
mask = fr.eq(fr.max(axis=1), axis=0)
perfume_df['longevity'] = (
    (fr.columns *
     mask)[mask].agg(
        lambda row: list(
            row.dropna()),
        axis=1))
perfume_df.loc[(perfume_df['longevity_poor'] == 0) & (perfume_df['longevity_weak'] == 0) & (
        perfume_df['longevity_moderate'] == 0) & (perfume_df['longevity_long'] == 0) & (
                       perfume_df['longevity_very_long'] == 0), 'longevity'] = perfume_df.loc[
    (perfume_df['longevity_poor'] == 0) & (perfume_df['longevity_weak'] == 0) & (
            perfume_df['longevity_moderate'] == 0) & (perfume_df['longevity_long'] == 0) & (
            perfume_df['longevity_very_long'] == 0), 'longevity'].apply(lambda x: [])
fr = perfume_df[['clswinter', 'clsspring', 'clssummer', 'clsautumn']]
fr.columns = ['winter', 'spring', 'summer', 'autumn']
mask = fr.eq(fr.max(axis=1), axis=0)
perfume_df['season'] = (
    (fr.columns *
     mask)[mask].agg(
        lambda row: list(
            row.dropna()),
        axis=1))
perfume_df.loc[(perfume_df['clswinter'] == 0) & (perfume_df['clsspring'] == 0) & (perfume_df['clssummer'] == 0) & (
        perfume_df['clsautumn'] == 0), 'season'] = perfume_df.loc[
    (perfume_df['clswinter'] == 0) & (perfume_df['clsspring'] == 0) & (perfume_df['clssummer'] == 0) & (
            perfume_df['clsautumn'] == 0), 'season'].apply(lambda x: [])
perfume_df = perfume_df.rename({"people": "ratings_count"}, axis="columns")
perfume_df.date = pd.to_numeric(perfume_df.date)


def check_condition(elem):
    return (
                   elem is not np.nan) and (
               not re.search(
                   r'\dnan$',
                   str(elem))) and (
               not re.search(
                   r'\d$',
                   str(elem)))


nFrame = perfume_df.iloc[:, 69:]
nFrame['notes'] = nFrame[0]
for i in range(1, 66):
    nFrame['notes'] = nFrame.apply(
        lambda row: row['notes'] + ',' + str(
            row[i]) if check_condition(
            row[i]) else row['notes'], axis=1)
perfume_df['notes'] = nFrame['notes']
perfume_df.image_url = perfume_df.perfume_id.apply(
    lambda x: 'https://fimgs.net/mdimg/perfume/375x500.' + str(x) + '.jpg')
perfume_df = perfume_df[['perfume_id',
                         'title',
                         'image_url',
                         'accords',
                         'notes',
                         'average_rating_',
                         'ratings_count',
                         'date',
                         'longevity',
                         'season']]
l = list(perfume_df.perfume_id)


def convert_to_int(lst):
    new_lst = []
    for item in lst:
        try:
            if (int(item) in l):
                new_lst.append(int(item))
        except ValueError:
            pass
    return new_lst


customers_df = customers_df.rename({"IDcustomer": "userID"}, axis="columns")
for i in ['favorite', 'love', 'like', 'dislike']:
    customers_df[i].fillna("0", inplace=True)
    customers_df[i] = customers_df[i].str.split(',')
    customers_df[i] = customers_df[i].apply(lambda x: list(
        map(lambda x: x[x.rfind('-') + 1:x.rfind('.')], x)))
    customers_df[i] = customers_df[i].apply(convert_to_int)
customers_df['likes'] = customers_df.apply(lambda x: list(
    set().union(*x[['favorite', 'love', 'like']].values)), axis=1)
customers_df = customers_df[customers_df['likes'].str.len() > 3]
customers_df = customers_df[customers_df['dislike'].str.len() > 0]
customers_df = customers_df[
    ['userID', 'name', 'likes', 'dislike']]
perfume_df.to_csv("final_perfume.csv", index=False)
customers_df.to_csv("final_users.csv", index=False)
