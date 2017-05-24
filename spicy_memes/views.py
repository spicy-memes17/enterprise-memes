from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import SignUp

def content(request):
    return render(request, 'content.html')

def signUp(request):
    if request.method == 'POST':
        signUpForm = SignUp(request.POST)
        if signUpForm.isVaild():
            # use data
            return HttpResponseRedirect('/content/')

    else:
        signUpForm = SignUp()

    return render(request, 'signup.html', {'signUpForm': signUpForm})