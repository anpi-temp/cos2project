from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (AdminView, UserListView, UserCreateView, AdminSetupView, AdminLoginView,
                    UserDeleteView, UserUpdateView, SendAdminMessageView, UserMessageListView, CustomLogoutView,
                    AdminMessageViewSet, ReadMessageListView, AdminMessageHistoryView)

from . import views

router = DefaultRouter()
router.register(r'admin-messages', AdminMessageViewSet, basename='admin-message')

urlpatterns = [
    path('set_up/', AdminSetupView.as_view(), name='admin_setup'),
    path('login/', AdminLoginView.as_view(), name='admin_login'),
    path('logout/', CustomLogoutView.as_view(), name='admin_logout'),
    path('dashboard/', AdminView.as_view(), name='dashboard'),
    path('dashboard/alt/', views.dashboard_alt, name='dashboard_alt'), 
    path('dashboard_alt2/', views.dashboard_alt2, name='dashboard_alt2'), 
    path('dashboard/test/', views.test_view, name='dashboard_test'),
    path('dashboard_test2/', views.dashboard_test2, name='dashboard_test2'),
    path('dashboard/user_list/', UserListView.as_view(), name='user_list'),
    path('dashboard/user_create/', UserCreateView.as_view(), name='user_create'),
    path('dashboard/user_delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('dashboard/user_edit/<int:pk>/', UserUpdateView.as_view(), name='user_edit'),
    path('dashboard/send_message/', SendAdminMessageView.as_view(), name='send_admin_message'),
    path('dashboard/admin_message_history/', AdminMessageHistoryView.as_view(), name='admin_message_history'),
    path('user/message_list/<int:user_id>/', UserMessageListView.as_view(), name='message_list'),
    path('read_message_list/<int:user_id>/', ReadMessageListView.as_view(), name='read_message_list'),
    path('api/', include(router.urls)),
]