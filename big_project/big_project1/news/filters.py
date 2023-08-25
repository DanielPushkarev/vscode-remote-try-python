from django_filters import FilterSet, DateFilter, CharFilter, ModelChoiceFilter
from .models import Post, Author
from django import forms


class PostFilter(FilterSet):
    headline = CharFilter(lookup_expr='icontains', label='По заголовку')
    post_author = ModelChoiceFilter(
        queryset=Author.objects.all(),
        label='По имени автора',
        empty_label='Любой'
    )
    post_time = DateFilter(
        field_name='post_time',
        lookup_expr='gt',
        label='Позже указанной даты',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = ['headline', 'post_author', 'post_time']