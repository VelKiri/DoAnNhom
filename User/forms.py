from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser
from django.core.validators import FileExtensionValidator

class UserRegisterForm(forms.ModelForm):
    password =forms.CharField(widget=forms.PasswordInput,max_length=10)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email','password','confirm_password','avatar','first_name','last_name','id_country']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Email da ton tai.')
        return email
    
    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size >1024*1024:
                raise ValidationError("Anh phai nho hon 1MB")
            if not avatar.name.lower().endswith(('.png','.jpg','.jpeg')):
                raise ValidationError("Anh phai co dinh dang jpg,jpeg hoac png")
        return avatar
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Mat khau xac nhan khong khop ")
        return cleaned_data