from django.urls import path

from news.views.news import NewsListViewSet
from news.views.news import NewsMutationViewSet
from news.views.news import NewsDetailViewSet

urlpatterns = [
	path('', NewsListViewSet.as_view({'get': 'list'}), name='news-list-explicit'), 
	path('create/', NewsMutationViewSet.as_view({'post': 'create'}), name='news-create'), 
	path('<str:slug>/', NewsDetailViewSet.as_view({'get': 'retrieve'}), name='news-detail'),
    path('<str:slug>/update/', NewsMutationViewSet.as_view({'put': 'update'}), name='news-update'),
    path('<str:slug>/partial/', NewsMutationViewSet.as_view({'patch': 'partial_update'}), name='news-partial-update'),
	path('<str:slug>/delete/', NewsMutationViewSet.as_view({'delete': 'destroy'}), name='news-delete'),
]
