from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.views import View

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import Appointment
# from django.core.mail import send_mail
from django.core.mail import mail_admins
from django.views.generic import TemplateView



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

class NewsDetail(LoginRequiredMixin, DetailView):
    model = Post
    ordering = '-sort_date_of_publication'
    template_name = 'flatpages/NEW.html'
    context_object_name = 'NEW'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_info'] = 'Next information later'
        return context

class NewCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('simpleapp.add_news')
    form_class = PostForm
    model = Post
    template_name = 'flatpages/NEW_edit.html'

    def form_valid(self, form):
        new = form.save(commit=False)
        if self.request.path == '/post/new/create/':
            new.news_category_id = 1
        elif self.request.path == '/post/article/create/':
            new.news_category_id = 2
        new.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

class NewDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('simpleapp.delete_news')
    model = Post
    template_name = 'flatpages/new_delete.html'
    success_url = reverse_lazy('new_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect('/profile/')

def profile(request):
    context = {'is_not_author': not request.user.groups.filter(name='authors').exists()}
    return render(request, 'flatpages/User_profile.html', context)

class AppointmentView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'flatpages/make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()

        mail_admins(
            subject=f'{appointment.client_name} {appointment.date.strftime("%d %m %Y")}',
            message=appointment.message,
        )

        return redirect('/appointment/')

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

def subscribe(request, pk):
    user = request.user
    category = Post.objects.get(id=pk)
    category.subscribers.add(user)
    message = 'You subscribed to the category: '
    return render(request, 'flatpages/subscribe.html', {'category': category, 'message': message})

def unsubscribe(request, pk):
    user = request.user
    category = Post.objects.get(id=pk)
    category.subscribers.remove(user)
    message = 'You unsubscribed from category: '
    return render(request, 'flatpages/subscribe.html', {'category': category, 'message': message})

class CategoryListView(ListView):
    model = Post
    template_name = 'flatpages/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.news_category = get_object_or_404(Post, id=self.kwargs['pk'])
        queryset = Post.objects.filter(news_category=self.news_category).order_by('-sort_date_of_publication')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.news_category.subscribers.all()
        context['is_subscriber'] = self.request.user in self.news_category.subscribers.all()
        context['category'] = self.news_category
        return context
# Create your views here.
