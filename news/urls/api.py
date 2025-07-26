from django.urls import path

from news.views.news import NewsListViewSet
from news.views.news import NewsMutationViewSet

urlpatterns = [
	path('news/', NewsListViewSet.as_view({'get': 'list'}), name='news-list-explicit'), 
	path('news/create/', NewsMutationViewSet.as_view({'post': 'create'}), name='news-create'), 
    path('news/<slug:slug>/update/', NewsMutationViewSet.as_view({'put': 'update'}), name='news-update'),
    path('news/<slug:slug>/partial/', NewsMutationViewSet.as_view({'patch': 'partial_update'}), name='news-partial-update'),
]
