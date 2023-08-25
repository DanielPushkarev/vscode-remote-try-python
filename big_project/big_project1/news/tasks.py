import datetime

from django.conf import settings

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from news.models import Post, Category


def weekly_notify():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    this_week_posts = Post.objects.filter(post_time__gt=last_week)
    for category in Category.objects.all():
        post_list = this_week_posts.filter(post_category=category)
        if post_list:
            subscribers = category.subscribers.values('username', 'email')
            recipients = []
            for subscriber in subscribers:
                recipients.append(subscriber['email'])

            html_content = render_to_string(
                'news/daily_news.html',
                {
                    'link': f'{settings.SITE_URL}posts/',
                }
            )

            msg = EmailMultiAlternatives(
                subject='Статьи за неделю',
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=recipients,
            )

            msg.attach_alternative(html_content, 'text/html')
            msg.send()