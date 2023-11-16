from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
#start for encryption
from django.contrib.auth.hashers import make_password
#end
from django.contrib import messages
#models
from .models import Main
from .models import Student
from .models import FacultyMember
from .models import Course
from .models import NewsArticle
from .models import Department

def home(request):
    
    #login check start
    if request.session.get('user_logged_in') or request.session.get('admin_logged_in'):
        sitename = "Main Page"
        active = "active"
        site1 = Main.objects.filter(pk=1)    
        site2 = Main.objects.filter(pk=2)
        site3 = Main.objects.filter(pk=3)
        site4 = Main.objects.filter(pk=4)
        site5 = Main.objects.filter(pk=5)
        return render(request, 'front/home.html', {'sitename':sitename, 'site1':site1, 'site2':site2, 'site3':site3, 'site4': site4, 'site5': site5, 'active':active})
    else:
        return redirect('login')

def about(request):
    
    if request.session.get('user_logged_in') or request.session.get('admin_logged_in'):
        # User is logged in, proceed with the view logic.
        sitename = "About Page"
        active = "active"
        return render(request, 'front/about.html', {'sitename': sitename, 'active':active})
    else:
        # User is not logged in, redirect them to the login page.
        return redirect('login')

def panel(request):
    
    if request.session.get('admin_logged_in'):
        num = User.objects.all().count
        last_login = User.objects.get(username="admin")
        return render(request, 'back/home.html', {'num' : num, 'obj' : last_login})
    else:
        return redirect('login')

def login(request):
    if request.method  == 'POST' :
        
        utxt = request.POST.get('username', '')
        ptxt = request.POST.get('password', '')

        user = authenticate(username=utxt, password=ptxt)
        userData = User.objects.get(username=utxt)
        
        if user:
            auth_login(request, user)
            request.session['site_settings'] = True
            
            
            if request.user.is_superuser:
                # Redirect to the admin panel
                request.session['admin_logged_in'] = True
                return redirect('panel')
            else:
                # Set a session variable to indicate the user is logged in
                request.session['user_logged_in'] = True
                request.session.set_expiry(30)
                print("HEYYYYYYYYYY USER LOGGED IN")
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password. Please try again')
            return redirect('login')
    
    sitename = "Login Page"
    active = "active"
    return render(request, 'front/login.html', {'sitename': sitename, 'active': active})

def mylogout(request):
    
    logout(request)
    request.session['admin_logged_in'] = False
    request.session['user_logged_in'] = False
    request.session['site_settings'] = False
    
    return redirect('login')

def delete_news_article(request, article_id):
    article = NewsArticle.objects.get(pk=article_id)
    
    if request.method == 'POST':
        article.delete()
        return redirect('site_setting')  # Redirect to the main settings page after deleting

    return render(request, 'back/site_setting.html', {'article': article})

def site_setting(request):
    
    if request.session.get('user_logged_in') or request.session.get('admin_logged_in'):
        Main.objects.filter(pk=1)    
        news_articles1 = NewsArticle.objects.filter(pk=2)
        news_articles2 = NewsArticle.objects.filter(pk=3)
        news_articles3 = NewsArticle.objects.filter(pk=4)
        
        request.session['default_font'] = request.COOKIES.get('font-size', 'medium')  # Default to 'medium' if not set
        request.session['default_foreground'] = request.COOKIES.get('font-color', 'black')
        request.session['default_background'] = request.COOKIES.get('bg-color', 'white')
        
        if request.method == 'POST':
            
            font = request.POST.get('font-size')
            background = request.POST.get('bg-color')
            foreground = request.POST.get('font-color')
            
            request.session['font'] = font 
            request.session['background'] = background
            request.session['foreground'] = foreground
            context = {
                'one': news_articles1,
                'two': news_articles2,
                'three': news_articles3,
                'font_size': font,
                'bg_color': background,
                'font_color': foreground
            }
            # Set user preferences as cookies with an expiration time (e.g., 30 days)
            response = render(request, 'back/site_setting.html')
            response.set_cookie('font_size', font, max_age=30 * 24 * 60 * 60, secure=True)  # 30 days
            response.set_cookie('bg_color', background, max_age=30 * 24 * 60 * 60, secure=True)  # 30 days
            response.set_cookie('font_color', foreground, max_age=30 * 24 * 60 * 60, secure=True)  # 30 days
            
            return render(request, 'back/site_setting.html', context)
        
        font = request.session.get('font', 'default_font')  # 'default_font' is a placeholder for your actual default value
        background = request.session.get('background', 'default_background')
        foreground = request.session.get('foreground', 'default_foreground')
        
        context = {
            'one': news_articles1,
            'two': news_articles2,
            'three': news_articles3,
            'font_size': font,
            'bg_color': background,
            'font_color': foreground,
        }
        
        return render(request, 'back/site_setting.html', context)
    else:
        return redirect('login')

def register(request):
    
    if request.method == 'POST':
        
        uname =request.POST.get('uname')
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        
        if password1 != password2 :
            msg = "Your Pass Didn't Match"
            print(msg)
        else :

        #POST
            if len(User.objects.filter(username=uname)) == 0 and len(User.objects.filter(email=email)) == 0 :
                #bcrypt encryption
                hash_password = make_password(password1)
                
                User.objects.create_user(username=uname, email=email, password=hash_password, first_name = fname, last_name = lname)
                
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
    if request.session.get('user_logged_in') or request.session.get('admin_logged_in'):

        if request.method == 'POST' :
            oldpass = request.POST.get('oldpass')
            newpass = request.POST.get('newpass')
        
            user = authenticate(username=request.user.username, password=oldpass)
        
            if user != None :
            
                user.set_password(newpass)
                user.save()

                logout(request=request)
            
                return redirect('logout')
        return render(request, 'back/changepass.html')
    else:
        return redirect('login')

#only admin has permission to edit
@user_passes_test(lambda u: u.is_superuser)
@login_required
def delete_person(request, pk):
    if request.method == 'POST':
        user_to_delete = get_object_or_404(User, pk=pk)
        if request.user.is_authenticated :
            user_to_delete.delete()
    return redirect('profile')

#only admin has permission to edit
@user_passes_test(lambda u: u.is_superuser)
@login_required
def edit_person(request, pk):
    if request.method == 'POST':
        new_username = request.POST.get('new_username')
        user_to_edit = get_object_or_404(User, pk=pk)
        user_to_edit.username = new_username
        user_to_edit.save()
        #Return a success message to display in the template
        success_message = f"Successfully saved username {new_username}"
        return JsonResponse({'success': True, 'message': success_message})
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
    if request.session.get('user_logged_in'):
        return render(request, 'front/user.html', {'objs': request.user})
    else:
        return redirect('login')