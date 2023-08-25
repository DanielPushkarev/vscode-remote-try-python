from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = Post.objects.filter(post_author=self).aggregate(pr=Coalesce(Sum('rating'), 0))['pr']
        comments_rating = Comment.objects.filter(user_comment=self.user).aggregate(cr=Coalesce(Sum('rating'), 0))['cr']
        comments_posts_rating = Comment.objects.filter(comments__post_author=self).aggregate(pcr=Coalesce(Sum('rating'),
                                                                                                          0))['pcr']

        print(posts_rating)
        print('----------------')
        print(comments_rating)
        print('----------------')
        print(comments_posts_rating)

        self.rating = posts_rating * 3 + comments_rating + comments_posts_rating
        self.save()


class Category(models.Model):
    theme = models.CharField(max_length=150, unique=True)
    subscribers = models.ManyToManyField(User, through='CategorySubscribers')

    def __str__(self):
        return self.theme


class CategorySubscribers(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE)


class Post(models.Model):
    news = 'NW'
    article = 'AR'

    CHAPTER = [
        (news, 'Новость'),
        (article, 'Статья')
    ]

    post_type = models.CharField(max_length=2, choices=CHAPTER, default=news)
    post_time = models.DateTimeField(auto_now_add=True)
    headline = models.CharField(max_length=255)
    article_text = models.TextField()
    rating = models.IntegerField(default=0)

    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        beginning = self.article_text[0:124] + '...'
        return beginning


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_text = models.TextField()
    comment_time = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(default=0)

    comments = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()