from django.urls import reverse
from rest_framework.test import APITestCase
from api.apps.users.models import User



class TestUser(APITestCase):
    def test_user_enrollment(self):
        """Test that a user can enrol successfully"""
        url = reverse('enrol_user')
        data = {
            'email': 'john@random.com',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
