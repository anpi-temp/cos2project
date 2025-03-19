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
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import AdminMessageSerializer

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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['admin_user'] = CustomUser.objects.filter(is_admin=True).first()
        return context

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
        return AdminMessage.objects.filter(recipient=recipient).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipient = get_object_or_404(CustomUser, id=self.kwargs.get('user_id'))
        context['recipient'] = recipient
        
        # 未読メッセージ数 (is_read を使用)
        context['unread_count'] = self.get_queryset().filter(is_read=False).count()
        return context

class AdminMessageViewSet(viewsets.ModelViewSet):
    serializer_class = AdminMessageSerializer

    queryset = AdminMessage.objects.all()  # すべてのメッセージを取得

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        try:
            message = AdminMessage.objects.get(pk=pk)  # メッセージを取得
            message.is_read = True
            message.save()
            return Response({'status': 'message marked as read'})
        except AdminMessage.DoesNotExist:
            return Response({'status': 'message not found'}, status=404)
        
class ReadMessageListView(View):
    template_name = 'cosapp/user/read_message_list.html'

    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, pk=user_id)  # user_id でユーザーを取得
        messages = AdminMessage.objects.filter(recipient=user, is_read=True)
        context = {
            'recipient': user,
            'messages': messages,
        }
        return render(request, self.template_name, context)

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