from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, FormView, TemplateView
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, CustomUserUpdateForm, AdminMessageForm
from .models import AdminMessage
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.contrib import messages
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import AdminMessageSerializer
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator

CustomUser = get_user_model()

class AdminView(LoginRequiredMixin, View):
    login_url = 'admin_login'
    template_name = 'cosapp/dashboard/dashboard.html'

    def get(self, request):
        if not request.user.is_admin:  # 管理者フラグでチェック
            return redirect('admin_login')
        return render(request, self.template_name)
    
def dashboard_alt(request):
    return render(request, 'cosapp/dashboard/dashboard_alt.html')

def dashboard_alt2(request):
    return render(request, 'cosapp/dashboard/dashboard_alt2.html')

class UserListView(ListView):
    template_name = 'cosapp/dashboard/user_list.html'
    model = CustomUser
    context_object_name = 'users'
    
    def get_queryset(self):
        return CustomUser.objects.filter(is_admin=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 管理者ユーザーを取得
        context['admin_user'] = CustomUser.objects.filter(is_admin=True).first()

        # 中間管理者ユーザーを取得
        staff_count = 2  # 中間管理者のスロット数
        staff_users = list(CustomUser.objects.filter(is_admin=False, is_staff=True)[:staff_count])

        labels = ['スタッフA', 'スタッフB']  # 表示したい文字列リスト
        staff_slots = []
        for i in range(staff_count):
            if i < len(staff_users):
                # ユーザーが存在する場合
                staff = staff_users[i]
                staff_slots.append({
                    'user': staff,
                    'label': labels[i] if i < len(labels) else ''  # ラベルが足りない場合は空文字
                })
            else:
                # ユーザーが存在しない場合、空スロットを作成
                staff_slots.append({
                    'user': None,
                    'label': labels[i] if i < len(labels) else ''
                })

        context['staff_slots'] = staff_slots

        users = list(self.get_queryset())
        slots = users + [None] * (20 - len(users))
        context['slots'] = slots
        context['user_slots'] = [slots[i*4:(i+1)*4] for i in range(5)]
        context['admin_user'] = CustomUser.objects.filter(is_admin=True).first()
        return context


def test_view(request):
    # 管理者
    admin_user = CustomUser.objects.filter(is_admin=True).first()

    # スタッフ
    staff_count = 2
    staff_users = list(CustomUser.objects.filter(is_admin=False, is_staff=True)[:staff_count])
    labels = ['スタッフA', 'スタッフB']
    staff_slots = []
    for i in range(staff_count):
        staff = staff_users[i] if i < len(staff_users) else None
        staff_slots.append({
            'user': staff,
            'label': labels[i]
        })

    # 通常ユーザー（is_admin=False, is_staff=False）
    users = list(CustomUser.objects.filter(is_admin=False, is_staff=False).values('id', 'username'))
    slots = users + [None] * (20 - len(users))
    user_slots = [slots[i*4:(i+1)*4] for i in range(5)]

    # JSONとしてJavaScriptに渡す用
    user_slots_json = json.dumps(user_slots, cls=DjangoJSONEncoder)

    return render(request, 'cosapp/dashboard/test.html', {
        'admin_user': admin_user,
        'staff_slots': staff_slots,
        'user_slots': user_slots,             # テンプレート初期描画用
        'user_slots_json': user_slots_json,   # JavaScript用
    })

def dashboard_test2(request):
    admin_user = CustomUser.objects.filter(is_admin=True).first()

    # スタッフ
    staff_count = 2
    staff_users = list(CustomUser.objects.filter(is_admin=False, is_staff=True)[:staff_count])
    labels = ['スタッフA', 'スタッフB']
    staff_slots = []
    for i in range(staff_count):
        staff = staff_users[i] if i < len(staff_users) else None
        staff_slots.append({
            'user': staff,
            'label': labels[i]
        })

    # 通常ユーザー（is_admin=False, is_staff=False）
    users = list(CustomUser.objects.filter(is_admin=False, is_staff=False).values('id', 'username'))
    slots = users + [None] * (20 - len(users))
    user_slots = [slots[i*4:(i+1)*4] for i in range(5)]

    # JSONとしてJavaScriptに渡す用
    user_slots_json = json.dumps(user_slots, cls=DjangoJSONEncoder)

    return render(request, 'cosapp/dashboard/dashboard_test2.html', {
        'admin_user': admin_user,
        'staff_slots': staff_slots,
        'user_slots': user_slots,             # テンプレート初期描画用
        'user_slots_json': user_slots_json,   # JavaScript用
    })

    
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

class SendAdminMessageView(LoginRequiredMixin, FormView):
    login_url = 'admin_login'
    template_name = 'cosapp/dashboard/send_message.html'
    form_class = AdminMessageForm
    success_url = reverse_lazy('dashboard_alt2')

    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        content = form.cleaned_data['content']
        send_to_all = form.cleaned_data['send_to_all_users']
        recipient = form.cleaned_data.get('recipient')

        if send_to_all:
            # 全ユーザーに送信
            for user in CustomUser.objects.filter(is_admin=False):
                AdminMessage.objects.create(
                    recipient=user,
                    subject=subject,
                    content=content
                )
            messages.success(self.request, '全ユーザーにメッセージを送信しました。')
        elif recipient:
            # 単一ユーザーに送信
            AdminMessage.objects.create(
                recipient=recipient,
                subject=subject,
                content=content
            )
            messages.success(self.request, 'メッセージを送信しました。')
        else:
            messages.error(self.request, '受信者を選択してください。')
            return self.form_invalid(form)

        return super().form_valid(form)

    def form_invalid(self, form):
        # フォームが無効な場合のエラーメッセージを追加
        messages.error(self.request, 'フォームにエラーがあります。修正してください。')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = CustomUser.objects.filter(is_admin=False)
        return context


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
            return redirect('dashboard_alt')
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

class AdminMessageHistoryView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = AdminMessage
    template_name = 'cosapp/dashboard/admin_message_history.html'
    context_object_name = 'messages'  # ← 変更
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        user_id = self.request.GET.get('user_id')
        queryset = AdminMessage.objects.all().order_by('-created_at')
        if user_id:
            queryset = queryset.filter(recipient_id=user_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = CustomUser.objects.filter(is_staff=False)  # ドロップダウン用
        context['selected_user_id'] = self.request.GET.get('user_id')
        return context

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin
    