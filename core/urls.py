from django.urls import include, path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.CustomRegisterView.as_view(), name='register'),
    path('', views.HomeView.as_view(), name='home'),
    path('groups/', views.GroupListView.as_view(), name='group_list'),
    path('groups/create/', views.GroupCreateView.as_view(), name='group_create'),
    path('groups/<str:group_name>/', views.TaskListView.as_view(), name='task_list'),
    path('groups/<str:group_name>/delete/', views.GroupDeleteView.as_view(), name='group_delete'),
    path('groups/<str:group_name>/<int:task_id>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('groups/<str:group_name>/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('groups/<str:group_name>/<int:task_id>/update/', views.TaskUpdateView.as_view(), name='task_update'),
    path('groups/<str:group_name>/<int:task_id>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
]