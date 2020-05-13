from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_POST
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:home')
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Welcome! Please login.')
            return redirect('movies:home')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('movies:home')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            messages.add_message(request, messages.INFO, "You've been successfully logged in")
            return redirect(request.GET.get('next') or 'movies:home')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)



@login_required
def logout(request):
    auth_logout(request)
    messages.add_message(request, messages.SUCCESS, "You've been logged out.")
    return redirect('movies:home')


def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('movies:home')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context ={
        'form':form
    }
    return render(request, 'accounts/update.html', context)


@require_POST
@login_required
def delete(request):
    request.user.delete()
    messages.add_message(request, messages.DANGER, "Your account has been deleted.")
    return redirect('movies:home')