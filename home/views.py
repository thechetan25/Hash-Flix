from django.shortcuts import render
import requests
from io import BytesIO
from django import template
from django.views.generic import TemplateView
import concurrent.futures
from ratelimit import sleep_and_retry,limits


# Create your views here.
api_key ="825f1726a0ab3395cd85750a10c213ef"

pop_url=f'https://api.themoviedb.org/3/trending/all/day'
gen_url=f'https://api.themoviedb.org/3/genre/movie/list'
tv_gen_url =f'https://api.themoviedb.org/3/genre/tv/list'
top_url=f'https://api.themoviedb.org/3/trending/movie/day'
up_url=f'https://api.themoviedb.org/3/movie/upcoming'
wpop_url=f'https://api.themoviedb.org/3/trending/movie/week'
tv_top_url=f'https://api.themoviedb.org/3/tv/top_rated'
all_url=f'https://api.themoviedb.org/3/trending/all/day'
pop_shows=f'https://api.themoviedb.org/3/tv/popular'
people_url=f'https://api.themoviedb.org/3/person/popular'

urls =[pop_url,gen_url,tv_gen_url,top_url,up_url,wpop_url,tv_top_url,all_url,pop_shows,people_url]

@sleep_and_retry
@limits(calls=3, period=1)
def fetch_results(url):
    params = {
    'api_key': api_key,
    'language':'en',
    'region': 'IN',
    'page': 1 
    }
    if url in [gen_url,tv_gen_url]:
        res=requests.get(url,params).json().get('genres',[])
    else:
        res=requests.get(url,params).json().get('results',[])
    return res

@sleep_and_retry
@limits(calls=3, period=1)
def fetch_logo(movie_id,media):
    
    if media!="tv":
        imgs_url =f' https://api.themoviedb.org/3/movie/{movie_id}/images'
    else:
        imgs_url =f' https://api.themoviedb.org/3/tv/{movie_id}/images'
    
    img =requests.get(imgs_url,{"movie_id":movie_id, 'api_key': api_key}).json().get('logos',[])
    
    for i in img:
        if i["iso_639_1"]=="en" and i["file_path"].endswith(".png"):
            logo =i["file_path"]
            return logo

def home_view(request):
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_urls ={executor.submit(fetch_results,url):url for url in urls}
        results ={}
        
    for future in concurrent.futures.as_completed(future_to_urls):
        url =future_to_urls[future]
        
        results[url]=future.result()
        
        
    gen_res =results.get(gen_url,[])
    genres = {genre["id"]: genre["name"] for genre in gen_res}
    
    tv_gen_res =results.get(tv_gen_url,[])
    for genre in tv_gen_res:
        if genre['id'] not in genres:
            genres[genre['id']]=genre['name']
    
    pop_results = results.get(pop_url, [])[:5]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_logo ={executor.submit(fetch_logo, movie["id"], movie["media_type"]): movie for movie in pop_results}

        for future in concurrent.futures.as_completed(future_to_logo):
            movie=future_to_logo[future]
            movie["logo"] =fetch_logo(movie["id"],movie["media_type"])
        
        
    context = {
        "resp": pop_results,
        "genres": genres,
        "top": results.get(top_url, []),
        "up": results.get(up_url, []),
        "wpop": results.get(wpop_url, []),
        "tv_top": results.get(tv_top_url, []),
        "all_trend": results.get(all_url, []),
        "pop_shows": results.get(pop_shows, []),
        "people":results.get(people_url, [])
    }

    return render(request, "home/home.html", context)
