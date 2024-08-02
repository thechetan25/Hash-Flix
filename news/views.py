from django.shortcuts import render
from django.http import JsonResponse
from newsapi import NewsApiClient
import logging

logger = logging.getLogger(__name__)

newsapi = NewsApiClient(api_key='7088c9efde1441038307dae2e83c8a46')

def homepage(request):
    top_headlines = newsapi.get_top_headlines(
        category='sports',
        language='en',
        country='in'
    ) 


    sources = newsapi.get_sources(category='sports')

    print(top_headlines['totalResults'])
    context = {
        "articles": top_headlines['articles'][:30] ,
        "sources": sources["sources"]
    }
    
    return render(request, 'news/news.html', context)

