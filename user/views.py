from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View


class CustomLoginView(View):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('product-list')
        else:
            return render(request, self.template_name, {'form': form})

class CustomLogoutView(LogoutView):
    next_page = 'login'

    def get_redirect_url(self):
        return reverse_lazy(self.next_page)