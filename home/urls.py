from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

# Create your tests here.
app_name = "home"
urlpatterns = [
    path('', views.index, name="index"),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page="/"),name='logout'),
    path('mangainfo/<str:manga_name>',views.mangainfo,name='mangainfo'),
    path('mangatype/<str:manga_type>',views.mangatype,name='mangatype'),
    path('content/<str:manga_name>/chap-<int:chap>',views.content,name="mangacontent"),
    path('addchap/<str:manga_name>',views.addchap,name='addchap'),
    path('search/<str:text>',views.search,name='search'),
]
