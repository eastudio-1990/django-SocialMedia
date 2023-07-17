from django.shortcuts import render,get_object_or_404
from django.views import View
from .forms import UserRegisterForm,UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .models import Relation
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

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return  super().setup(request, *args, **kwargs)
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
                if self.next:
                    return  redirect(self.next)
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
        is_following = False
        user = get_object_or_404(User, pk=user_id)
        posts = user.posts.all()
        relation = Relation.objects.filter(from_user=request.user,to_user=user)
        if relation.exists():
            is_following = True
        return  render(request, 'account/profile.html', {'user':user, 'posts': posts, 'is_following':is_following})

class UserPasswordResetView(auth_views.PasswordResetView):

    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')
    email_template_name = 'account/password_reset_email.html'

class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'

class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')

class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'

class UserFollowView(LoginRequiredMixin, View):
    def get(self,request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            messages.error(request,'You are already following this user','danger')
        else:
            Relation.objects.create(from_user=request.user,to_user=user)
            messages.success(request, 'You  followed this user', 'success')
        return  redirect('account:user_profile',user_id)

class UserUnFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user,to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request, 'You Unfollowed this user', 'success')
        else:
            messages.error(request, 'You Are Not Following This User', 'error')

        return redirect('account:user_profile',user_id)







