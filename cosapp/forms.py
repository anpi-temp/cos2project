from django.contrib.auth.forms import forms
from .models import CustomUser, AdminMessage

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number']
        
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
        fields = ['recipient', 'subject']