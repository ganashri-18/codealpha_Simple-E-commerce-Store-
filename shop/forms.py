from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        required=True
    )

    class Meta:
        model = User

        fields = [
            "username",
            "email",
            "password1",
            "password2"
        ]


class CheckoutForm(forms.Form):

    address = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Enter your delivery address",
                "rows": 4
            }
        )
    )

    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter phone number"
            }
        )
    )