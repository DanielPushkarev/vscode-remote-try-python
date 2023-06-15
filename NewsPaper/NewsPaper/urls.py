"""
URL configuration for NewsPaper project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import PostList, PostDetail, SearchList, PostCreate, PostDelete, PostUpdate


urlpatterns = [
   path('', PostList.as_view()),
   path('<int:pk>/', PostDetail.as_view()),
   path('search/', SearchList.as_view()),
   path('create/', PostCreate.as_view()),
   path('<int:pk>/edit/', PostUpdate.as_view()),
   path('<int:pk>/delete/', PostDelete.as_view()),
   path('article/create/', PostCreate.as_view()),
   path('article/<int:pk>/edit/', PostUpdate.as_view()),
   path('article/<int:pk>/delete/', PostDelete.as_view()),
]
