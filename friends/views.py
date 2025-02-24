from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import logout
from .forms import SignUpForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            
            return redirect(reverse('login'), permanent=True)
    else:
        form = SignUpForm()

    return render(request, 'friends/signup.html', context={
        'form': form,
    })

def user_logout(request):
    logout(request)
    return redirect('home')