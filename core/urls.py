from django.contrib import admin
from django.urls import path
from django.urls import include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularSwaggerSplitView

from core.views.api_root import APIRootView

def redirect_to_api(request):
    return redirect('api-root')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', redirect_to_api),
	path('api/', APIRootView.as_view(), name='api-root'), 
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/docs/', SpectacularSwaggerSplitView.as_view(url_name='schema')),
    path('news/', include('news.urls')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
