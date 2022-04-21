from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
    TaskListView,
    # TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    CustomLoginView,
    RegisterPage,
    UpdateUserView,
    UserPasswordChangeView,
    UserPasswordResetView,
)

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('settings/<int:pk>/', UpdateUserView.as_view(), name='settings'),
    path('settings/pasword_change/',
         UserPasswordChangeView.as_view(), name='password_change'),
    path('login/reset_password/',
         UserPasswordResetView.as_view(), name='password_reset'),

    path('', TaskListView.as_view(), name='task_list'),
    # path('task/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('task/create/', TaskCreateView.as_view(), name='task_create'),
    path('task/update/<int:pk>/', TaskUpdateView.as_view(), name='task_update'),
    path('task/delete/<int:pk>/', TaskDeleteView.as_view(), name='task_delete'),
]
