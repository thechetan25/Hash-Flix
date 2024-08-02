from django.shortcuts import render
import requests
from django.conf import settings
from django.http import JsonResponse

api_key ="825f1726a0ab3395cd85750a10c213ef"

def search(request):
    query = request.GET.get('query', '')
    results = []
    if query:
        movie_url = f'https://api.themoviedb.org/3/search/movie'
        tv_url =f'https://api.themoviedb.org/3/search/tv'
        params = {
            'api_key': api_key,
            'query': query,
            'language': 'en-US',
            'page': 1
        }
        movie_response = requests.get(movie_url, params=params)
        tv_response = requests.get(tv_url, params=params)
        if movie_response.status_code == 200:
            data = movie_response.json()
            mv_results = data.get('results', [])
            mv_total_pages =data.get('total_pages','')
            
        if tv_response.status_code == 200:
            data = tv_response.json()
            tv_results = data.get('results', [])
            tv_total_pages =data.get('total_pages','')
            
    return render(request, 'search/search.html', {'movie_results': mv_results, 'query': query , 'mv_total':mv_total_pages, 'tv_results': tv_results , 'tv_total':tv_total_pages})

def mv_search_more(request):
    query = request.GET.get('query', '')
    page = request.GET.get('page', 2)
    results = []
    if query:
        url = 'https://api.themoviedb.org/3/search/movie'
        params = {
            'api_key': api_key,
            'query': query,
            'language': 'en-US',
            'page': page
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
    return JsonResponse({'results': results}, status=200)

def tv_search_more(request):
    query = request.GET.get('query', '')
    page = request.GET.get('page', 2)
    results = []
    if query:
        url = 'https://api.themoviedb.org/3/search/tv'
        params = {
            'api_key': api_key,
            'query': query,
            'language': 'en-US',
            'page': page
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
    return JsonResponse({'results': results}, status=200)
