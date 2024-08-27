from django.shortcuts import render
from django.urls import reverse_lazy
from requests import post
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostFilter
from .forms import PostForm
from django.views.generic import TemplateView



class NewsList(ListView):
    model = Post
    ordering = '-post_time'
    template_name = 'post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_template_names(self):
        if self.request.path == '/news/':
            self.template_name = 'post_list.html'
        elif self.request.path == '/news/search/':
            self.template_name == 'search.html'
        return self.template_name


class NewsDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'


class NewsSearch(ListView):
    model = Post
    ordering = '-post_time'
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'


    def form_valid(self, form):
        post == form.save(commit=False)
        if self.request.path == '/articles/create/':
            post.post_type = 'AR'
        post.save()
        return super().form_valid(form)


class NewsUpdate(UpdateView):
    model = Post
    template_name = 'post_edit.html'



class NewsDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_premium'] = not self.request.user.groups.filter(name='premium').exists()
        return context



