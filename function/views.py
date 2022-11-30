from itertools import chain
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render 
from django.contrib import auth
from .models import Post,User,Genre
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import RegisterForm
from django.views import generic
from django.template import RequestContext
from django.db.models import Count,Sum
from django.views.generic.edit import CreateView, UpdateView, DeleteView
#from .forms import PostForm

def index(request):
    #訪問次數
    
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    post_list = Post.objects.all().order_by('-created_time')
    hot_post = Post.objects.all().order_by('-times')
    #user_list = User.objects.all().order_by('username')
    #if request.method == 'POST':
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
    
    return render(request, 'index.html', {'num_visits': num_visits, 'post_list': post_list,'genre':genre,'hot_post':hot_post})



def post_read(request,pk):
    try:
        num_visits = request.session.get('num_visits', 1)
        request.session['num_visits'] = num_visits + 1
        x =[]
        genre = Genre.objects.all()
        post = Post.objects.get(pk=pk)
        post.times += 1
        #post.genre_name = Genre.objects.get(pk=pk)
        post.save()
        genres = Post.objects.values('genre_id').order_by('id')
        for genres in genres:
            genre_get = Genre.objects.order_by('id').filter(id=genres['genre_id'])
            x.append(genre_get)
            #totals = Post.objects.get(genre_id=genres[genre_id])
            #totals.genre_name = x[0][0]
            #totals.save()
        
        for i in range(Post.objects.order_by('id').count()):
            genre_id = list(Post.objects.all().order_by('id'))
            #print(genre_id)
            genre_id = genre_id[i]
            genre_id.genre_name = str(x[i][0])
            genre_id.save()
                

    except Post.DoesNotExist:
        raise Http404('Post does not exist')
    return render(request,'postread.html',{'post': post,'genre':genre,'num_visits':num_visits})


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
    'form': form,
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


#def UserHomePage(request,pk):

    #return render(request,'userhomepage/post_homepage_create.html')

#class ContinueRead(generic.DetailView):
    #model = Post
    #template_name = 'postread.html'
    
i=0
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
import time
class PostCreate(LoginRequiredMixin, CreateView):
    #form_class = PostForm
    model = Post
    fields = ['title','genre','body',]
    #fields= ['title', 'author']
    #initial={'date_of_death':'05/01/2018',}
    template_name = 'userhomepage/post_homepage_create.html'
    success_url = ''
    def form_valid(self, form):
        if self.request.POST:
            pk = self.request.POST
            answer = form.save()
            answer.created_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            
            k = Post.objects.order_by('id').filter(title=pk['title'])[0]
            genre_get = Genre.objects.order_by('id').filter(id=k.genre_id)
            answer.genre_name = str(genre_get[0])
            answer.save()
            #pk.save()
            #post = Post.objects.get(id=pk)
            #if self.request == 'POST':
            #return render(self.request,'index.html')
            return super(PostCreate, self).form_valid(form)
    
    


