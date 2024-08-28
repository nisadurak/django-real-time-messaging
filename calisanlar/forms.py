from django import forms
from django.contrib.auth.models import User
from .models import Calisan

class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User  # Kayıt formunun temel alacağı model
        fields = ['email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Unicode karakterlerle eşleşme kontrolü yapılacak
        if not Calisan.objects.filter(mail=email).exists():
            raise forms.ValidationError("Bu email ile kayıtlı bir çalışan bulunamadı.")
        return email

    def save(self, commit=True):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = User.objects.create_user(username=email, email=email, password=password)
        return user
