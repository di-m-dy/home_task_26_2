from django.urls import reverse
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscribe
from users.models import User


class LessonTestCase(APITestCase):
    """
    Тесты для уроков (CRUD
    """
    def setUp(self):
        self.user = User.objects.create(email='testuser@example.com', password='testpassword')
        self.other_user = User.objects.create(email='other_test_user@example.com', password='testpassword')
        self.admin = User.objects.create(email='test_admin@example.com', password='testpassword', is_staff=True)
        self.course = Course.objects.create(title='Test Course', description='Test Description', owner=self.user)
        self.lesson = Lesson.objects.create(title='Test Lesson', description='Test Description', owner=self.user,
                                            course=self.course)
        self.subscribe = Subscribe.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse('materials:lesson_detail', args=[self.lesson.pk])
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['title'], self.lesson.title)
        self.assertEqual(data['description'], self.lesson.description)
        self.assertEqual(data['owner'], self.lesson.owner.pk)
        self.assertEqual(data['course'], self.lesson.course.pk)

    def test_lesson_create(self):
        url = reverse('materials:lesson_create')
        self.client.request(**{'user': self.user.pk})
        data = {
            'title': 'New Lesson',
            'description': 'New Description',
            'course': self.course.pk,
            'owner': self.user.pk
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Lesson.objects.count(), 2)
        self.assertEqual(Lesson.objects.last().title, 'New Lesson')
        self.assertEqual(Lesson.objects.last().description, 'New Description')
        self.assertEqual(Lesson.objects.last().owner, self.user)
        self.assertEqual(Lesson.objects.last().course, self.course)

    def test_lesson_update(self):
        url = reverse('materials:lesson_update', args=[self.lesson.pk])
        data = {
            'title': 'Updated Lesson',
            'description': 'Updated Description',
            'course': self.course.pk,
            'owner': self.user.pk
        }
        new_data = {
            'title': 'New Lesson',
            'description': 'New Description'
        }
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Updated Lesson')
        self.assertEqual(self.lesson.description, 'Updated Description')
        self.assertEqual(self.lesson.owner, self.user)
        self.assertEqual(self.lesson.course, self.course)
        self.client.force_authenticate(user=self.other_user)
        response = self.client.patch(url, data=new_data)
        self.assertEqual(response.status_code, 403)
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(url, data=new_data)
        self.assertEqual(response.status_code, 200)

    def test_lesson_delete(self):
        url = reverse('materials:lesson_delete', args=[self.lesson.pk])
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_lesson_list(self):
        url = reverse('materials:lesson_list')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 4)
        self.assertEqual(data['results'][0]['title'], self.lesson.title)
        self.assertEqual(data['results'][0]['description'], self.lesson.description)
        self.assertEqual(data['results'][0]['owner'], self.lesson.owner.pk)
        self.assertEqual(data['results'][0]['course'], self.lesson.course.pk)


class SubscribeToggleTestCase(APITestCase):
    """
    Тесты для подписки на курс
    """
    def setUp(self):
        self.user = User.objects.create(email='test_for_subscribe', password='testpassword')
        self.course = Course.objects.create(title='Test Course', description='Test Description', owner=self.user)
        self.subscribe = Subscribe.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_subscribe_toggle(self):
        url = reverse('materials:lesson_subscribe')
        data = {
            'course': self.course.pk
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Subscribe.objects.count(), 0)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Subscribe.objects.count(), 1)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Subscribe.objects.count(), 0)
