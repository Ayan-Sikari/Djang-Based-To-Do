from django.shortcuts import render, redirect
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,FormView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .models import Task
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.db.models import Q

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterView(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        try:
            user = form.save()
            login(self.request, user)
            return super(RegisterView, self).form_valid(form)
        except Exception as e:
            form.add_error(None, "Registration failed. Please try again.")
            return self.form_invalid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterView, self).get(*args, **kwargs)


@method_decorator(never_cache, name='dispatch')
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    
    def get_queryset(self):
        """Filters tasks based on logged-in user."""
        q_object = Q(user=self.request.user)
        queryset=Task.objects.filter(q_object)
        search_input = self.request.GET.get('search-area', '').strip()

        if search_input:
            queryset = queryset.filter(title__icontains=search_input).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        """Adds extra context to the template."""
        context = super().get_context_data(**kwargs)
        context['count'] = self.get_queryset().filter(complete=False).count()
        context['color'] = 'red'  # Not used, but kept as in the original
        context['search_input'] = self.request.GET.get('search-area', '')
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks')


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task_confirm_delete.html'
    success_url = reverse_lazy('tasks')
