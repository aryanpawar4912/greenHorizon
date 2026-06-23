from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, ContactMessage, Donation, Volunteer


class SignupForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username',
        })
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
        })
    )
    password2 = forms.CharField(
        label="Confirm Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password',
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'form-control',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-control',
        })
    )


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'full_name', 'mobile', 'email',
            'profile_photo', 'interests', 'gender',
            'address', 'birthday'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name',
            }),
            'mobile': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your mobile number',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email',
            }),
            'profile_photo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'interests': forms.Select(attrs={
                'class': 'form-select',
            }),
            'gender': forms.RadioSelect(attrs={
                'class': 'form-check-input',
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Enter your address',
            }),
            'birthday': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UpdateProfileForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.user:
            profile.user = self.user
        if commit:
            profile.save()
        return profile


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['name', 'email', 'amount']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter donation amount'}),
        }


class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ['name', 'email', 'phone', 'interest']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'interest': forms.Select(attrs={'class': 'form-select'}),
        }


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': True}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'required': True}),
        }


from django import forms
from .models import MobileApp

class MobileAppForm(forms.ModelForm):
    class Meta:
        model = MobileApp
        fields = ['apk_file', 'version', 'release_notes']
        widgets = {
            'apk_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'version': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 1.0.3'}),
            'release_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe changes...'}),
        }
