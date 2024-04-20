from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def auth_login(request):

    if request.method == 'POST':
        # login request received
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            # successful authentication. Login user
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'blogapi_auth/login.html', {'error_message':error_message})


    return render(request, 'blogapi_auth/login.html')

def auth_signup(request):

    if request.method == 'POST':
        # user registration request
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # valid details provided. Create user
            user = form.save()

            # login user
            login(request, user)
            return redirect('home')
        
    else:
        form = UserCreationForm()

    return render(request, 'blogapi_auth/signup.html', {'form': form})


def auth_logout(request):
    if request.method == 'POST':
        logout(request)

    return redirect('home')
