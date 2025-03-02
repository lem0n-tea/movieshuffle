from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import LogInForm
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(authentication_form=LogInForm, template_name='friends/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', views.user_logout, name='logout'),
]
