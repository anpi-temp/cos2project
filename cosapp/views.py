from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, FormView, TemplateView
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, CustomUserUpdateForm, AdminMessageForm
from .models import AdminMessage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib import messages

CustomUser = get_user_model()

class AdminView(LoginRequiredMixin, View):
    login_url = 'admin_login'
    template_name = 'cosapp/dashboard/dashboard.html'

    def get(self, request):
        if not request.user.is_admin:  # 管理者フラグでチェック
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
    template_name = 'cosapp/dashboard/user_edit.html'
    success_url = reverse_lazy('user_list')

    def get_initial(self):
        initial = super().get_initial()
        initial['username'] = ''  # ユーザー名の初期値をクリア
        return initial

class SendAdminMessageView(FormView):
    template_name = 'cosapp/dashboard/send_message.html'
    form_class = AdminMessageForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        message = form.save(commit=False)
        message.sender = self.request.user  # 現在のユーザーを送信者として設定
        message.save()
        return super().form_valid(form)

class UserMessageListView(ListView):
    model = AdminMessage
    template_name = 'cosapp/user/message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        recipient = get_object_or_404(CustomUser, id=user_id)
        return AdminMessage.objects.filter(recipient=recipient)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipient'] = get_object_or_404(CustomUser, id=self.kwargs.get('user_id'))
        return context

class DashboardView(LoginRequiredMixin, View):
    login_url = 'admin_login'

    def get(self, request):
        if not request.user.is_admin:  # 管理者フラグでチェック
            return redirect('admin_login')
        return render(request, 'cosapp/dashboard/dashboard.html')

class AdminSetupView(View):
    def get(self, request):
        if CustomUser.objects.filter(is_admin=True).exists():  # 管理者が存在する場合リダイレクト
            return redirect('admin_login')
        return render(request, 'cosapp/dashboard/admin_setup.html')

    def post(self, request):
        if CustomUser.objects.filter(is_admin=True).exists():
            return redirect('admin_login')
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = CustomUser.objects.create_user(username=username, password=password)
        user.is_admin = True  # 管理者フラグを設定
        user.is_staff = True  # スタッフ権限を付与（管理画面アクセス可能）
        user.save()
        
        login(request, user)
        return redirect('dashboard')

class AdminLoginView(View):
    def get(self, request):
        if not CustomUser.objects.filter(is_admin=True).exists():  # 管理者がいない場合セットアップへリダイレクト
            return redirect('admin_setup')
        if request.user.is_authenticated and request.user.is_admin:  # 認証済みかつ管理者の場合ダッシュボードへリダイレクト
            return redirect('dashboard')
        return render(request, 'cosapp/dashboard/admin_login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_admin:  # 管理者フラグでチェック
            login(request, user)
            return redirect('/dashboard/')
        else:
            messages.error(request, '無効な資格情報です。')
            return render(request, 'cosapp/dashboard/admin_login.html')

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().get(request, *args, **kwargs)
    
class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'ログアウトしました。')
        return redirect('admin_login')
    
class SomeView(TemplateView):
    template_name = "cosapp/dashboard/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["key"] = "value"
        return context