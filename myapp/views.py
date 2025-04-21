from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import loginForm, registerForm, forgotForm
from .models import Account

# Create your views here.

def home(request):
    return render(request, 'myapp/home.html')

def login(request):
    if request.session.get('logged_in'):
        if request.session.get('username') == 'admin':
            return redirect('Admin')
        else:
            return redirect('User')
    notice = None
    if request.method == "POST":
        form =  loginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            try:
                user = Account.objects.get(username=username)
                if password == user.password:
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username
                    request.session['logged_in'] = True
                    if user.username == 'admin':
                        return redirect('Admin')
                    else:
                        return redirect('User')
                else:
                    if notice == None:
                        notice = "Sai tên đăng nhập hoặc mật khẩu!"
            except Account.DoesNotExist:
                if notice == None:
                    notice = "Sai tên đăng nhập hoặc mật khẩu!"
        return render(request, 'myapp/login.html', {'form': form, 'notice': notice})
    else:
        form = loginForm()
        return render(request, 'myapp/login.html', {'form': form})

def register(request):
    notice = None
    if request.method == "POST":
        form =  registerForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')

            if Account.objects.filter(username=username).exists():
                if notice == None:
                    notice = "Sử dụng tên đăng nhập khác"
            elif Account.objects.filter(email=email).exists():
                if notice == None:
                    notice = "Email này đã được sử dụng"
            else:
                user = Account(username=username, email=email, password=password)
                user.save()
                if notice == None:
                    notice = "Tạo tài khoản thành công"
                return redirect('Login')
        return render(request, 'myapp/register.html', {'form': form, 'notice': notice})
    else:
        form = registerForm()
        return render(request, 'myapp/register.html', {'form': form})

def forgot(request):
    if request.method == "POST":
        form =  forgotForm(request.POST)
        notice = None
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            try:
                user = Account.objects.get(username=username)
                if email != user.email:
                    if notice == None:
                        notice = "Tên đăng nhập hoặc email không đúng"
                        return render(request, 'myapp/forgot.html', {'form': form, 'notice': notice})
                else:
                    message = f"Mật khẩu của bạn là: {user.password}"
                    return render(request, 'myapp/forgot.html', {'form': form, 'message': message})
            except Account.DoesNotExist:
                if notice == None:
                    notice = "Tên đăng nhập hoặc email không đúng"
        return render(request, 'myapp/forgot.html', {'form': form, 'notice': notice})
    else:
        form = forgotForm()
        return render(request, 'myapp/forgot.html', {'form': form})

def user(request):
    if request.session.get('logged_in') and request.session.get('username') != 'admin':
        name = request.session.get('username')
        return render(request, 'myapp/user.html', {'name': name})
    else:
        return redirect('Home')

def logout(request):
    if request.method == "POST":
        request.session.flush() 
        return redirect('Home') 

def admin(request):
    if request.session.get('logged_in') and request.session.get('username') == 'admin':
        name = request.session.get('username')
        users = Account.objects.all()
        return render(request, 'myapp/admin.html', {'name': name, 'users': users})
    else:
        return redirect('Home')