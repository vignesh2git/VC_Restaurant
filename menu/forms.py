from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (css + ' form-control').strip()
            # set sensible placeholders
            if name == 'username':
                field.widget.attrs.setdefault('placeholder', 'Username')
            elif name == 'email':
                field.widget.attrs.setdefault('placeholder', 'Email (optional)')
            elif name == 'password1':
                field.widget.attrs.setdefault('placeholder', 'Password')
            elif name == 'password2':
                field.widget.attrs.setdefault('placeholder', 'Confirm password')

