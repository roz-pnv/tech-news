from django.utils import timezone
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny

from utils.pagination import StandardResultsSetPagination
from news.models import News
from news.serializers.news import NewsListSerializer


class NewsListViewSet(ListModelMixin, GenericViewSet):
    serializer_class = NewsListSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        now = timezone.now()
        return (
            News.objects.filter(published_at__lte=now)
            .prefetch_related('tags')
            .order_by('-published_at')  
        )
