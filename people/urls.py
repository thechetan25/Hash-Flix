from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>/',views.person_view,name="person-detail")
]
