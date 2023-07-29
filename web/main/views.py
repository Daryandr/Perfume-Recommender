from django.shortcuts import render
from .models import Perfume, Users
from .algorithms import rated_top, season_top, popularity_top, date_top, longevity_top, get_SVD_recommendations, get_content_recommendations, find_similar_content, find_similar_SVD
import pandas as pd


all_perfume = Perfume.objects.all()
perfumes = list(all_perfume.values())
df_perfumes = pd.DataFrame(perfumes)
all_users = Users.objects.all()
users = list(all_users.values())
df_users = pd.DataFrame(users)


def index(req):
    id_perfume_rated = rated_top(df_perfumes)
    list_perfume_rated = Perfume.objects.filter(
        id__in=id_perfume_rated).values_list("id", "title", "image_url")
    
    id_perfume_season = season_top(df_perfumes)
    list_perfume_season = Perfume.objects.filter(
        id__in=id_perfume_season).values_list("id", "title", "image_url")
    
    id_perfume_popularity = popularity_top(df_perfumes)
    list_perfume_popularity = Perfume.objects.filter(
        id__in=id_perfume_popularity).values_list("id", "title", "image_url")
    
    id_perfume_date = date_top(df_perfumes)
    list_perfume_date = Perfume.objects.filter(
        id__in=id_perfume_date).values_list("id", "title", "image_url")
    
    id_perfume_longevity = longevity_top(df_perfumes)
    list_perfume_longevity = Perfume.objects.filter(
        id__in=id_perfume_longevity).values_list("id", "title", "image_url")

    id_user = req.POST.get("id_user")
    id_perfume_user_SVD = get_SVD_recommendations(df_users, id_user)
    list_perfume_user_SVD = Perfume.objects.filter(
        id__in=id_perfume_user_SVD).values_list("id", "title", "image_url")
    
    id_perfume_user_content = get_content_recommendations(
        df_users, df_perfumes, id_user)
    list_perfume_user_content = Perfume.objects.filter(
        id__in=id_perfume_user_content).values_list("id", "title", "image_url")
    
    nik_user = Users.objects.get(id=int(id_user))

    return render(req, 'main/index.html',
                  {'list_perfume_rated': list_perfume_rated,
                   'list_perfume_season': list_perfume_season,
                   'list_perfume_popularity': list_perfume_popularity,
                   'list_perfume_date': list_perfume_date,
                   'list_perfume_longevity': list_perfume_longevity,
                   'list_perfume_user_SVD': list_perfume_user_SVD,
                   'list_perfume_user_content': list_perfume_user_content,
                   'nik_user': nik_user})


def perfume(req, id):
    all_info_perfume = Perfume.objects.get(id=int(id))
    info_perfume = Perfume.objects.filter(id=int(id))
    list_perfume = list(info_perfume.values())
    accords_perfume = list_perfume[0]['accords'].split(',')
    accords_perfume = [item.capitalize() for item in accords_perfume]
    notes_perfume = list_perfume[0]['notes'].split(',')

    id_perfume_similar_content = find_similar_content(df_perfumes, id)
    list_perfume_similar_content = Perfume.objects.filter(
        id__in=id_perfume_similar_content).values_list("id", "title", "image_url")
    
    id_perfume_similar_SVD = find_similar_SVD(df_users, id)
    list_perfume_similar_SVD = Perfume.objects.filter(
        id__in=id_perfume_similar_SVD).values_list("id", "title", "image_url")

    return render(req, 'main/perfume.html',
                  {'info_perfume': all_info_perfume,
                   'notes_perfume': ', '.join(notes_perfume),
                   'accords_perfume': ', '.join(accords_perfume),
                   'list_perfume_similar_content': list_perfume_similar_content,
                   'list_perfume_similar_SVD': list_perfume_similar_SVD})


















def start(req):
    all_perfume = Perfume.objects.all()
    perfumes = list(all_perfume.values())
    df_perfumes = pd.DataFrame(perfumes)
    list_perfume = rated_top(df_perfumes)
    # list_perfume1 = Perfume.objects.filter(
    #     id__in=list_perfume).values_list("title")
    return render(req, 'main/start.html', {'list_perfume': list_perfume})
