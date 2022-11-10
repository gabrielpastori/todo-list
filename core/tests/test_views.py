from audioop import reverse
from pydoc import resolve
from re import T
from django.test import TestCase
from django.urls import reverse
from django.shortcuts import resolve_url

from core.forms import CreateUserForm, CreateGroupForm, CreateTaskForm
from core.models import Group, Task, User

class CustomLoginViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(
            username='testuser1', password='12345')
        test_group = Group.objects.create(
            user=test_user, name='test_group')
        Task.objects.create(
            group=test_group, title='test_task', description='test_description')

    def test_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/login.html')

    def test_post(self):
        response = self.client.post(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/login.html')
    
    def test_get_authenticated(self):
        self.client.login(username='testuser1', password='12345')
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('group_list'))

class CustomRegisterViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(
            username='testuser1', password='12345')
        test_group = Group.objects.create(
            user=test_user, name='test_group')
        Task.objects.create(
            group=test_group, title='test_task', description='test_description')

    def test_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/register.html')

    def test_post_invalid(self):
        form = CreateUserForm()
        response = self.client.post(reverse('register'), {'form': form})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/register.html')
    
    def test_post_valid(self):
        form_data = {"username": "testuser2", "password1": "senhainteressante21", "password2": "senhainteressante21"}
        response = self.client.post(reverse('register'), data = form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_get_authenticated(self):
        self.client.login(username='testuser1', password='12345')
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('group_list'))

class HomeViewTest(TestCase):
    def test_get(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'core/index.html')
        self.assertEqual(response.status_code, 200)

class GroupListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(
            username='testuser1', password='12345')
        test_group = Group.objects.create(
            user=test_user, name='test_group')
        Task.objects.create(
            group=test_group, title='test_task', description='test_description')

    def test_get_authenticated(self):
        self.client.login(username='testuser1', password='12345')
        response = self.client.get(reverse('group_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/group_list.html')
    
    def test_get_not_authenticated(self):
        response = self.client.get(reverse('group_list'))
        url = reverse('login') + '?next=' + reverse('group_list')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, url)
    
    def test_post_autenticated(self):
        self.client.login(username='testuser1', password='12345')
        response = self.client.post(reverse('group_list'))
        self.assertEqual(response.status_code, 405)

    def test_post_not_authenticated(self):
        response = self.client.post(reverse('group_list'))
        self.assertEqual(response.status_code, 302)
        url = reverse('login') + '?next=' + reverse('group_list')
        self.assertRedirects(response, url)

class GroupCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(
            username='testuser1', password='12345')
        test_group = Group.objects.create(
            user=test_user, name='test_group')
        Task.objects.create(
            group=test_group, title='test_task', description='test_description')

    def test_get_authenticated(self):
        self.client.login(username='testuser1', password='12345')
        response = self.client.get(reverse('group_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/group_create.html')
    
    def test_get_not_authenticated(self):
        response = self.client.get(reverse('group_create'))
        url = reverse('login') + '?next=' + reverse('group_create')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, url)
    
    def test_post_valid(self):
        self.client.login(username='testuser1', password='12345')
        response = self.client.post(reverse('group_create'), data = {'name': 'test_group2'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('group_list'))
    
    def test_post_invalid(self):
        self.client.login(username='testuser1', password='12345')
        response = self.client.post(reverse('group_create'), data = {'name': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/group_create.html')

    def test_post_not_authenticated(self):
        response = self.client.post(reverse('group_create'), data = {'name': 'test_group2'})
        url = reverse('login') + '?next=' + reverse('group_create')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, url)

class TaskListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(
            username='testuser1', password='12345')
        test_user2 = User.objects.create_user(
            username='testuser2', password='12345')
        test_group = Group.objects.create(
            user=test_user, name='test_group')
        test_group2 = Group.objects.create(
            user=test_user2, name='test_group2')
        Task.objects.create(
            group=test_group, title='test_task', description='test_description')
        Task.objects.create(
            group=test_group, title='test_task2', description='test_description2')
        Task.objects.create(
            group=test_group2, title='test_task3', description='test_description3')
        Task.objects.create(
            group=test_group2, title='test_task4', description='test_description4')
    
    def test_get_not_authenticated(self):
        response = self.client.get(resolve_url('task_list', group_name = 'test_group'))
        url = reverse('login') + '?next=' + resolve_url('task_list', group_name = 'test_group')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, url)
    
    def test_get_authenticated(self):
        self.client.login(username='testuser1', password='12345')
        response = self.client.get(resolve_url('task_list', group_name = 'test_group'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/task_list.html')

    def test_get_filtered(self):
        self.client.login(username='testuser1', password='12345')
        response = self.client.get(resolve_url('task_list', group_name = 'test_group'), {'search-area': 'test_task'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/task_list.html')
        self.assertEqual(len(response.context['tasks']), 2)

    def test_post(self):
        self.client.login(username='testuser1', password='12345')
        response = self.client.post(resolve_url('task_list', group_name = 'test_group'))
        self.assertEqual(response.status_code, 405)

class TaskDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(
            username='testuser1', password='12345')
        test_group = Group.objects.create(
            user=test_user, name='test_group')
        Task.objects.create(
            group=test_group, title='test_task', description='test_description')
        Task.objects.create(
            group=test_group, title='test_task2', description='test_description2')

    def test_get_not_authenticated(self):
        response = self.client.get(resolve_url('task_detail', group_name = 'test_group', task_id = 1))
        url = reverse('login') + '?next=' + resolve_url('task_detail', group_name = 'test_group', task_id = 1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, url)
    
    def test_get_authenticated(self):
        self.client.login(username='testuser1', password='12345')
        response = self.client.get(resolve_url('task_detail', group_name = 'test_group', task_id = 1))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/task_detail.html')

    def test_post(self):
        self.client.login(username='testuser1', password='12345')
        response = self.client.post(resolve_url('task_detail', group_name = 'test_group', task_id = 1))
        self.assertEqual(response.status_code, 405)

class TaskCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(
            username='testuser1', password='12345')
        test_group = Group.objects.create(
            user=test_user, name='test_group')
        Task.objects.create(
            group=test_group, title='test_task', description='test_description')
        Task.objects.create(
            group=test_group, title='test_task2', description='test_description2')
    
    def test_get_not_authenticated(self):
        response = self.client.get(resolve_url('task_create', group_name = 'test_group'))
        url = reverse('login') + '?next=' + resolve_url('task_create', group_name = 'test_group')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, url)
    
    def test_get_authenticated(self):
        self.client.login(username='testuser1', password='12345')
        response = self.client.get(resolve_url('task_create', group_name = 'test_group'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/task_create.html')
    
    def test_post_not_authenticated(self):
        response = self.client.post(resolve_url('task_create', group_name = 'test_group'), data = {'title': 'test_task3', 'description': 'test_description3'})
        url = reverse('login') + '?next=' + resolve_url('task_create', group_name = 'test_group')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, url)
    
    def test_post_invalid(self):
        self.client.login(username='testuser1', password='12345')
        response = self.client.post(resolve_url('task_create', group_name = 'test_group'), data = {'title': '', 'description': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/task_create.html')
        self.assertEqual(len(Task.objects.all()), 2)
    
    def test_post_valid(self):
        self.client.login(username='testuser1', password='12345')
        response = self.client.post(resolve_url('task_create', group_name = 'test_group'), data = {'title': 'test_task3', 'description': 'test_description3', 'completed': True})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, resolve_url('task_list', group_name = 'test_group'))
        self.assertEqual(len(Task.objects.all()), 3)

class TaskUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(
            username='testuser1', password='12345')
        test_group = Group.objects.create(
            user=test_user, name='test_group')
        Task.objects.create(
            group=test_group, title='test_task', description='test_description')
        Task.objects.create(
            group=test_group, title='test_task2', description='test_description2')
    
    def test_get_not_authenticated(self):
        response = self.client.get(resolve_url('task_update', group_name = 'test_group', task_id = 1))
        url = reverse('login') + '?next=' + resolve_url('task_update', group_name = 'test_group', task_id = 1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, url)
    
    def test_get_authenticated(self):
        self.client.login(username='testuser1', password='12345')
        response = self.client.get(resolve_url('task_update', group_name = 'test_group', task_id = 1))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/task_update.html')
        self.assertEqual(len(Task.objects.all()), 2)

    def test_post_not_authenticated(self):
        response = self.client.post(resolve_url('task_update', group_name = 'test_group', task_id = 1))
        url = reverse('login') + '?next=' + resolve_url('task_update', group_name = 'test_group', task_id = 1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, url)
        self.assertEqual(len(Task.objects.all()), 2)
    
    def test_post(self):
        self.client.login(username='testuser1', password='12345')
        data = {'title': 'test_task3', 'description': 'test_description3', 'completed': True}
        response = self.client.post(resolve_url('task_update', group_name = 'test_group', task_id = 1), data = data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, resolve_url('task_list', group_name = 'test_group'))
        self.assertEqual(len(Task.objects.all()), 2)

class TaskDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(
            username='testuser1', password='12345')
        test_group = Group.objects.create(
            user=test_user, name='test_group')
        Task.objects.create(
            group=test_group, title='test_task', description='test_description')
        Task.objects.create(
            group=test_group, title='test_task2', description='test_description2')
    
    def test_get_not_authenticated(self):
        response = self.client.get(resolve_url('task_delete', group_name = 'test_group', task_id = 1))
        url = reverse('login') + '?next=' + resolve_url('task_delete', group_name = 'test_group', task_id = 1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, url)
    
    def test_get_authenticated(self):
        self.client.login(username='testuser1', password='12345')
        response = self.client.get(resolve_url('task_delete', group_name = 'test_group', task_id = 1))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/task_delete.html')
        self.assertEqual(len(Task.objects.all()), 2)

    def test_post_not_authenticated(self):
        response = self.client.post(resolve_url('task_delete', group_name = 'test_group', task_id = 1))
        url = reverse('login') + '?next=' + resolve_url('task_delete', group_name = 'test_group', task_id = 1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, url)
        self.assertEqual(len(Task.objects.all()), 2)
    
    def test_post(self):
        self.client.login(username='testuser1', password='12345')
        response = self.client.post(resolve_url('task_delete', group_name = 'test_group', task_id = 1))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, resolve_url('task_list', group_name = 'test_group'))
        self.assertEqual(len(Task.objects.all()), 1)