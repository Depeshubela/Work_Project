
from django.urls import path
from . import views

#瀏覽器網址由此定義，修改此便改變
urlpatterns = [
    #path('index/',views.Index.as_view(),name='index'),
    path('index/',views.index,name='index'),
    #path('homepage/<int:pk>',views.UserHomePage,name='userhomepage'),
    path('homepage/<int:pk>',views.PostCreate.as_view(),name='userhomepage'),
    path('post/<int:pk>',views.post_read,name='post-id'),
]