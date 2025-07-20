from django.utils import timezone
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from utils.pagination import StandardResultsSetPagination
from news.models import News
from news.serializers.news import NewsListSerializer
from news.serializers.news import NewsCreateSerializer
from news.filters import NewsFilter


class NewsListViewSet(ListModelMixin, GenericViewSet):
    serializer_class = NewsListSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = NewsFilter
    
    def get_queryset(self):
        now = timezone.now()
        return (
            News.objects.filter(published_at__isnull=False)
            .prefetch_related('tags')
            .order_by('-published_at')  
        )
    

class NewsCreateViewSet(CreateModelMixin, GenericViewSet):
    queryset = News.objects.all()
    serializer_class = NewsCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(published_at=timezone.now())
