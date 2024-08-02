from django.urls import path
from . import views

urlpatterns = [
    path('',views.movie_homepage,name="movie-page"),
    path('detail/<str:media>/<int:id>/',views.movie_detail,name="movie-detail")
]
