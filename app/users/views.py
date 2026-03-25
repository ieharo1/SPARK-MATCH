from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm, ProfileForm, UserInfoForm
from .models import UserProfile


def register_view(request):
    if request.user.is_authenticated:
        return redirect('discover')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, f'¡Bienvenido/a {user.first_name}! Completa tu perfil para comenzar. 💕')
            return redirect('profile_edit')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('discover')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'¡Hola de nuevo, {user.first_name or user.username}! 👋')
            return redirect('discover')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, '¡Hasta pronto! Vuelve pronto. 👋')
    return redirect('landing')


@login_required
def profile_edit(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserInfoForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, '✅ Perfil actualizado correctamente.')
            return redirect('discover')
    else:
        profile_form = ProfileForm(instance=profile)
        user_form = UserInfoForm(instance=request.user)
    return render(request, 'users/profile_edit.html', {
        'profile_form': profile_form,
        'user_form': user_form,
        'profile': profile,
    })


@login_required
def profile_view(request, user_id=None):
    if user_id:
        profile_user = User.objects.get(id=user_id)
    else:
        profile_user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=profile_user)
    return render(request, 'users/profile_view.html', {
        'profile': profile,
        'profile_user': profile_user,
    })
