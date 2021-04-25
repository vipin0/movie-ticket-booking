from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.utils.http import is_safe_url
from django.views.generic import CreateView, FormView

from .forms import LoginForm, RegisterForm


def admin_view(request):
    template_name = 'admin.html'
    if request.user.is_authenticated:
        if request.user.is_admin:
            return render(request, template_name)
        else:
            messages.error(
                request, "You are not authorized to access this page.")
            return redirect('logout')
    else:
        return redirect('login')


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = '/'

    def form_valid(self, form):
        valid = super(RegisterView, self).form_valid(form)
        email, password = form.cleaned_data.get(
            'email'), form.cleaned_data.get('password1')
        new_user = authenticate(email=email, password=password)
        login(self.request, new_user)
        return valid


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    success_url = '/login'

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get("next")
        next_post = request.POST.get("next")
        redirect_path = next_ or next_post or None
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            # print(user)
            login(request, user)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        return self.form_invalid(form)

    def form_invalid(self, form):
        form.add_error(None, "Username and password dont match")
        return super(FormView, self).form_invalid(form)
