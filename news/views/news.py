from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

from utils.pagination import StandardResultsSetPagination
from news.filters import NewsFilter
from news.models import News
from news.serializers.news import NewsListSerializer
from news.serializers.news import NewsCreateSerializer
from news.serializers.news import NewsUpdateSerializer
from news.serializers.news import NewsDetailSerializer


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
    update=extend_schema(
        summary="Update a news item",
        description="Fully updates a news article. Requires JWT authentication.",
        request=NewsUpdateSerializer,
        responses=NewsUpdateSerializer,
    ),
    partial_update=extend_schema(
        summary="Partially update a news item",
        description="Partially updates a news article. Requires JWT authentication.",
        request=NewsUpdateSerializer,
        responses=NewsUpdateSerializer,
    ),
    destroy=extend_schema(
        summary="Delete a news article",
        description="Deletes a news article by slug. Requires JWT authentication.",
        responses={204: None},
    ),
)
class NewsMutationViewSet(
    GenericViewSet,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    queryset = News.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug' 

    def get_serializer_class(self):
        if self.action == 'create':
            return NewsCreateSerializer
        
        elif self.action in ['update', 'partial_update']:
            return NewsUpdateSerializer

    def perform_create(self, serializer):
        serializer.save() 

    def perform_destroy(self, instance):
        for image in instance.images.all():
            if image.image_file:
                image.image_file.delete(save=False)
    
        instance.delete()


@extend_schema_view(
    retrieve=extend_schema(
        summary="Retrieve a specific published news item",
        description="Returns the details of a published news article by ID. Only published articles are accessible.",
        responses=NewsListSerializer
    )
)
class NewsDetailViewSet(
    GenericViewSet,
    RetrieveModelMixin, 
):
    serializer_class = NewsDetailSerializer  
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def get_queryset(self):
        return (
            News.objects.filter(published_at__isnull=False)
            .prefetch_related('tags')
        )
