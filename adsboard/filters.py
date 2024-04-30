from django.utils.translation import gettext_lazy as _
from django_filters import FilterSet, ModelChoiceFilter, CharFilter, DateTimeFilter
from django.utils.translation import pgettext_lazy
from django import forms
from .models import Post, Category, Comment
from django.db.models import Q


class PostFilter(FilterSet):
    category = ModelChoiceFilter(
        field_name='postcategory__category',
        queryset=Category.objects.all(),
        label=_('Category'),
        empty_label=_('all'),
        to_field_name='name'
    )
    text = CharFilter(method='filter_text', label=_('Search'))

    def filter_text(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) | Q(content__icontains=value)
        )

    class Meta:
        model = Post
        fields = {
            'category': ['exact'],
        }


class CommentFilter(FilterSet):
    added_after = DateTimeFilter(
        field_name='post_time',
        lookup_expr='gt',
        widget=forms.DateTimeInput(
            format='%Y-%m-%d',
            attrs={'type':'date'},
        ),
        label=pgettext_lazy('post_time', 'Posted after')
    )

    class Meta:
        model = Comment
        fields = {
            'author__username': ['contains'],
            'post__title': ['icontains'],
            'status': ['exact']
        }
