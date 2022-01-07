from django.urls import path
from .views import *

urlpatterns=[

 path('custom/', loginView, name="login-user"),    

]