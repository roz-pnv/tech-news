import django_filters
from django_filters import rest_framework as filters
from django.db.models import Q

from news.models import News


class NewsFilter(filters.FilterSet):
    tags = django_filters.CharFilter(method='filter_by_tags', label='Tag Name(s)')
    contains = django_filters.CharFilter(method='filter_contains', label='Contains (in title or body)')
    not_contains = django_filters.CharFilter(method='filter_not_contains', label='Does NOT Contain (in title or body)')

    class Meta:
        model = News
        fields = []

    def filter_by_tags(self, queryset, name, value):
        tag_names = [tag.strip() for tag in value.split(',')]
        return queryset.filter(tags__name__in=tag_names).distinct()

    def filter_contains(self, queryset, name, value):
        phrases = [phrase.strip() for phrase in value.split(',')]
        for phrase in phrases:
            queryset = queryset.filter(
                Q(title__icontains=phrase) | Q(body__icontains=phrase)
            )
        return queryset

    def filter_not_contains(self, queryset, name, value):
        phrases = [phrase.strip() for phrase in value.split(',')]
        for phrase in phrases:
            queryset = queryset.exclude(
                Q(title__icontains=phrase) | Q(body__icontains=phrase)
            )
        return queryset
