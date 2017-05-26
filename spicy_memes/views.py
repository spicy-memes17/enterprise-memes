from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import SignUpForm
from .forms import LogInForm
from .models import MyUser
from django.contrib.auth import authenticate, login

def content(request):
    current_user = request.user
    return render(request, 'content.html', {'user' : current_user})

def signUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = request.POST['username']
            user.email = request.POST['email']
            user.password = request.POST['password']
            user.save()
            return HttpResponseRedirect('/spicy_memes')

    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'signUpForm': form})

def userprofile(request):
    return render(request, 'userProfile.html')

def trendingPage(request):
    return render(request, 'trending.html')

def freshPage(request):
    return render(request, 'fresh.html')

def loginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        print(username)
        password = request.POST['password']
        print(password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/spicy_memes') #succes redirect to the startpage
        else:
            print("no-succes")
            return HttpResponseRedirect('/spicy_memes/loginPage') #wrong login-information: reload for the moment
            


    else:
        form = LogInForm()

    return render(request, 'login.html', {'LogInForm': form})