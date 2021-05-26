from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from basketapp.models import Basket

from django.views.generic.edit import FormView


class Login(FormView):
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
        form.save()
        messages.success(self.request, 'Вы успешно зарегистрировались!')
        return HttpResponseRedirect(self.get_success_url())


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)
    context = {
        'title': 'GeekShop - Личный кабинет',
        'form': form,
        'baskets': Basket.objects.filter(user=request.user),
    }
    return render(request, 'authapp/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))