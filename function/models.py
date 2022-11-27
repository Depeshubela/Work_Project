from django.db import models
from django.contrib.auth.models import (
	 BaseUserManager, AbstractBaseUser	)
from django.urls import reverse

class Genre(models.Model):
    name = models.CharField(max_length=200)
    total = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return self.name



#使用者資料
class Post (models.Model):
    title = models.CharField(max_length=20)
    author = models.CharField(max_length=20,default=None)
    genre = models.ForeignKey(Genre,on_delete=models.SET_NULL, null=True, help_text='Select a genre for this book')
    body = models.TextField(max_length=999,default="")
    created_time = models.DateTimeField(null=True, blank=True)
    modified_time = models.DateTimeField(null=True, blank=True)
    times = models.IntegerField(default=0)
    def __str__(self):
        return self.title

        #回傳一個存取此資料的url給html
    def get_absolute_url(self):
        #reverse實現動態網址，urls.py改變即可變全部
        return reverse('post-id', args=[str(self.id)]) 


    
#繼承django預設的的使用者介面並更改用戶創建資料
class AccountManager(BaseUserManager):
    
    def create_user(self, email, date_of_birth, password=None):
    
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, date_of_birth, password=None):
    
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
#定義用戶模型
class User(AbstractBaseUser):
        username = models.CharField(unique=True,max_length=20,default="")
        email = models.EmailField()
        date_of_birth = models.DateField()
        date_joined = models.DateTimeField(auto_now_add=True)
        last_login = models.DateTimeField(auto_now=True)
        is_admin = models.BooleanField(default=False)
        is_active = models.BooleanField(default=True)
        objects = AccountManager()
        USERNAME_FIELD = 'username' #類似主鍵的功用
        REQUIRED_FIELDS = ['email','username'] #必填
    
        def __str__(self):
            return self.email
    
        def is_staff(self):
            return self.is_admin
    
        def has_perm(self, perm, obj=None):
            return self.is_admin
            
        def has_module_perms(self, app_label):
            return self.is_admin