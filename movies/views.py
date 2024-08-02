from django.shortcuts import render
import requests
import concurrent.futures
from ratelimit import sleep_and_retry, limits

api_key = "825f1726a0ab3395cd85750a10c213ef"


wpop_url = f'https://api.themoviedb.org/3/trending/movie/week'
pop_url = f'https://api.themoviedb.org/3/movie/popular'
top_url = f'https://api.themoviedb.org/3/movie/top_rated'
up_url = f'https://api.themoviedb.org/3/movie/upcoming'
gen_url = f'https://api.themoviedb.org/3/genre/movie/list'

urls = [wpop_url, pop_url, top_url, up_url]

params = {
    'api_key': api_key,
    'language': 'en-US',
    'region': 'IN',
    'page': 1
}

@sleep_and_retry
@limits(calls=3, period=1)
def fetch_results(url):
    res = requests.get(url, params=params).json()
    return res

@sleep_and_retry
@limits(calls=3, period=1)
def fetch_collection(id):
    collection_url=f'https://api.themoviedb.org/3/collection/{id}'
    res = requests.get(collection_url, params=params).json()
    return res

@sleep_and_retry
@limits(calls=3, period=1)
def fetch_logo(movie_id, media):
    if media != "tv":
        imgs_url = f'https://api.themoviedb.org/3/movie/{movie_id}/images'
    else:
        imgs_url = f'https://api.themoviedb.org/3/tv/{movie_id}/images'
    
    try:
        img = requests.get(imgs_url, params={'api_key': api_key}).json().get('logos', [])
        for i in img:
            if i["iso_639_1"] == "en" and i["file_path"].endswith(".png"):
                return i["file_path"]
    except requests.RequestException as e:
        print(f"Error fetching images for {movie_id}: {e}")
    return None

@sleep_and_retry
@limits(calls=3, period=1)
def fetch_credits(id):
    
    credits =f'https://api.themoviedb.org/3/movie/{id}/credits'
    cast_res =requests.get(credits,params).json().get('cast',[])
    crew_res =requests.get(credits,params).json().get('crew',[])
    
    
    for member in crew_res:
        if member.get('job') == 'Director':
            director = member
            break

    actor_list = [member for member in cast_res if member.get('known_for_department') == 'Acting']
    top_actors = actor_list[:3]

    
    return [director,top_actors,cast_res,crew_res]

@sleep_and_retry
@limits(calls=3, period=1)
def fetch_providers(id):
    
    providers_url =f'https://api.themoviedb.org/3/movie/{id}/watch/providers'
    providers_res =fetch_results(providers_url).get('results',{}).get('IN',{}).get('flatrate',[])

    return providers_res

def movie_homepage(request):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures_to_url = {executor.submit(fetch_results, url): url for url in urls}
        results = {url: future.result().get('results', []) for future, url in futures_to_url.items()}
    
    wepo = results.get(wpop_url, [])[:5]
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_logo = {executor.submit(fetch_logo, movie["id"], "movie"): movie for movie in wepo}
        for future in concurrent.futures.as_completed(future_to_logo):
            movie = future_to_logo[future]
            movie["logo"] = future.result()
    
    gen_res = fetch_results(gen_url).get('genres', [])
    genres = {genre["id"]: genre["name"] for genre in gen_res}
    
    return render(request, "movies/home.html", {
        "wepo": wepo,
        "wepop":results.get(wpop_url, []),
        "genres": genres,
        "popo": results.get(pop_url, []),
        "top": results.get(top_url, []),
        "up": results.get(up_url, [])
    })

def movie_detail(request, media, id):
    if media == "tv":
        test_url = f'https://api.themoviedb.org/3/tv/{id}'
        videos_url = f'https://api.themoviedb.org/3/tv/{id}/videos'
    else:
        test_url = f'https://api.themoviedb.org/3/movie/{id}'
        videos_url = f'https://api.themoviedb.org/3/movie/{id}/videos'
        
    release_url =f'https://api.themoviedb.org/3/movie/{id}/release_dates'
    recomendations =f'https://api.themoviedb.org/3/movie/{id}/recommendations'
    
    urls = [test_url, videos_url,release_url,recomendations]
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_url = {executor.submit(fetch_results, url): url for url in urls}
        results = {url: future.result() for future, url in future_to_url.items()}
    
    test_res = results.get(test_url, {})
    video_res = results.get(videos_url, {}).get('results', [])
    
    gen_res = fetch_results(gen_url).get('genres', [])
    genres = {genre["id"]: genre["name"] for genre in gen_res}
    recomend_res=results.get(recomendations,{}).get('results', [])
    release_res =results[release_url].get('results', [])
    
    release_date ="Not Anounced"
    
    for i in release_res:
        if i["iso_3166_1"]=="IN" or i["iso_3166_1"]=="US":
            dates =i["release_dates"]
            
    for i in dates:
        if i["type"] == 3 or  i["type"] == 2:
            release_date =i["release_date"][:10]
            break
    
    logo = fetch_logo(id, media)
    cast =fetch_credits(id)
    providers =fetch_providers(id)
    
    video_key = None
    for video in video_res:
        if video["iso_639_1"] == "en" and video["type"] == "Trailer":
            video_key = video["key"]
            break
      
    collection = None
    if test_res["belongs_to_collection"] != None:
        collection_id = test_res["belongs_to_collection"]["id"]
        collection = fetch_collection(collection_id)
    
    context = {
        "test": test_res,
        "logo": logo,
        "genres": genres,
        "key": video_key,
        "media":media,
        "director":cast[0],
        "actors":cast[1],
        "cast":cast[2],
        "crew":cast[3],
        "release":release_date,
        "providers":providers,
        "recomendations":recomend_res,
        "videos":video_res[:5],
        "collection":collection
        
    }
    
    return render(request, "movies/movie_view.html", context)
