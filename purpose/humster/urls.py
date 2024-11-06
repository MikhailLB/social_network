from django.urls import path, re_path, register_converter
from . import converters
from .views import *

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', HumsterHome.as_view(), name='home'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('about/', about, name='about'),
    path('add_par/', AddPage.as_view(), name='add_par'),
    path('take_away/', take_away, name='take_away'),
    path('sign_in/', sign_in, name='sign_in'),
    path('category/<slug:cat_slug>/', HumsterCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', HumsterShowTagPostList.as_view(), name='tag'),
    path('edit/<slug:slug>/', UpdatePage.as_view(),  name='edit_page'),
]

