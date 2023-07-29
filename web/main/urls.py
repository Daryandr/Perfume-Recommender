from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('perfume/<id>', views.perfume),
    path('start/', views.start)
]
