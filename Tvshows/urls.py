from django.urls import path
from . import views

urlpatterns = [
    path('',views.home_view,name="tvshows-page"),
    path('detail/<str:media>/<int:id>/', views.tv_view, name="tv-detail"),
    path('episodes/<int:id>/',views.season_info , name="episodes"),
    path('fetch_season/<int:id>/<int:num>/', views.fetch_season, name="fetch_season"),
]
