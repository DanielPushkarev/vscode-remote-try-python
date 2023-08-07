from django.core.management.base import BaseCommand, CommandError
from NewsPaper.models import Post, Category

class Command(BaseCommand):
    help = 'Обнуляет все новости или статьи'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('argument', nargs='+', type=int)

    def handle(self, *args, **options):
        self.stdout.readable()
        self.stdout.write('Вы действительно хотите удалить новости или статьи? если Новости то 1,'
                          'если Статьи то 2')
        answer = input()

        if answer not in ('1', '2'):
            self.stdout.write(self.style.ERROR('Отменено'))

        elif answer == '1':
            category = Post.objects.get(name='Новости')
            Category.objects.filter(category=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted all news from category {category.name}'))
            return

        elif answer == '2':
            category = Post.objects.get(name='Статьи')
            Category.objects.filter(category=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted all news from category {category.name}'))
            return

        self.stdout.write(
            self.style.ERROR('Access denied'))