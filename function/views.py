from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render 
from django.contrib import auth
from .models import Post,User,Genre
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import RegisterForm
from django.views import generic
from django.template import RequestContext
from django.db.models import Count,Sum

def index(request):
    #訪問次數
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    post_list = Post.objects.all().order_by('-created_time')
    hot_post = Post.objects.all().order_by('-times')
    #user_list = User.objects.all().order_by('username')
    for i in range(1,Genre.objects.count()+1):
        totals = Genre.objects.get(id=i)
        totals.total = Post.objects.filter(genre_id=i).count()
        totals.save()
    #totals = Post.objects.filter(genre_id=2).count()
    genre = Genre.objects.all()
    '''
    num = Genre.objects.count()
    total = []
    #total = dict()
    for i in range(1,num):
        j = Post.genre.through.objects.filter(genre_id=i).count()
        total.append(j)
    
    #for k in range(len(List)):
        #total[k]=List[k]
    #total = Genre.objects.count()#種類數
    
    #total = Post.genre.through.objects.filter(genre_id=1).count()#該種類下總數'''
    

    return render(request, 'index.html', {'num_visits': num_visits, 'post_list': post_list,'genre':genre,'hot_post':hot_post,'totals':totals})



def post_read(request,pk):
    try:
        genre = Genre.objects.all()
        post = Post.objects.get(pk=pk)
        post.times += 1
        post.save()
    except Post.DoesNotExist:
        raise Http404('Post does not exist')
    return render(request,'postread.html',{'post': post,'genre':genre})


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


def UserHomePage(request):
    return render(request,'userhomepage.html')

#class ContinueRead(generic.DetailView):
    #model = Post
    #template_name = 'postread.html'
    


