from django.shortcuts import render
from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy



class PostList(ListView):
    model = Post
    ordering = 'timing'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['timing'] = datetime.utcnow()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'news_1.html'
    context_object_name = 'news_1'
    pk_url_kwarg = ''

class SearchList(ListView):
    model = Post
    filterset_class = PostFilter
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'create.html'
    context_object_name = 'post_create'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/news/article/create/':
            post.type = 'A'
        post.save()
        return super().form_valid(form)

class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'edit.html'
    context_object_name = 'post_edit'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class PostDelete(DeleteView):
    model = Post
    template_name = 'delete.html'
    context_object_name = 'post_delete'
    success_url = reverse_lazy('NEWS')
# Create your views here.
