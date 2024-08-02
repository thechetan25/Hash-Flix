from django.shortcuts import render
import requests
import concurrent.futures
from ratelimit import sleep_and_retry, limits
from django.http import JsonResponse

# Create your views here.
api_key = "825f1726a0ab3395cd85750a10c213ef"

pop_url = f'https://api.themoviedb.org/3/trending/tv/day'
gen_url = f'https://api.themoviedb.org/3/genre/tv/list'
air_url = f'https://api.themoviedb.org/3/tv/airing_today'
on_air_url = f'https://api.themoviedb.org/3/tv/on_the_air'
tpr_url = f'https://api.themoviedb.org/3/tv/top_rated'
tv_daily_url = f'https://api.themoviedb.org/3/trending/tv/day'

urls = [pop_url, gen_url, air_url, on_air_url, tpr_url, tv_daily_url]

params = {
    'api_key': api_key,
    'language': 'en-US',
    'region': 'IN',
    'page': 1
}

@sleep_and_retry
@limits(calls=3, period=1)
def fetch_results(url):
    res = requests.get(url, params=params)
    res.raise_for_status()  # Raise an error for bad status codes
    return res.json()

@sleep_and_retry
@limits(calls=3, period=1)
def fetch_logo(tv_id):
    imgs_url = f'https://api.themoviedb.org/3/tv/{tv_id}/images'
    params = {'api_key': api_key}
    img = requests.get(imgs_url, params=params).json().get('logos', [])

    for i in img:
        if i["iso_639_1"] == "en" and i["file_path"].endswith(".png"):
            return i["file_path"]
    for i in img:
        if i["iso_639_1"] == "en":
            return i["file_path"]
    return None

def home_view(request):
    results = {}
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_url = {executor.submit(fetch_results, url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                results[url] = future.result()
            except Exception as exc:
                results[url] = str(type(exc))

    gen_res = results.get(gen_url, {}).get('genres', [])
    genres = {genre["id"]: genre["name"] for genre in gen_res}

    pop_results = results.get(pop_url, {}).get('results', [])[:5]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_logo = {executor.submit(fetch_logo, movie["id"]): movie for movie in pop_results}
        for future in concurrent.futures.as_completed(future_to_logo):
            movie = future_to_logo[future]
            try:
                movie["logo"] = future.result()
            except Exception as exc:
                movie["logo"] = None

    context = {
        "resp": pop_results,
        "genres": genres,
        "air": results.get(air_url, {}).get('results', []),
        "onair": results.get(on_air_url, {}).get('results', []),
        "top": results.get(tpr_url, {}).get('results', []),
        "tvd": results.get(tv_daily_url, {}).get('results', [])
    }

    return render(request, "Tvshows/tv_home.html", context)

@sleep_and_retry
@limits(calls=3, period=1)
def fetch_providers(tv_id):
    providers_url = f'https://api.themoviedb.org/3/tv/{tv_id}/watch/providers'
    res = fetch_results(providers_url)
    return res.get('results', {}).get('IN', {}).get('flatrate', [])


@sleep_and_retry
@limits(calls=3, period=1)
def fetch_credits(tv_id):
    credits_url = f'https://api.themoviedb.org/3/tv/{tv_id}/credits'
    res = requests.get(credits_url, params=params).json()
    cast_res = res.get('cast', [])
    crew_res = res.get('crew', [])

    director = next((member for member in crew_res if member.get('job') == 'Director'), None)
    actor_list = [member for member in cast_res if member.get('known_for_department') == 'Acting']
    top_actors = actor_list[:3]

    return [director, top_actors, cast_res, crew_res]

def tv_view(request, media, id):
    if media == "tv":
        test_url = f'https://api.themoviedb.org/3/tv/{id}'
        videos_url = f'https://api.themoviedb.org/3/tv/{id}/videos'
    else:
        test_url = f'https://api.themoviedb.org/3/movie/{id}'
        videos_url = f'https://api.themoviedb.org/3/movie/{id}/videos'
    
    recomendations_url = f'https://api.themoviedb.org/3/tv/{id}/recommendations'

    urls = [test_url, videos_url, recomendations_url]

    results = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_url = {executor.submit(fetch_results, url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                results[url] = future.result()
            except Exception as exc:
                results[url] = str(type(exc))

    test_res = results.get(test_url, {})
    video_res = results.get(videos_url, {}).get('results', [])
    
    gen_res = fetch_results(gen_url).get('genres', [])
    genres = {genre["id"]: genre["name"] for genre in gen_res}
    recomend_res = results.get(recomendations_url, {}).get('results', [])

    first_air_date = test_res.get('first_air_date', 'N/A')
    last_air_date = test_res.get('last_air_date', 'N/A')

    logo = fetch_logo(id)
    cast = fetch_credits(id)
    providers = fetch_providers(id)

    video_key = None
    for video in video_res:
        if video["iso_639_1"] == "en" and video["type"] == "Trailer":
            video_key = video["key"]
            break

    context = {
        "test": test_res,
        "logo": logo,
        "genres": genres,
        "key": video_key,
        "media": media,
        "director": cast[0],
        "actors": cast[1],
        "cast": cast[2],
        "crew": cast[3],
        "release": first_air_date,
        "last_date": last_air_date,
        "providers": providers,
        "recomendations": recomend_res,
        "videos": video_res[:5],
    }

    return render(request, "Tvshows/tv_view.html", context)

def season_info(request,id):
    
    series_url =f'https://api.themoviedb.org/3/tv/{id}'
    info_url=f'https://api.themoviedb.org/3/tv/{id}/season/1'
    
    series_res =requests.get(series_url,params).json()
    res =requests.get(info_url,params).json().get('episodes',[])
    
    context ={
        "episodes":res,
        "series":series_res
    }
    
    return render(request , 'Tvshows/season_info.html' ,context)


def fetch_season(request, id, num):
    params = {
        'api_key': api_key,
        'language': 'en-US',
    }
    info_url = f'https://api.themoviedb.org/3/tv/{id}/season/{num}'
    
    
    res = requests.get(info_url, params=params)
    episodes = res.json().get('episodes', [])
    return JsonResponse(data={'episodes': episodes}, status=200)