import logging

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm, UserProfileEditForm
from authapp.models import User
from basketapp.models import Basket

from django.views.generic.edit import FormView


class Login(FormView, backend='django.contrib.auth.backends.ModelBackend'):
    form_class = UserLoginForm
    template_name = 'authapp/login.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(Login, self).get_context_data()
        context.update({'title': 'GeekShop - Авторизация'})
        return context

    def form_valid(self, form):
        username = self.request.POST['username']
        password = self.request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(self.request, user)
            return HttpResponseRedirect(self.get_success_url())


class Register(FormView):
    form_class = UserRegisterForm
    template_name = 'authapp/register.html'
    success_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super(Register, self).get_context_data()
        context.update({'title': 'GeekShop - Регистрация'})
        return context

    def form_valid(self, form):
        user = form.save()
        if send_verify_link(user):
            logging.debug('sent successful')
        else:
            logging.error('sent failed')
        messages.success(self.request, 'Вы успешно зарегистрировались!')
        return HttpResponseRedirect(self.get_success_url())


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        profile_form = UserProfileEditForm(data=request.POST, instance=request.user.userprofile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)
        profile_form = UserProfileEditForm(instance=request.user.userprofile)

    context = {
        'title': 'GeekShop - Личный кабинет',
        'form': form,
        'baskets': Basket.objects.filter(user=request.user),
        'profile_form': profile_form,
    }
    return render(request, 'authapp/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def send_verify_link(user):
    verify_link = reverse('users:verify', args=[user.email, user.activation_key])
    subject = 'Account verify'
    message = f'Your link for account activation: {settings.DOMAIN_NAME}{verify_link}'
    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, key):
    user = User.objects.filter(email=email).first()
    if user and user.activation_key == key and not user.is_activation_key_expired():
        user.is_active = True
        user.activation_key = ''
        user.activation_key_created = None
        user.save()
        auth.login(request, user)
    return render(request, 'authapp/verify.html')
