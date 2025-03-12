from django.contrib.auth.forms import forms
from .models import CustomUser, AdminMessage, CustomAdmin

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
        fields = ['recipient', 'subject']

class AdminRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomAdmin
        fields = ['username', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data