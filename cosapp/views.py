from django.shortcuts import render, redirect

# Create your views here.

from django.views.generic import ListView, CreateView, TemplateView, DeleteView, UpdateView, FormView
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, CustomUserUpdateForm, AdminMessageForm, AdminMessage
from .models import CustomAdmin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse

CustomUser = get_user_model()

class AdminView(LoginRequiredMixin, View):
    login_url = 'admin_login'
    template_name = 'cosapp/dashboard/dashboard.html'

    def get(self, request):
        if not CustomAdmin.objects.exists():
            return redirect('admin_setup')
        
        if not isinstance(request.user, CustomAdmin):
            return redirect('admin_login')
        
        return render(request, self.template_name)

class UserListView(ListView):
    template_name = 'cosapp/dashboard/user_list.html'
    model = CustomUser
    context_object_name = 'users'
    
    def get_queryset(self):
        return CustomUser.objects.filter(is_admin=False)

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

class DashboardView(LoginRequiredMixin, View):
    login_url = 'admin_login'

    def get(self, request):
        return render(request, 'cosapp/dashboard/dashboard.html')

class AdminSetupView(View):
    def get(self, request):
        if CustomAdmin.objects.exists():
            return redirect('admin_login')
        return render(request, 'cosapp/dashboard/admin_setup.html')

    def post(self, request):
        if CustomAdmin.objects.exists():
            return redirect('admin_login')
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        admin = CustomAdmin.objects.create_admin(username=username, password=password)
        
        login(request, admin)
        return render(request, 'cosapp/dashboard/dashboard.html')  # 直接ダッシュボードを表示

class AdminLoginView(View):
    def get(self, request):
        if not CustomAdmin.objects.exists():
            return redirect('admin_setup')
        if request.user.is_authenticated and isinstance(request.user, CustomAdmin):
            return redirect('dashboard')
        return render(request, 'cosapp/dashboard/admin_login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Attempting login for user: {username}")  # デバッグ出力
        user = authenticate(request, username=username, password=password)
        
        print(f"Authenticated user: {user}")  # デバッグ出力
        print(f"User type: {type(user)}")  # デバッグ出力
        
        if user is not None and user.is_admin_user:  # CustomAdminの代わりにis_admin_userをチェック
            login(request, user)
            print("Login successful, redirecting to dashboard")  # デバッグ出力
            return redirect('dashboard')
        else:
            print("Login failed")  # デバッグ出力
            return render(request, 'cosapp/dashboard/admin_login.html', {'error': 'Invalid credentials'})
            
class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().get(request, *args, **kwargs)