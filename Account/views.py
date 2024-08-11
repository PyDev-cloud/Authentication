from django.shortcuts import render,redirect
from django.contrib import messages
from django.views import generic
from .forms import LoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate,login,logout
from .mixins import LogoutMixins
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
# Create your views here.

@method_decorator(never_cache,name="dispatch")
class home(LoginRequiredMixin,generic.TemplateView):
    login_url='login'
    template_name = "home.html"

    

@method_decorator(never_cache,name="dispatch")
class Login(LogoutMixins,generic.View):
    def get(self,*args, **kwargs):
        form=LoginForm()
        context={
            'form':form
        }
        return render(self.request,'account/login.html',context)
    
    def post(self,*args, **kwargs):
        form=LoginForm(self.request.POST)

        if form.is_valid():
            user=authenticate(
                self.request,
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user:
                login(self.request,user)
                return redirect('home')
            else:
                messages.warning(self.request,"Please Input currect data")
                return redirect('login')
        else:
            messages.warning(self.request,'User not validated')
            return render(self.request,'account/login.html',{'form':form})
        

class Logout(generic.View):
    def get(self,*args, **kwargs):
        logout(self.request)
        return redirect('login')