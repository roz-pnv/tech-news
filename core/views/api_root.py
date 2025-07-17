from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from core.constants.api_endpoints import API_ENDPOINTS

class APIRootView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, format=None):
        return Response({
            "endpoints": API_ENDPOINTS,
            "server": {
                "status": "ok",
                "timezone": settings.TIME_ZONE,
                "current_time": self._get_current_time(),
            }
        })

    def _get_current_time(self):
        from django.utils import timezone
        return timezone.now().isoformat()
