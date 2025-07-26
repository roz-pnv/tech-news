from django.conf import settings
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import serializers

from core.constants.api_endpoints import API_ENDPOINTS

class APIRootResponseSerializer(serializers.Serializer):
    endpoints = serializers.DictField(
        child=serializers.CharField(),
        help_text="Dictionary of available API endpoints with their descriptions"
    )
    server = serializers.DictField(
        help_text="Server status and metadata like timezone and current time"
    )

@extend_schema(
    summary="API Root Endpoint",
    description="Returns basic metadata about the API, including available endpoints and server info.",
    responses=APIRootResponseSerializer
)
class APIRootView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, format=None):
        return Response({
            "endpoints": self._get_endpoints(),
            "server": self._get_server_info(),
        })

    def _get_endpoints(self):
        return {
            name: {
                "description": data["description"],
                "url": self.request.build_absolute_uri(data["path"])
            }
            for name, data in API_ENDPOINTS.items()
        }

    def _get_server_info(self):
        return {
            "status": "ok",
            "timezone": settings.TIME_ZONE,
            "current_time": timezone.now().isoformat(),
        }
