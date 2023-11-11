from django.contrib.auth import logout, authenticate, login
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'New account "{user.username}" was created successfully.')
            return redirect(reverse('account:login'))

        for error in list(form.errors.values()):
            messages.error(request, error)

    form = UserRegisterForm()
    ctx = {'form': form}
    return render(request, 'account/register.html', ctx)


def login_page(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Dear "{username}"! you have been logged in successfully!')
                return redirect(reverse('index'))

            else:
                messages.error(request, 'username or password is incorrect')
        for error in list(form.errors.values()):
            messages.error(request, error)

    form = UserLoginForm()
    ctx = {'form': form}
    return render(request, 'account/login.html', ctx)


@login_required(login_url='/account/login')
def logout_page(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect(reverse('index'))


def profile(request, id):
    if request.method == 'POST':
        user = request.user
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            user_form = form.save()
            messages.success(request, f'Dear "{user.username}", your profile has been updated successfully!')
            return redirect('account:profile', user_form.id)
        for error in list(form.errors.values()):
            messages.error(request, error)

    user = User.objects.filter(id=id).first()
    if user:
        form = UserUpdateForm(instance=user)
        ctx = {'form': form}
        return render(request, 'account/profile.html', ctx)









