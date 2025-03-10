from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView, CreateView, TemplateView, DeleteView, UpdateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, CustomUserUpdateForm, AdminMessageForm, AdminMessage

CustomUser = get_user_model()

class AdminView(TemplateView):
    template_name = 'cosapp/dashboard/dashboard.html'

class UserListView(ListView):
    template_name = 'cosapp/dashboard/user_list.html'
    model = CustomUser
    context_object_name = 'users'

class UserCreateView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'cosapp/dashboard/user_create.html'
    success_url = reverse_lazy('user_list')

class UserDeleteView(DeleteView):
    model = CustomUser
    template_name = 'cosapp/dashboard/user_delete.html'
    success_url = reverse_lazy('user_list')

class UserUpdateView(UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = 'cosapp/dashboard/user_update.html'
    success_url = reverse_lazy('user_list')

class SendAdminMessageView(FormView):
    template_name = 'cosapp/dashboard/send_message.html'
    form_class = AdminMessageForm
    success_url = reverse_lazy('dashboard')

class UserMessageListView(ListView):
    model = AdminMessage
    template_name = 'cosapp/user/message_list.html'
    context_object_name = 'messages'
