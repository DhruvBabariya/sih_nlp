from django.shortcuts import render,get_object_or_404,redirect  
from django.contrib.auth.models import User

from django.contrib import auth
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            user_form = UserRegisterForm(request.POST)
            email = request.POST['email']
            username = request.POST['username']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if password1 == password2:
                if User.objects.filter(email=email).exists():
                    messages.error(request,'That email is being used')
                    return redirect('register')
                elif User.objects.filter(username=username).exists():
                    messages.error(request,'That username is beign used')
                    return redirect('register')
                
                else:
                    if user_form.is_valid():
                        user = user_form.save()
                        user.save()
                        obj = Delivered(user=user, is_delivered=True)
                        obj.save()
                        return redirect('login')
                    else:
                        messages.error(request,f"least 8 char & don't use commonly used password & don't use entirely numeric.")
                        return redirect('register')
            else:
                messages.error(request,f'Password do not Match!!')
                return redirect('register')

        else:
            user_form = UserRegisterForm()
            
            context ={
                'user_form': user_form
            }
            return render(request, 'accounts/register.html',context=context)


def login(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username,password=password)

            if user is not None:
                auth.login(request,user)
                return redirect('index')
            else:
                messages.error(request,'Invalid Username/Password')
                return redirect('login')
        else:
	        return render(request, 'accounts/login.html') #app_name/template_name.html

@login_required(login_url='/login')
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('login')
    return render(request, 'projects/projects.html')
