from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status

from apps.checklist.models import Directory
from apps.checklist.serializers import DirectorySerializer
from rest_framework.test import APITestCase


class DirectoryAPITestCase(APITestCase):
    def test_get(self):
        user_1 = User.objects.create(username='user_1', password='12345')
        dir_1 = Directory.objects.create(name='/', parent=None, owner=user_1)
        url = reverse('dir_data', args=(dir_1.id,))
        self.client.force_login(user_1)
        response = self.client.get(url)
        serializer_data = DirectorySerializer(dir_1)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data.data, response.data)
