from django.contrib import admin
from .models import Categories, Post, News, Author, Reply

admin.site.register(Categories)
admin.site.register(Post)
admin.site.register(News)
admin.site.register(Author)
admin.site.register(Reply)