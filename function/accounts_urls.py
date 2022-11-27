
from django.urls import path
from . import views

#瀏覽器網址由此定義，修改此便改變
urlpatterns = [
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('logout/', views.log_out, name='logout')
]   