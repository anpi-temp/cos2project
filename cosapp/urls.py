from django.urls import path
from .views import (AdminView, UserListView, UserCreateView, AdminSetupView, AdminLoginView, 
                    UserDeleteView, UserUpdateView, SendAdminMessageView, UserMessageListView, CustomLogoutView)

urlpatterns = [
    path('set_up/', AdminSetupView.as_view(), name='admin_setup'),
    path('login/', AdminLoginView.as_view(), name='admin_login'),
    path('logout/', CustomLogoutView.as_view(), name='admin_logout'),
    path('dashboard/', AdminView.as_view(), name='dashboard'),
    path('dashboard/user_list/', UserListView.as_view(), name='user_list'),
    path('dashboard/user_create/', UserCreateView.as_view(), name='user_create'),
    path('dashboard/user_delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('dashboard/user_edit/<int:pk>/', UserUpdateView.as_view(), name='user_edit'),
    path('dashboard/send_message/', SendAdminMessageView.as_view(), name='send_admin_message'),
    path('user/message_list/', UserMessageListView.as_view(), name='message_list'),
]