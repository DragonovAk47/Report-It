from django.conf.urls import url
from django.urls import path
from userapp import views


         

#TEMPLATES URLS!
# app_name='userapp'
# appname variable

urlpatterns=[

path('register/',views.register,name='register'),
path('withlogin/',views.withlogin, name= 'withlogin'),
path('user_login/',views.user_login,name='user_login'),
path('logout/',views.user_logout,name='user_logout'),

]
