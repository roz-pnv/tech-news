from django.urls import path

from news.views.news import NewsListViewSet
from news.views.news import NewsMutationViewSet

urlpatterns = [
	path('', NewsListViewSet.as_view({'get': 'list'}), name='news-list-explicit'), 
	path('create/', NewsMutationViewSet.as_view({'post': 'create'}), name='news-create'), 
    path('<slug:slug>/update/', NewsMutationViewSet.as_view({'put': 'update'}), name='news-update'),
    path('<slug:slug>/partial/', NewsMutationViewSet.as_view({'patch': 'partial_update'}), name='news-partial-update'),
	path('<slug:slug>/delete/', NewsMutationViewSet.as_view({'delete': 'destroy'}), name='news-delete'),
]
