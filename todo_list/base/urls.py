from django.urls import path
from .views import (
    TaskList,
    TaskDetail, 
    TaskCreate, 
    TaskUpdate, 
    DeleteView, 
    CustomLoginView, 
    RegisterView
)
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>', DeleteView.as_view(), name='task-delete'),
]