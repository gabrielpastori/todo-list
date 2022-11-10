from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Group, Task

class GroupModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = User.objects.create_user(
            username='testuser1', password='12345')
        Group.objects.create(
            user=testuser1, name='test_group')

    def test_group_str_default(self):
        group = Group.objects.get(id=1)
        expected_object_name = f'{group}'
        self.assertEqual(expected_object_name, 'test_group')

    def test_group_user(self):
        group = Group.objects.get(id=1)
        expected_object_user = f'{group.user}'
        self.assertEqual(expected_object_user, 'testuser1')

class TaskModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = User.objects.create_user(
            username='testuser1', password='12345')
        test_group = Group.objects.create(
            user=testuser1, name='test_group')
        Task.objects.create(
            group=test_group, title='test_task', description='test_description')
    
    def test_task_str_default(self):
        task = Task.objects.get(id=1)
        expected_object_name = f'{task}'
        self.assertEqual(expected_object_name, 'test_task')

    def test_task_group(self):
        task = Task.objects.get(id=1)
        expected_object_group = f'{task.group}'
        self.assertEqual(expected_object_group, 'test_group')