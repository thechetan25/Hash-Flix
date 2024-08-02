from django.urls import path
from . import views

urlpatterns = [
    path('', views.search, name='search'),
    path('mv/search/more/', views.mv_search_more, name='mv_search_more'),
    path('tv/search/more/', views.tv_search_more, name='tv_search_more'),
]
