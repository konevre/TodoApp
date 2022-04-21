from django.shortcuts import render, redirect

from django.contrib.auth.models import User

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


from django.urls import reverse_lazy

from .models import Task


class CustomLoginView(LoginView):
    template_name = 'base/registration/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('task_list')


class RegisterPage(FormView):
    template_name = 'base/registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('task_list')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskListView(LoginRequiredMixin, ListView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_list'] = context['task_list'].filter(
            user=self.request.user)
        context['count'] = context['task_list'].filter(
            complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['task_list'] = context['task_list'].filter(
                title__icontains=search_input)

        context['search_input'] = search_input

        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('task_list')

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.user


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('task_list')

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.user


class UpdateUserView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'base/registration/user_update.html'
    fields = ['username', ]
    success_url = reverse_lazy('task_list')

    def test_func(self):
        user = self.get_object()
        return user == self.request.user


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'base/registration/password_change_form.html'
    success_url = reverse_lazy('login')


class UserPasswordResetView(PasswordResetView):
    template_name = 'base/registration/password_reset_form.html'
    success_url = reverse_lazy('login')
