from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    PostList, PostDetail, PostSearch, PostCreate, PostUpdate, PostDelete, CategoryList, became_author,
    BaseRegisterView, subscribe)


urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('news/create/', PostCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('articles/create/', PostCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='articles_edit'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
    path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
    path('signup/', BaseRegisterView.as_view(template_name='sign/signup.html'), name='signup'),
    path('upgrade/', became_author, name='became_author'),
    path('categories/<int:pk>/', CategoryList.as_view(), name='category_list'),
    path('categories/<int:pk>/subscriber/', subscribe, name='subscribe'),
]