"""
URL configuration for flix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from home import urls as hurls
from movies import urls as murls
from Tvshows import urls as tvurls
from search import urls as surls
from people import urls as purls
from news import urls as nurls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(hurls)),
    path('movies/',include(murls),name="movies"),
    path('tvshows/',include(tvurls),name="tvshows"),
    path('search/', include(surls)),
    path('person/',include(purls)),
    path('news/',include(nurls))
]
