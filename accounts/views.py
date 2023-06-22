from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, redirect
from django.contrib import messages


from .forms import RegistrationForm, UpdateProfileForm
from .models import AuthUsers


def register(request):
    if request.user.is_authenticated:
        print(request.user)
        return redirect('home_page')

    form = RegistrationForm(request.POST)
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save(request)
            phone = form.cleaned_data.get('phone').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(phone=phone, password=raw_password)
            login(request, account)
            messages.success(request, f"Account was created!")
            return redirect('home_page')

        else:
            form = RegistrationForm()

    context = {
        'form': form
    }
    template_name = 'pages/registration.html'
    return render(request, template_name, context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home_page')

    template_name = 'pages/login.html'
    auth = None

    if request.POST:
        phone = request.POST.get("phone").lower()
        passwd = request.POST.get("password")

        try:
            auth = AuthUsers.objects.get(phone=phone)
        except Exception as e:
            print(e)
            messages.error(request, 'Username does not exist')

        if auth is not None:
            try:
                user = AuthUsers.objects.get(phone=auth.phone)
                auth_user = authenticate(
                    request, username=user.phone, password=passwd)

                if auth_user is not None:
                    login(request, auth_user)
                    return redirect(request.GET['next'] if 'next' in request.GET else 'home_page')

                else:
                    messages.error(
                        request, 'Username OR password is incorrect')
            except Exception as e:
                print(e)
                messages.error(request, 'Username OR password is incorrect')

    return render(request, template_name, {})


@login_required
def logout_user(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('home_page')


@login_required
def profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=request.user)

        if form.is_valid():

            form.save()
            messages.success(request, _("Your profile has been saved successfully!"))
