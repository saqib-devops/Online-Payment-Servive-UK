from crispy_forms.helper import FormHelper
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.shortcuts import redirect, render

from register.models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'currency_type']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['currency_type'].widget.attrs.update({"class": "form-control"})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, 'register/signup.html', {'form': form})
