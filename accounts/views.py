from random import randint
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.generic import View
from django.core.mail import EmailMultiAlternatives

from adsboard.models import OTPCode
from classifiedads.settings import SERVER_EMAIL
from .forms import SignUpForm


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            otp_code = randint(1000, 9999)
            OTPCode.objects.create(code=otp_code, related_user=user)

            subject = 'Email Confirmation'
            text = f'Your OTP code is: {otp_code}'
            html = f'<b>Your OTP code is: {otp_code}</b>'
            msg = EmailMultiAlternatives(subject, text, from_email=SERVER_EMAIL, to=[user.email])
            msg.attach_alternative(html, 'text/html')
            msg.send()

            return redirect('email_verification', pk=user.pk)
    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})


class EmailVerification(View):
    def get(self, request, pk, **kwargs):
        user = User.objects.get(id=pk)
        return render(request, 'account/email_verification.html', {'user': user})
    def post(self, request, pk, **kwargs):
        entered_code = request.POST.get("code")
        user = User.objects.get(id=pk)
        try:
            otp_code_obj = OTPCode.objects.get(related_user=user)
        except OTPCode.DoesNotExist:
            return redirect("verification_failed")

        user_code = otp_code_obj.code
        if int(entered_code) == user_code:
            otp_code_obj.delete()
            user.is_active = True
            user.save()
            return redirect("successful_verification")
        else:
            return redirect("verification_failed")


def successful_verification(request):
    return render(request, 'account/successful_verification.html')


def verification_failed(request):
    return render(request, 'account/verification_failed.html')


def login_view(request):

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():  
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user) #log the user in
                messages.success(request, f'Welcome {username} !!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request=request, template_name="registration/login.html", context={})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('http://127.0.0.1:8000')
    else:
        return render(request=request, template_name='account/logout.html')


def home(request):
    return render(request=request, template_name='home.html', context={})

