from django.shortcuts import render
from django.views import View
from .forms import UserRegisterForm,UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.mixins import LoginRequiredMixin

class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'account/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['email'], cd['username'], cd['password'])
            messages.success(request, 'You Register SuccessFully!', 'success')
            return redirect('home:home')
        return render(request, self.template_name, {'form': form})





class UserLoginView(View):

    form_class = UserLoginForm
    template_name = 'account/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self,request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password= cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'Login SuccessFully', 'success')
                return  redirect('home:home')

            messages.error(request, 'UserName Or Password Is Wrong!', 'warning')
        return render(request, self.template_name, {'form':form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self,request):
        logout(request)
        messages.success(request, 'Logout SuccessFully', 'success')
        return redirect('home:home')



class UserProfileView(LoginRequiredMixin,View):
    def get(self,request,user_id):
        user = User.objects.get(pk=user_id)
        return  render(request, 'account/profile.html', {'user':user})