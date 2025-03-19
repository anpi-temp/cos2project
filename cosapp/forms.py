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
        
class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number']
        labels = {
            'username': 'ユーザー名',
            'phone_number': '電話番号',
        }

class AdminMessageForm(forms.ModelForm):
    class Meta:
        model = AdminMessage
        fields = ['recipient', 'subject', 'content']  # contentを追加

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recipient'].queryset = CustomUser.objects.filter(is_admin=False)
        
        # contentフィールドのカスタマイズ（オプション）
        self.fields['content'].widget = forms.Textarea(attrs={
            'rows': 5,
            'placeholder': 'メッセージ本文を入力してください'
        })
        self.fields['content'].label = "本文"

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