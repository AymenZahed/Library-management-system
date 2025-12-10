from django.test import TestCase
from .models import Notification
from django.urls import reverse
from rest_framework import status

class NotificationModelTest(TestCase):
    def setUp(self):
        self.notification = Notification.objects.create(
            user_id=1,
            type='info',
            subject='Test Notification',
            message='This is a test notification.',
            status='sent'
        )

    def test_notification_creation(self):
        self.assertEqual(self.notification.subject, 'Test Notification')
        self.assertEqual(self.notification.message, 'This is a test notification.')

class NotificationAPITest(TestCase):
    def setUp(self):
        self.notification_data = {
            'user_id': 1,
            'type': 'info',
            'subject': 'Test Notification',
            'message': 'This is a test notification.',
            'status': 'sent'
        }
        self.notification = Notification.objects.create(**self.notification_data)

    def test_send_notification(self):
        response = self.client.post(reverse('send_notification'), self.notification_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_user_notifications(self):
        response = self.client.get(reverse('get_user_notifications', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_notification_details(self):
        response = self.client.get(reverse('get_notification_details', args=[self.notification.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_pending_notifications(self):
        response = self.client.get(reverse('get_pending_notifications'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)