from django.shortcuts import render, redirect
import os, json
from .models import Podcasts
from django.db.models import F
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import requests
from bs4 import BeautifulSoup
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

# Create your views here.
def home_view(request):
    
    return render(request, 'home.html')

def list_view(request):
    p_set = Podcasts.objects.order_by(F('id').desc())
    paginator = Paginator(p_set, 15)
    page = request.GET.get('page')
    items = paginator.get_page(page)
    context = {
        'items': items
    }
    return render(request, 'list.html', context)

def podcast_view(request):
    pid = request.GET.get('id')
    podcast = get_object_or_404(Podcasts, id=pid)
    context = {
        'item': podcast
    }
    return render(request, 'podcast.html', context)

def jump_view(request):
    if request.method == 'POST':
        pid = request.POST.get('pid')
        return redirect('/podcast?id='+pid)
    else:
        return render(request, 'jump.html')

def search(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query.isdigit():
            result = Podcasts.objects.filter(id__contains=query).order_by(F('id').desc())    
        else:
            result = Podcasts.objects.filter(title__contains=query).order_by(F('id').desc())
        context = {
            'items': result
        }
        return render(request, 'list.html', context)

def add_from_url(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        p = get_podcast_from_url(url)
        p.save()
        return redirect('list')
    else:
        return render(request, 'add_from_url.html')

def get_podcast_page_all_link():
    r = requests.get('https://www.scientificamerican.com/podcasts/')
    soup = BeautifulSoup(r.text, 'html.parser')
    atags = soup.select('a')
    result = []
    for tag in atags:
        link = tag.get('href')
        if link and link.startswith('https://www.scientificamerican.com/podcast/episode/'):
            result.insert(0, link)
    return result

def get_podcast_from_url(url):
    r = requests.get(url.strip())
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        tag = soup.find('h3', {"itemprop": "name", "class": True})
        title = tag.text
        tag = soup.find('span', {'itemprop': 'datePublished'})
        date = tag.text
        tag = soup.find('source', {"type": "audio/mp3", "src": True})
        audio = tag.get("src")
        tag = soup.find('img', {"itemprop": "image", "src": True})
        if tag != None:
            img = tag.get("src")
        else:
            img = ''
        tag = soup.find('div', {"class": "transcript__inner"})
        transcript = ''
        if tag != None:
            for p in tag.find_all('p'):
                transcript += str(p)
        p = Podcasts(
            title=title,
            url=url,
            date=date,
            audio=audio,
            img=img,
            transcript=transcript
        )
        return p
    except AttributeError as ae:
        pass

def refresh(request):
    arr = []
    for link in get_podcast_page_all_link():
        result = Podcasts.objects.filter(url=link)
        if len(result) == 0:
            p = get_podcast_from_url(link)
            p.save()
            arr.append(link)
        else:
            pass
    result = {
        'msg': 'ok',
        'adding_links': arr
    }
    return JsonResponse(result)