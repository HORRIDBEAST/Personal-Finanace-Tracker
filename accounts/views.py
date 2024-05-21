from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout as auth_logout
from .models import Feature
def index(request):
    
    features = Feature.objects.all()
    return render(request , 'index.html', {'features':features} )

def counter(request):
    posts=[1,2,3,4,'Horrid','Beast']
    return render(request, 'counter.html' , {'posts': posts})


def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        gender = request.POST.get('gender')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        agreed_to_terms = request.POST.get('agreed_to_terms')

        if password == confirm_password:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already used')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already used')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                # Save additional user information if necessary
                user.save()
                messages.success(request, 'Registration successful. You can now login.')
                return redirect('login')
        else:
            messages.error(request, "Passwords do not match")
            return redirect('register')

    return render(request, 'register.html')

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username , password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else :
            messages.info(request,'Credentials,invlid')
            return redirect('login')

    else :return render(request, 'login.html')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')

def post(request, id):
    return render(request, 'post.html' ,{'id':id})
