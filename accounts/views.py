from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from .forms import UserRegisterForm,UserLoginForm,ProfileEditForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from posts.models import Post
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .models import Relation


class UserRegisterView(View):
    form_class = UserRegisterForm

    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self,request):
        form = self.form_class
        return render(request,'accounts/register.html',{'form':form})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(username=cd['username'],email=cd['email'],password=cd['password1'])
            messages.success(request,'You have successfully registered','success')
            return redirect('home:home')
        
class UserLoginView(View):
    form_class = UserLoginForm

    def setup(self,request,*args,**kwargs):
        self.next = request.GET.get('next')
        return super().setup(request,*args,**kwargs)

    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self,request):
        form = self.form_class
        return render(request,'accounts/login.html',{'form':form})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd['username'],password=cd['password'])
            if user:
                login(request,user)
                messages.success(request,'You have successfully logged in','success')
                if self.next:
                    return redirect(self.next)
                else:
                    return redirect('home:home')
            else:
                messages.error(request,'The username does not match the username','danger')
                return redirect('accounts:login')
                            

class UserLogoutView(LoginRequiredMixin,View):

    def get(self,request):
        logout(request)
        messages.success(request,'You have successfully logged out','success')
        return redirect('home:home')
    
class UserProfileView(LoginRequiredMixin,View):

    def get(self,request,user_id):
        is_following = False
        user = get_object_or_404(User,id=user_id)
        posts = user.posts.all()
        relation = Relation.objects.filter(user_from=request.user,user_to=user).exists()
        if not relation:
            is_following = True
        return render(request,'accounts/profile.html',{'user':user,'posts':posts,'is_following':is_following})
    
class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')

class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')

class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
    

class UserFollowView(View):

    def get(self,request,user_id):
        user = get_object_or_404(User,id=user_id)
        relation = Relation.objects.filter(user_from=request.user).exists()
        if relation:
            messages.error(request,'You have following already this account','danger')
        else:    
            Relation.objects.create(user_from=request.user,user_to=user)
        return redirect('accounts:profile',user.id)
    
class UserUnfollowView(View):

    def get(self,request,user_id):
        user = get_object_or_404(User,id=user_id)
        relation = Relation.objects.filter(user_from=request.user)
        if relation.exists():
            relation.delete()
        else:
            messages.error(request,'You dont follow this account','danger')
        return redirect('accounts:profile',user.id)
    

class ProfileEditView(LoginRequiredMixin,View):
    form_class = ProfileEditForm

    def get(self,request,*args,**kwargs):
        form = self.form_class(instance=request.user.profile,initial={'email':request.user.email,})
        return render(request,'accounts/edit_profile.html',{'form':form})
    
    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST,instance=request.user.profile,initial={'email':request.user.email})
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request,'Your profile edited','success')
            return redirect('accounts:profile',request.user.id)






        