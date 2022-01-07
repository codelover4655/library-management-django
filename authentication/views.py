from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.http import Http404





def loginView(request):
    if(request.method == 'POST'):
        
        username = request.POST['user-name']
        password = request.POST['pass-word']
        user=authenticate(request, username=username, password=password)
        if user is not None:
          login(request, user)
          return redirect('../../../')
        else:
            raise Http404("user not found")
    else:
        return render(request,'authentication/customlogin.html')
    
            

def logoutView(request):
    pass

def registerView(request):
    pass