from django.urls import path

from news.views.news import NewsListViewSet
from news.views.news import NewsCreateViewSet

urlpatterns = [
	path('news/', NewsListViewSet.as_view({'get': 'list'}), name='news-list-explicit'), 
	path('news/create/', NewsCreateViewSet.as_view({'post': 'create'}), name='news-create'), 
]
