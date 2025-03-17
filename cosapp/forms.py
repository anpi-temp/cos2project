from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser, AdminMessage

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number']
        labels = {
            'username': 'ユーザー名',
            'phone_number': '電話番号',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_admin = False  # 明示的にis_adminをFalseに設定
        if commit:
            user.save()
        return user
        
class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number']
        labels = {
            'username': 'ユーザー名',
            'phone_number': '電話番号',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 管理者のユーザー名をデフォルト値から除外
        if 'username' in self.fields:
            self.fields['username'].initial = ''

class AdminMessageForm(forms.ModelForm):
    class Meta:
        model = AdminMessage
        fields = ['recipient', 'subject']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recipient'].queryset = CustomUser.objects.filter(is_admin=False)

class AdminRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        user.is_admin = True
        if commit:
            user.save()
        return user