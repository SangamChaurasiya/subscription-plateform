from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from .token import user_tokenizer_generate
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser


def home(request):
    return render(request, 'account/index.html')


def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            user = form.save()

            user.is_active = False
            user.save()

            # Email Verification Config
            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('account/email-verification.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_tokenizer_generate.make_token(user),
            })

            user_email = user.email

            send_mail(subject=subject, message=message, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[user_email])

            return redirect('email-verification-sent')
        
    context = {'RegisterForm': form}
    return render(request, 'account/register.html', context=context)


def my_login(request):
    form = AuthenticationForm()

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username') # Username / Email
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_writer == True:
                login(request, user)
                return redirect('writer:dashboard')
            
            if user is not None and user.is_writer == False:
                login(request, user)
                return redirect('client:dashboard')

    context = {'LoginForm': form}
    return render(request, 'account/my-login.html', context)


def user_logout(request):
    logout(request)
    
    return redirect('my-login')


def email_verification(request, uidb64, token):
    unique_token = force_str(urlsafe_base64_decode(uidb64))
    custom_user = CustomUser.objects.get(pk=unique_token)

    if custom_user and user_tokenizer_generate.check_token(custom_user, token):
        custom_user.is_active = True
        custom_user.save()

        return redirect('email-verification-success')
    else:
        return redirect('email-verification-failed')


def email_verification_sent(request):
    return render(request, 'account/email-verification-sent.html')


def email_verification_success(request):
    return render(request, 'account/email-verification-success.html')


def email_verification_failed(request):
    return render(request, 'account/email-verification-failed.html')
