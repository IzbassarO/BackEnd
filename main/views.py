#Assignment 4
#Web Technologies 2 (Back-End)
#Learn about Encryption and use encryption to keep your database secure
#Learn and implement Hashing and Salting with bcrypt
#Using Sessions and Cookies to persist user log in sessions
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
#for encryption
from django.contrib.auth.hashers import make_password
from django.contrib import messages
#models
from .models import Main
from .models import Student
from .models import FacultyMember
from .models import Course
from .models import NewsArticle
from .models import Department
# Create your views here.
#--------------------  api  --------------------------



def home(request):
    
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
    if request.method  == 'POST' :
        
        utxt = request.POST.get('username', '')
        ptxt = request.POST.get('password', '')

        user = authenticate(username=utxt, password=ptxt)
        hash_password = make_password(ptxt)
        user = User.objects.get(username=utxt)

        if request.user.is_superuser:
            # Redirect to the admin panel
            return redirect('panel')
        else:
            if utxt != "" and ptxt != "" and user is not None:
                auth_login(request, user)
                return redirect('home')
    
    sitename = "Login Page"
    
    return render(request, 'front/login.html', {'sitename': sitename, 'active': active})

def mylogout(request):
    
    logout(request)
    
    return redirect('login')

def delete_news_article(request, article_id):
    article = NewsArticle.objects.get(pk=article_id)
    
    if request.method == 'POST':
        article.delete()
        return redirect('site_setting')  # Redirect to the main settings page after deleting

    return render(request, 'back/site_setting.html', {'article': article})

def site_setting(request):
    
    #login check start
    if not request.user.is_authenticated :
        return redirect('login')
    #login check end
    
    Main.objects.filter(pk=1)    
    news_articles1 = NewsArticle.objects.filter(pk=1)
    news_articles2 = NewsArticle.objects.filter(pk=2)
    news_articles3 = NewsArticle.objects.filter(pk=3)
    
    return render(request, 'back/site_setting.html', {'one':news_articles1, 'two':news_articles2, 'three':news_articles3})

def register(request):
    
    if request.method == 'POST':
        
        uname =request.POST.get('uname')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2 :
            msg = "Your Pass Didn't Match"
            print(msg)
        else :

        #POST
            if len(User.objects.filter(username=uname)) == 0 and len(User.objects.filter(email=email)) == 0 :
                hash_password = make_password(password1)
                user = User.objects.create_user(username=uname, email=email, password=hash_password)
                auth_login(request, user)
                return redirect('login')
    
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
                error = "Your Password Must Be At Least 2"
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

@user_passes_test(lambda u: u.is_superuser)
@login_required
def delete_person(request, pk):
    if request.method == 'POST':
        user_to_delete = get_object_or_404(User, pk=pk)
        if request.user.is_authenticated :
            user_to_delete.delete()
    return redirect('profile')

@user_passes_test(lambda u: u.is_superuser)
@login_required
def edit_person(request, pk):
    if request.method == 'POST':
        new_username = request.POST.get('new_username')
        user_to_edit = get_object_or_404(User, pk=pk)
        user_to_edit.username = new_username
        user_to_edit.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def profile(request):
    #login check start
    try:
        data = get_object_or_404(User, id=id)
    except Exception:
        print('error')
    
    
    if request.method == 'POST':
        data.delete()
        objs = User.objects.all()
        return redirect('back/profile.html', {'objs' : objs})
    else:
        objs = User.objects.all()
        return render(request, 'back/profile.html', {'objs' : objs})

def user_page(request):
    #login check start
    if not request.user.is_authenticated :
        return redirect('login')
    #login check end
    
    
    return render(request, 'front/user.html', {'objs': request.user})