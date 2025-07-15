from django.urls import path
from news.views.news import NewsListViewSet

urlpatterns = [
	path('news/', NewsListViewSet.as_view({'get': 'list'}), name='news-list-explicit'),  
]
