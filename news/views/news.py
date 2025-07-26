from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

from utils.pagination import StandardResultsSetPagination
from news.models import News
from news.serializers.news import NewsListSerializer
from news.serializers.news import NewsCreateSerializer
from news.filters import NewsFilter

@extend_schema(
    summary="List published news",
    description="Returns a paginated list of news articles that have a valid publish date. Supports filtering by tags and keywords.",
    responses=NewsListSerializer
)
class NewsListViewSet(
    GenericViewSet,
    ListModelMixin, 
):
    serializer_class = NewsListSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = NewsFilter
    
    def get_queryset(self):
        return (
            News.objects.filter(published_at__isnull=False)
            .prefetch_related('tags')
            .order_by('-published_at')  
        )
    

@extend_schema_view(
    create=extend_schema(
        summary="Create a news item",
        description="Creates a new news article. Requires JWT authentication.",
        request=NewsCreateSerializer,
        responses=NewsCreateSerializer,
    ),
)
class NewsMutationViewSet(
    GenericViewSet,
    CreateModelMixin,
):
    queryset = News.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return NewsCreateSerializer

    def perform_create(self, serializer):
        serializer.save() 
