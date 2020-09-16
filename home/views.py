from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from . import models
from .forms import RegisterForm, LoginForm, UploadForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
import re
from django.utils.datastructures import MultiValueDict
from django.forms.fields import IntegerField

# Create your views here.
def get_mangatype():
    mangatype = models.MangaType.objects.filter()
    return mangatype

def get_chap(manga_name, chap):
    content = models.ChapInfo.objects.filter(name=manga_name,chap=chap)
    if len(content) > 0:
        return True
    return False

def index(request):
    data = models.MangaInfo.objects.order_by('time_up')
    return render(request,'home/index.html',{'mangainfo':data, 'mangatype':get_mangatype()})

def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            auth_login(request,user)
            return HttpResponseRedirect('/')
    return render(request,'home/register.html',{'form':form, 'mangatype':get_mangatype()})

def mangainfo(request, manga_name):
    try:
        manga = models.MangaInfo.objects.get(name=manga_name)
    except models.MangaInfo.DoesNotExist:
        return error(request,"error")
    listchap = [chap for chap in range(manga.current_chap+1) if get_chap(manga_name,chap)]
    return render(request, 'home/mangainfo.html',{'manga':manga,"listchap":listchap, 'mangatype':get_mangatype()})

def mangatype(request, manga_type):
    try:
        mangatype = models.MangaType.objects.get(name=manga_type)
    except models.MangaType.DoesNotExist:
        return error(request,'error')
    mangas = models.MangaInfo.objects.filter(manga_type=mangatype)
    return render(request, 'home/mangatype.html',{'mangas':mangas, 'mangatype':get_mangatype()})

def content(request, manga_name, chap):
    try:
        content = models.ChapInfo.objects.filter(name=manga_name,chap=chap)
        curchap = models.MangaInfo.objects.get(name=manga_name).current_chap
    except models.MangaInfo.DoesNotExist:
        return error(request,'error')
    listchap = [chap for chap in range(curchap+1) if get_chap(manga_name,chap)]
    if len(content) == 0:
        content = [models.ChapInfo(name=manga_name,chap=chap)]
        return render(request, 'home/mangacontent.html',{'content':content,'mangatype':get_mangatype(),"listchap":listchap,'error':"Can't load this chap"})
    return render(request, 'home/mangacontent.html',{'content':content,"listchap":listchap,'mangatype':get_mangatype()})

def login(request):
    form = LoginForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            auth_login(request,user)
            return HttpResponseRedirect('/')
        else:
            return render(request,'home/login.html',{'error':'Your username or password is incorrect!', 'mangatype':get_mangatype()})
    return render(request,'home/login.html',{'form':form,'error':'', 'mangatype':get_mangatype()})

def addchap(request, manga_name):
    form = UploadForm()
    if request.method == 'POST':
        manga = models.MangaInfo.objects.get(name=manga_name)
        requestchap = int(request.POST['chap'])
        if requestchap > manga.current_chap:
            manga.current_chap = requestchap
            manga.save()
        for FILES in request.FILES.getlist('content'):
            files = MultiValueDict({'content':[FILES]})
            form = UploadForm(request.POST, files)
            if form.is_valid():
                form.save()
        return render(request,'home/addchap.html',{'form':form,'manganame':manga_name})
    return render(request,'home/addchap.html',{'form':form, 'manganame':manga_name})

def search(request, text):
    data = []
    mangas = models.MangaInfo.objects.order_by('time_up')
    for manga in mangas:
        if manga.name.lower().replace(" ","").find(text.lower()) != -1:
            data.append(manga)
    if len(data) == 0:
        data = mangas
    return render(request,'home/index.html',{'mangainfo':data, 'mangatype':get_mangatype()})

def error(request, exception):
    return render(request, 'home/index.html',{'error':exception})
