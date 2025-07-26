from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

class APIRootViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("api-root")

    def test_api_root_response_structure(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Top-level keys
        self.assertIn("endpoints", response.data)
        self.assertIn("server", response.data)

        # Server info checks
        server_info = response.data["server"]
        self.assertEqual(server_info["status"], "ok")
        self.assertIn("timezone", server_info)
        self.assertIn("current_time", server_info)

        # Endpoints check: should be a dictionary
        endpoints = response.data["endpoints"]
        self.assertIsInstance(endpoints, dict)
        for name, data in endpoints.items():
            self.assertIn("description", data)
            self.assertIn("url", data)
