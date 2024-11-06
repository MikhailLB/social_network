from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView

from humster.forms import AddPostForm, UploadFileForm
from humster.models import Humster, Category, tagPost, UploadFiles

import uuid

from humster.utils import DataMixin


# def handle_uploaded_file(f):
#     with open(f"uploads/{uuid.uuid1()}.jpg", "wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)


# def main(request):
#     posts = Humster.published.all().select_related('cat')
#     data = {
#         'title': 'main page',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': 0,
#     }
#     return render(request, 'humster/index.html', context=data)
# def add_par(request):
#
#     if request.method == "POST":
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#
#
#     else:
#         form = AddPostForm
#
#     data = {
#         'title': "Add paragraph",
#         'menu': menu,
#         'form': form,
#     }
#     return render(request, 'humster/add_par.html', context=data)
#def about(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             # handle_uploaded_file(form.cleaned_data['file'])
#             fp = UploadFiles(file=form.cleaned_data['file'])
#             fp.save()
#     else:
#         form = UploadFileForm()
#     return render(request, 'humster/about.html', {'title': 'about site', 'form': form})
# class AddPage(FormView):
#     form_class = AddPostForm
#     template_name = 'humster/add_par'
#     success_url = reverse_lazy('home')
#     extra_context = {
#         'menu': menu,
#         'title': 'Добавление статьи'
#     }
#
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)

# class AddPage(View):
#     def get(self, request):
#         form = AddPostForm
#         data = {
#             'title': "Add paragraph",
#             'menu': menu,
#             'form': form,
#         }
#         return render(request, 'humster/add_par.html', context=data)
#
#     def post(self, request):
#
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#
#         data = {
#             'title': "Add paragraph",
#             'menu': menu,
#             'form': form,
#         }
#         return render(request, 'humster/add_par.html', context=data)
# def show_post(request, post_slug):
#     post = get_object_or_404(Humster, slug=post_slug)
#
#     data = {
#         'title': post.title,
#         'menu': menu,
#         'post': post,
#         'cat_selected': 1
#     }
#     return render(request, 'humster/post.html', data)

class HumsterHome(DataMixin, ListView):
    template_name = 'humster/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0
    # extra_context = {
    #     'title': 'Главная',
    #     'menu': menu,
    #     'cat_selected': 0,
    # }

    def get_queryset(self):
        return Humster.published.all().select_related('cat')

@login_required
def about(request):
    contact_list = Humster.published.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'humster/about.html', {'title': 'about site', 'page_obj': page_obj})

def pagenotfound(request, exception):
    return HttpResponseNotFound('ERROR 404 PAGE NOT FOUND</h1>')


class AddPage(LoginRequiredMixin,DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'humster/add_par.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавление статьи'
    login_url = '/users/login'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)
class UpdatePage(DataMixin, UpdateView):
    model = Humster
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'humster/add_par.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'


def take_away(request):
    data = {
        'title': "take_away",
        #'menu': menu,
    }
    return render(request, 'humster/take_away.html', context=data)

def sign_in(request):
    return HttpResponse(f'Sign In')

def servererror(request):
    return HttpResponseServerError('Server Error!')


class HumsterCategory(DataMixin, ListView):
    template_name = 'humster/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Humster.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context, title='Категория - ' + cat.name, cat_selected=cat.pk,)

class HumsterShowTagPostList(DataMixin, ListView):
    template_name = 'humster/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Humster.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = tagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег: ' + tag.tag)


class ShowPost(DataMixin, DetailView):
    context_object_name = 'post'
    template_name = 'humster/post.html'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Humster.published, slug=self.kwargs[self.slug_url_kwarg])