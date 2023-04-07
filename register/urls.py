from register.views import signup

app_name = 'register'
from django.contrib.auth import views as auth_views
from django.urls import path
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='register/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'register/logout.html'), name='logout'),
    path('signup/', signup, name='signup'),

    ]
