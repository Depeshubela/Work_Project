from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from .models import Post,User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import RegisterForm
from django.views import generic



def index(request):
    #訪問次數
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    post_list = Post.objects.all().order_by('-created_time')
    #user_list = User.objects.all().order_by('username')
    return render(request, 'index.html', {'num_visits': num_visits, 'post_list': post_list})



def login(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request,username=username,password=password)
        if user is not None and user.is_active:
            auth.login(request,user)
            return HttpResponseRedirect('/index')
    context = {
    'form': form
    }   
    return render(request, 'login.html', context)

def log_out(request):
    auth.logout(request)
    return HttpResponseRedirect('/accounts/login')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/index')
    else:
        form = RegisterForm()
        
    context = {'form': form}
    return render(request, 'register.html', context)


