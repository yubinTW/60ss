from django.shortcuts import render, redirect
import os, json
from .models import Podcasts
from django.db.models import F
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import requests
from bs4 import BeautifulSoup
from django.shortcuts import get_object_or_404

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
        r = requests.get(url.strip())
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            tag = soup.find('h3', {"itemprop": "name", "class": True})
            title = tag.text
            # print(title)
            tag = soup.find('span', {'itemprop': 'datePublished'})
            date = tag.text
            # print(date)
            tag = soup.find('source', {"type": "audio/mp3", "src": True})
            audio = tag.get("src")
            # print(audio)
            tag = soup.find('img', {"itemprop": "image", "src": True})
            if tag != None:
                img = tag.get("src")
            else:
                img = ''
            # print(img)
            tag = soup.find('div', {"class": "transcript__inner"})
            transcript = ''
            if tag != None:
                for p in tag.find_all('p'):
                    transcript += str(p)
            # print(transcript)
            p = Podcasts(
                title=title,
                url=url,
                date=date,
                audio=audio,
                img=img,
                transcript=transcript
            )
            p.save()
        except AttributeError as ae:
            pass
        return redirect('list')
    else:
        return render(request, 'add_from_url.html')

def read_data_from_json(request):
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'static/data.json')
    f = open(file_path, 'r')
    arr = json.loads(f.read())
    print(len(arr))
    for i in range(len(arr)-1, -1, -1):
        p = Podcasts()
        p.title = arr[i]['title']
        p.url = arr[i]['url']
        p.audio = arr[i]['audio']
        p.img = arr[i]['img']
        p.transcript = arr[i]['transcript']
        p.date = arr[i]['date']
        try:
            p.save()
        except IntegrityError as ie:
            print(p.title)
            print(ie)
    return redirect('/')