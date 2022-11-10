from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseNotFound
from django.views import View
from django.views.generic import TemplateView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Group, Task
from .forms import CreateGroupForm, CreateUserForm, CreateTaskForm


class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('group_list')


class CustomRegisterView(View):
    template_name = 'core/register.html'
    success_url = reverse_lazy('group_list')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('group_list')
        form = CreateUserForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        context = {'form': form}
        return render(request, self.template_name, context)

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'core/index.html', {})


class GroupListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        groups = Group.objects.filter(user=request.user)
        context = {'groups': groups}
        return render(request, 'core/group_list.html', context)


class GroupCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = CreateGroupForm()
        return render(request, 'core/group_create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = CreateGroupForm(request.POST)
        form.instance.user = request.user
        if form.is_valid():
            form.save()
            return redirect('group_list')
        return render(request, 'core/group_create.html', {'form': form})

class GroupDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        group_name = kwargs['group_name']
        group = get_object_or_404(Group, name=group_name, user = request.user)
        context = {'group_name': group_name}
        return render(request, 'core/group_delete.html', context)

    def post(self, request, *args, **kwargs):
        group_name = kwargs['group_name']
        group = get_object_or_404(Group, name=group_name, user = request.user)
        group.delete() 
        return redirect('group_list')

class TaskListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        group_name = kwargs['group_name']
        group_id = get_object_or_404(Group, name=group_name, user = request.user).id
        tasks_filtered = Task.objects.filter(group=group_id)
        search_input = request.GET.get('search-area') or ''
        if search_input:
            tasks_filtered = tasks_filtered.filter(
                title__startswith=search_input)

        context = {'tasks': tasks_filtered,
                   'group_name': group_name, 'search_input': search_input}

        return render(request, 'core/task_list.html', context)


class TaskDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        group_name = kwargs['group_name']
        group_id = get_object_or_404(Group, name=group_name, user = request.user).id
        task = get_object_or_404(Task, id=kwargs['task_id'], group=group_id)
        context = {'task': task, 'group_name': group_name}
        return render(request, 'core/task_detail.html', context)


class TaskCreateView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        form = CreateTaskForm()
        group_name = kwargs['group_name']
        user = get_object_or_404(Group, name=group_name, user = request.user)
        context = {'form': form, 'group_name': group_name}
        return render(request, 'core/task_create.html', context)

    def post(self, request, *args, **kwargs):
        form = CreateTaskForm(request.POST)
        group_id = get_object_or_404(Group, name=kwargs['group_name'], user = request.user).id
        form.instance.group = Group.objects.get(id=group_id)
        if form.is_valid():
            form.save()
            return redirect("task_list", kwargs['group_name'])
        context = {'form': form, 'group_name': kwargs['group_name']}
        return render(request, 'core/task_create.html', context)

class TaskUpdateView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        group_name = kwargs['group_name']
        group_id = get_object_or_404(Group, name=group_name, user = request.user).id
        task_instance = get_object_or_404(Task, id=kwargs['task_id'], group=group_id)
        form = CreateTaskForm(instance=task_instance)
        group_name = kwargs['group_name']
        context = {'form': form, 'task': task_instance, 'group_name': group_name}
        return render(request, 'core/task_update.html', context)

    def post(self, request, *args, **kwargs):
        group_name = kwargs['group_name']
        group_id = get_object_or_404(Group, name=group_name, user = request.user).id
        task_instance = get_object_or_404(Task, id=kwargs['task_id'], group=group_id)
        form = CreateTaskForm(request.POST, instance=task_instance)
        group_name = kwargs['group_name']
        if form.is_valid():
            form.save()
            return redirect("task_list", group_name)


class TaskDeleteView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        group_name = kwargs['group_name']
        group_id = get_object_or_404(Group, name=group_name, user = request.user).id
        task_instance = get_object_or_404(Task, id=kwargs['task_id'], group=group_id)
        context = {'task': task_instance, 'group_name': group_name}
        return render(request, 'core/task_delete.html', context)

    def post(self, request, *args, **kwargs):
        group_name = kwargs['group_name']
        group_id = get_object_or_404(Group, name=group_name, user = request.user).id
        task_instance = get_object_or_404(Task, id=kwargs['task_id'], group=group_id)
        task_instance.delete() 
        return redirect('task_list', group_name)
