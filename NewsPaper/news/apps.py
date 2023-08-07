from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        from .signals import send_notifications, notify_about_new_post

red = redis.Redis(
    host='redis-19198.c258.us-east-1-4.ec2.cloud.redislabs.com',
    port=19198,
    password='QqT6z8XsLUIRKIf8KSdaeU6fvFsLJxGO'
)
