# forms.py
from django import forms
from .models import User

class SignUpForm(forms.ModelForm):    
    user_name = forms.CharField(
        required=True,
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    email = forms.EmailField(
        required=True,
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'Email'})

    )
    password = forms.CharField(
        required=True,
        label="",
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    password_confirm = forms.CharField(
        required=True,
        label="",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = User
        fields = ['user_name', 'email', 'password', ]
        

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")

        return password_confirm
