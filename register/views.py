from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from register.forms import SignUpForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect("payapp:dashboard")
    else:
        form = SignUpForm()
    return render(request, 'register/signup.html', {'form': form})

