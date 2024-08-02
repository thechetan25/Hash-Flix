from django.shortcuts import render
import requests

# Create your views here.
api_key ="825f1726a0ab3395cd85750a10c213ef"

def person_view(request,id):
    
    params={
        'api_key': api_key
    }
    
    works_url =f'https://api.themoviedb.org/3/person/{id}/combined_credits'
    detail_url =f'https://api.themoviedb.org/3/person/{id}'
    images_url =f'https://api.themoviedb.org/3/person/{id}/images'
    
    images =requests.get(images_url,params).json().get('profiles',[])
    details =requests.get(detail_url,params).json()
    acted =requests.get(works_url,params).json().get('cast',[])
    crewed =requests.get(works_url,params).json().get('crew',[])
    
    context ={"person":details,
              "images":images[1:],
              "acted":acted,
              "crew":crewed
             }
    return render(request,'people/view.html',context)
