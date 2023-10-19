from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

#models
from .models import Main
from .models import Student
from .models import FacultyMember
from .models import Course
from .models import NewsArticle
from .models import Department
# Create your views here.

@login_required
def home_auth(request):
    
    #login check start
    if not request.user.is_authenticated :
        return redirect('login')
    #login check end
    
    
    sitename = "Main Page"
    active = "active"
    site1 = Main.objects.filter(pk=1)    
    site2 = Main.objects.filter(pk=2)
    site3 = Main.objects.filter(pk=3)
    site4 = Main.objects.filter(pk=4)
    site5 = Main.objects.filter(pk=5)
    return render(request, 'front/home.html', {'sitename':sitename, 'site1':site1, 'site2':site2, 'site3':site3, 'site4': site4, 'site5': site5, 'active':active})

def home_not_auth(request) :
    return render(request, 'front/login.html')

def about(request):
    
    #login check start
    if not request.user.is_authenticated :
        return redirect('login')
    #login check end
    
    sitename = "About Page"
    active = "active"
    return render(request, 'front/about.html', {'sitename': sitename, 'active':active})

def panel(request):
    
    #login check start
    if not request.user.is_authenticated :
        return redirect('login')
    #login check end
    
    return render(request, 'back/home.html')

def login(request):
    active = "active"
    #GET
    if request.method  == 'POST' :
        
        utxt = request.POST.get('username', '')
        ptxt = request.POST.get('password', '')
        if utxt == "admin" and ptxt == "0000":
            # Redirect to the admin panel
            return redirect('panel')
        else:
            user = authenticate(username=utxt, password=ptxt)
            
            if utxt != "" and ptxt != "" and user is not None:
                auth_login(request, user)
                return redirect('home')
    
    sitename = "Login Page"
    
    return render(request, 'front/login.html', {'sitename': sitename, 'active': active})

def mylogout(request):
    
    logout(request)
    
    return redirect('login')

def site_setting(request):
    
    return render(request, 'back/site_setting.html')

def register(request):
    
    if request.method == 'POST':
        
        uname =request.POST.get('uname')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2 :
            msg = "Your Pass Didn't Match"
            print(msg)
        
        #POST
        if len(User.objects.filter(username=uname)) == 0 and len(User.objects.filter(email=email)) == 0 :
            
            user = User.objects.create_user(username=uname, email=email, password=password1)
    
    sitename = "Register Page"
    active = "active"
    return render(request, 'front/register.html', {'sitename': sitename, 'active':active})

def tables(request):
    
    return render(request, 'back/tables.html')

def charts(request):
    
    return render(request, 'back/charts.html')

def error(request):
    
    return render(request, 'back/error.html')

def change_pass(request): 
    
    #login check start
    if not request.user.is_authenticated :
        return redirect('login')
    #login check end
    
    #GET
    if request.method == 'POST' :
        oldpass = request.POST.get('oldpass')
        newpass = request.POST.get('newpass')
        
        if oldpass == "" or newpass == "":
            error = "All Fields Required"
            print(error)
        
        user = authenticate(username=request.user, password=oldpass)
        
        if user != None :
            
            if len(newpass) < 2 :
                error = "Your Password Must Be At Least 3"
                print(error)
            #GET
            
            user = User.objects.get(username=request.user)
            user.set_password(newpass)
            user.save()
            return redirect('logout')
            
        else :
            error = "Your Password IS Not Correct"
            print(error)
            
    return render(request, 'back/changepass.html')
